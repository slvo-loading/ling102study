# LING 102 Study Tools

Interactive study tools for:

• IPA symbol recognition  
• English dialect transcription  

These programs play audio and quiz you interactively in the terminal.

---

# STEP 1 — Install Python

1. Go to:

https://www.python.org/downloads/

2. Click **Download Python**

3. Run the installer.

4. ⚠️ VERY IMPORTANT: make sure this box is checked:

```
Add Python to PATH
```

5. Finish installation.

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

# STEP 3 — Download the Study Tools

Copy and paste this command into the terminal:

```bash
git clone https://github.com/slvo-loading/ling102study.git
```

Then move into the folder:

```bash
cd ling102study
```

You should now be inside the project folder.

---

# STEP 4 — Create a Virtual Environment

This step prevents Python installation issues.

Copy and paste:

```bash
python3 -m venv venv
```

Then activate it.

### Mac / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Your terminal should now look like this:

```
(venv)
```

---

# STEP 5 — Install Required Packages

Copy and paste:

```bash
pip install -r requirements.txt
```

Then install the audio browser:

```bash
playwright install
```

---

# STEP 6 — Run the IPA Trainer

Copy and paste:

```bash
python ipa_trainer.py
```

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

Skipping a character removes it from practice.  
To restore skipped characters, edit `skip.json`.

---

# Run the Dialect Trainer

```bash
python dialect_trainer.py
```

---

# Important Notes

• When the program starts, a small browser window will open.  
• **Do not close the browser window** — it plays the audio.  
• You can minimize it.

---

# If Something Doesn't Work

Make sure you are inside the project folder:

```bash
cd ling102study
```

Make sure the virtual environment is active:

```
(venv)
```

If it is not active, run:

```bash
source venv/bin/activate
```

Then try running the trainer again.