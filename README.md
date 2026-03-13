# LING 102 Study Tools

Interactive study tools for:

• IPA symbol recognition  
• English dialect transcription

These programs play audio and quiz you interactively in the terminal.

---

# STEP 1 — Install Python

1. Go to the Python download page:

https://www.python.org/downloads/

2. Click the large **Download Python** button.

3. Run the installer that downloads.

4. ⚠️ VERY IMPORTANT: make sure this box is checked during installation:

```
Add Python to PATH
```

5. Click **Install Now**.

Wait for Python to finish installing.

---

# STEP 2 — Open a Terminal

## Mac

1. Press **Command + Space**
2. Type:

```
Terminal
```

3. Press **Enter**

---

## Windows

1. Press the **Windows key**
2. Type:

```
cmd
```

3. Click **Command Prompt**


---

# STEP 3 — Check Python Installed Correctly

Copy and paste this command into the terminal and press Enter:

```bash
python --version
```

You should see something like:

```
Python 3.12.3
```

If you see a version number, Python is installed correctly.

If you see an error, restart your computer and try again.

---

# STEP 4 — Download the Study Tools

### Option A (Recommended)

Copy and paste this command into the terminal:

```bash
git clone https://github.com/YOURUSERNAME/ling102-study-tools.git
```

Then run:

```bash
cd ling102-study-tools
```

---

### Option B (If git does not work)

1. Go to the GitHub page:

```
https://github.com/YOURUSERNAME/ling102-study-tools
```

2. Click the green **Code** button.

3. Click **Download ZIP**.

4. Unzip the folder.

5. Open a terminal inside that folder.

---

# STEP 5 — Install Required Packages

Copy and paste this command:

```bash
pip install -r requirements.txt
```

Then run:

```bash
playwright install
```

This installs the browser used for playing audio.

---

# STEP 6 — Run the IPA Study Tool

Copy and paste:

```bash
python ipa_trainer.py
```

You will see instructions and the quiz will begin.

---

# IPA Commands

```
1 = show answer
2 = mark correct
3 = mark incorrect
4 = repeat audio
5 = skip symbol
6 = quit
```

If you skip a symbol, it will be permanently removed from practice.

To restore skipped symbols, open the file:

```
skip.json
```

and delete the character from the list.

---

# STEP 7 — Run the Dialect Trainer

Copy and paste:

```bash
python dialect_trainer.py
```

---

# If Python does not run

Try using this command instead:

```bash
python3 ipa_trainer.py
```

or

```bash
python3 dialect_trainer.py
```

Some systems use `python3` instead of `python`.

---

# Troubleshooting

### If `pip` does not work

Run:

```bash
python -m pip install -r requirements.txt
```

---

### If the audio browser does not install

Run:

```bash
python -m playwright install
```

---

# Notes

• When the program starts, a small browser window will open.  
• **Do not close this window** — it is used to play audio.  
• You can minimize it if you want.