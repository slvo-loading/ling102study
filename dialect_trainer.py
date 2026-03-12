import asyncio
import random
import re
from dataclasses import dataclass
from typing import Optional, List, Tuple
import sys

from playwright.async_api import async_playwright, Page, Locator

INDEX_URL = "https://www.lel.ed.ac.uk/research/gsound/Eng/Database/Phonetics/Englishes/ByWord/"
WORD_LINK_RE = re.compile(r"Word[_\s-]*\d+.*\.htm?$", re.IGNORECASE)


@dataclass
class Item:
    english_word: str
    accent: str
    ipa: str
    audio_url: str


# -------------------- welcome --------------------

def show_welcome():

    print("""
========================================
        ENGLISH DIALECT TRAINER
========================================

Instructions:

1. After pressing ENTER, a browser window will open.
Please keep it open so the audio can play. You may minimize it if needed.

2. Listen to the audio and narrowly transcribe
   the pronunciation on paper.

3. After revealing the answer, mark whether
   you got it correct or incorrect.
          
4. Incorrect items will reappear every 10 questions.

Commands:

1 = show answer
2 = mark correct
3 = mark incorrect
4 = repeat audio
5 = quit

----------------------------------------

Press ENTER to start.
""")

    input()

def show_loading(msg="\n⏳ Loading next audio..."):
    sys.stdout.write("\r" + msg)
    sys.stdout.flush()

def clear_loading():
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()


# -------------------- navigation --------------------

async def get_word_links(page: Page) -> List[str]:

    links = page.locator("a[href]")
    n = await links.count()

    out = []

    for i in range(n):

        el = links.nth(i)
        href = await el.get_attribute("href")

        if href and WORD_LINK_RE.search(href):
            out.append(href)

    return out


# -------------------- extraction --------------------

async def get_english_word(page: Page) -> str:

    word_span = page.locator("div.Section1 span[style*='32.0pt']")

    if await word_span.count() > 0:
        return (await word_span.first.inner_text()).strip()

    return "Unknown"


async def get_candidate_cells(page: Page) -> List[Locator]:

    a = page.locator("a[href]")
    n = await a.count()

    mp3_cells = []

    for i in range(n):

        el = a.nth(i)
        txt = (await el.inner_text()).strip()

        if txt.startswith("[") and txt.endswith("]"):

            href = await el.get_attribute("href")

            if href and href.lower().endswith(".mp3"):
                mp3_cells.append(el)

    return mp3_cells


async def get_audio_url(cell: Locator) -> str:

    href = await cell.get_attribute("href")

    if not href:
        raise RuntimeError("IPA cell missing audio link")

    return href


async def get_accent(cell: Locator) -> str:

    td = cell.locator("xpath=ancestor::td[1]")

    spans = td.locator("span")

    count = await spans.count()

    for i in range(count):

        sp = spans.nth(i)
        style = (await sp.get_attribute("style")) or ""

        if "Arial Narrow" in style:

            txt = (await sp.inner_text()).strip()

            if txt:
                return txt

    return "Unknown"


# -------------------- audio --------------------

async def play_audio(page: Page, url: str):

    await page.evaluate(
        """url => {
            if (!window.__trainerAudio) window.__trainerAudio = new Audio();
            window.__trainerAudio.pause();
            window.__trainerAudio.currentTime = 0;
            window.__trainerAudio.src = url;
            window.__trainerAudio.play();
        }""",
        url
    )


# -------------------- create new item --------------------

async def load_item(page: Page, word_links: List[str]) -> Item:

    href = random.choice(word_links)

    await page.goto(INDEX_URL + href)

    english_word = await get_english_word(page)

    cells = await get_candidate_cells(page)

    if not cells:
        raise RuntimeError("No IPA audio cells found")

    cell = random.choice(cells)

    ipa = (await cell.inner_text()).strip()
    audio_url = await get_audio_url(cell)
    accent = await get_accent(cell)

    return Item(english_word, accent, ipa, audio_url)


async def start_browser():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        return browser, page


# -------------------- main --------------------

async def main():

    show_welcome()

    print("⏳ Loading dialect database...")

    async with async_playwright() as p:

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

        word_links = await get_word_links(page)

        if not word_links:
            raise RuntimeError("No word pages found")


        incorrect_pool: List[Item] = []
        question_count = 0

        current_item = await load_item(page, word_links)

        while True:

            question_count += 1

            if incorrect_pool and question_count % 10 == 0:

                current_item = await load_item(random.choice(incorrect_pool))

                print("\n🔁 Reviewing incorrect item")

            else:
                show_loading()
                current_item = await load_item(page, word_links)
                clear_loading()

            await play_audio(page, current_item.audio_url)

            print("\n🔊 New Audio")
            print("Accent:", current_item.accent)

            print("""
Commands
1 = show answer
2 = mark correct
3 = mark incorrect
4 = repeat audio
5 = quit
""")

            while True:

                cmd = input("> ").strip()

                if cmd == "1":

                    print("\nEnglish word:", current_item.english_word)
                    print("IPA:", current_item.ipa)

                elif cmd == "2":

                    if current_item in incorrect_pool:
                        incorrect_pool.remove(current_item)

                    print("✅ marked correct")
                    break

                elif cmd == "3":

                    incorrect_pool.append(current_item)

                    print("❌ marked incorrect")
                    break

                elif cmd == "4":

                    await play_audio(page, current_item.audio_url)
                    print("🔁 repeat")

                elif cmd == "5":

                    await browser.close()
                    return

                else:

                    print("Use numbers 1–5")


if __name__ == "__main__":
    asyncio.run(main())