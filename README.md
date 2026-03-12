# LING 102 Study Tools

Interactive command-line study tools for:

- IPA symbols
- English dialect transcription

Both tools play audio and quiz you interactively.

---

# 1. Install Python

Download Python here:

https://www.python.org/downloads/

During installation make sure to check:

✔ Add Python to PATH

---

# 2. Download the study tools

Download this folder or clone the repository.

Then open a terminal inside the folder.

---

# 3. Install dependencies

Run:

```bash
pip install -r requirements.txt
playwright install
```

This installs the audio browser used by the program.

---

# 4. Run the IPA trainer

```bash
python ipa_trainer.py
```

Commands:

```
1 = show answer
2 = mark correct
3 = mark incorrect
4 = repeat audio
5 = skip symbol
6 = quit
```

Skipped characters are stored in `skip.json`.

To restore a skipped character, open `skip.json` and delete it from the list.

---

# 5. Run the Dialect trainer

```bash
python dialect_trainer.py
```

Commands:

```
1 = show answer
2 = mark correct
3 = mark incorrect
4 = repeat audio
5 = quit
```