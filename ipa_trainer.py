import asyncio
import random
import json
import sys
from dataclasses import dataclass
from typing import List

from playwright.async_api import async_playwright, Page

INDEX_URL = "https://jbdowse.com/ipa/"
SKIP_FILE = "skip.json"


@dataclass
class Item:
    char: str
    place: str
    manner: str
    feature: str
    place_label: str
    manner_label: str
    feature_label: str
    audio: List[str]


# -------------------- skip list --------------------

try:
    with open(SKIP_FILE) as f:
        skipped = set(json.load(f))
except:
    skipped = set()


def save_skip():
    with open(SKIP_FILE, "w") as f:
        json.dump(list(skipped), f)


# -------------------- welcome --------------------

def show_welcome():

    print("""
========================================
        LING 102 IPA STUDY TOOL
========================================

Instructions:

1. After pressing ENTER, a browser window will open.
Please keep it open so the audio can play. You may minimize it if needed.

2. Listen to the audio or examine the character
and write the voicing, manner, and placement.

3. After revealing the answer, mark whether
you got it correct or incorrect.

4. If you SKIP a character it will be skipped forever.
To restore it, remove it from skip.json.

5. Incorrect characters will reappear every 5 questions.

Commands:

1 = show answer
2 = mark correct
3 = mark incorrect
4 = repeat audio
5 = skip symbol
6 = quit

----------------------------------------

Press ENTER to start.
""")

    input()


# -------------------- loading indicator --------------------

def show_loading(msg="\n⏳ Loading next character..."):
    sys.stdout.write("\r" + msg)
    sys.stdout.flush()


def clear_loading():
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()


# -------------------- audio --------------------

async def play_audio(page: Page, audio_ids):

    for src in audio_ids:

        button = page.locator(f'button[data-src="{src}"]').first

        if await button.count() > 0:
            await button.click()

        await asyncio.sleep(1.8)


# -------------------- symbol extraction --------------------

async def get_random_symbol(page: Page) -> Item:

    tables = await page.query_selector_all("table")

    while True:

        table = random.choice(tables)

        headers = await table.query_selector_all("thead th")
        rows = await table.query_selector_all("tbody tr")

        if len(headers) < 2 or len(rows) == 0:
            continue

        table_class = await table.get_attribute("class") or ""
        is_vowel = "vowel" in table_class

        header_index = random.randint(1, len(headers) - 1)
        row = random.choice(rows)

        row_label_el = await row.query_selector("td")

        if not row_label_el:
            continue

        row_label = (await row_label_el.inner_text()).strip()

        col_left = 2 * header_index - 1
        col_right = col_left + 1

        cells = await row.query_selector_all("td")

        if col_left >= len(cells):
            continue

        candidates = []

        if col_left < len(cells):
            candidates.append((cells[col_left], "left"))

        if col_right < len(cells):
            candidates.append((cells[col_right], "right"))

        cell, side = random.choice(candidates)

        cell_class = await cell.get_attribute("class") or ""

        if "blank" in cell_class:
            continue

        char_el = await cell.query_selector("p")

        if not char_el:
            continue

        char = (await char_el.inner_text()).strip()

        if char in skipped:
            continue

        place = (await headers[header_index].inner_text()).strip()

        if is_vowel:
            feature = "unrounded" if side == "left" else "rounded"
            place_label = "Backness"
            manner_label = "Height"
            feature_label = "Rounding"
        else:
            feature = "voiceless" if side == "left" else "voiced"
            place_label = "Place"
            manner_label = "Manner"
            feature_label = "Voicing"

        buttons = await cell.query_selector_all("button")

        audio = []

        for b in buttons:
            src = await b.get_attribute("data-src")
            if src:
                audio.append(src)

        return Item(
            char,
            place,
            row_label,
            feature,
            place_label,
            manner_label,
            feature_label,
            audio
        )


# -------------------- browser --------------------

async def start_browser():

    p = await async_playwright().start()

    browser = await p.chromium.launch(
        headless=False,
        args=[
            "--window-size=200,200",
            "--disable-backgrounding-occluded-windows",
            "--disable-features=CalculateNativeWinOcclusion"
        ]
    )

    context = await browser.new_context(
        viewport={"width": 200, "height": 200}
    )

    page = await context.new_page()

    await page.goto(INDEX_URL)

    return p, browser, page


# -------------------- main --------------------

async def main():

    show_welcome()

    print("⏳ Loading IPA chart...")

    p, browser, page = await start_browser()

    incorrect_pool: List[Item] = []
    question_count = 0

    while True:

        question_count += 1

        if incorrect_pool and question_count % 5 == 0:

            item = random.choice(incorrect_pool)
            print("\n🔁 Reviewing incorrect symbol")

        else:

            show_loading()
            item = await get_random_symbol(page)
            clear_loading()

        print("\n📝 New Character")
        print("Character:", item.char)

        print("""
Commands
1 = show answer
2 = mark correct
3 = mark incorrect
4 = repeat audio
5 = skip symbol
6 = quit
""")

        await play_audio(page, item.audio)

        while True:

            cmd = input("> ").strip()

            if cmd == "1":

                print(item.feature_label + ":", item.feature)
                print(item.place_label + ":", item.place)
                print(item.manner_label + ":", item.manner)

            elif cmd == "2":

                if item in incorrect_pool:
                    incorrect_pool.remove(item)

                print("✅ marked correct")
                break

            elif cmd == "3":

                incorrect_pool.append(item)
                print("❌ marked incorrect")
                break

            elif cmd == "4":

                await play_audio(page, item.audio)

            elif cmd == "5":

                skipped.add(item.char)
                save_skip()

                print("Skipped:", item.char)
                break

            elif cmd == "6":

                await browser.close()
                await p.stop()
                return

            else:

                print("Use numbers 1–6")


if __name__ == "__main__":
    asyncio.run(main())