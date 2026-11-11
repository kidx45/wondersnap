``` # ✨ WonderSnap

**Point your camera at anything (a bicycle, a kettle, a Wi-Fi router) and get a mini science game that shows how it works.**

WonderSnap sends your photo (or a typed question) to an AI model. The AI works out what the object is and which science explains it, then writes a small interactive web page made just for you. The page has:

- 📝 a two-sentence explanation
- 🎞 an animated diagram
- 🎚 2–3 sliders or buttons that change the animation live (for example temperature, speed, or number of gear teeth)
- 🧠 a short quiz to check what you learned

You choose how deep the explanation goes: **7-Year-Old**, **High Schooler**, or **Engineer**.

---

## 📋 Contents

1. [What you need](#-what-you-need)
2. [Get an AI key (pick one)](#-step-1--get-an-ai-key-pick-one)
3. [Install and run](#-step-2--install-and-run)
4. [Using the app](#-step-3--using-the-app)
5. [Tips for a live demo](#-tips-for-a-live-demo)
6. [How it works](#-how-it-works-in-plain-language)
7. [What's in the folder](#-whats-in-the-folder)
8. [Changing things](#-changing-things)
9. [Troubleshooting](#-troubleshooting)

---

## 🧰 What you need

| You need | Why | How to check |
|---|---|---|
| A laptop (Windows, Mac or Linux) | To run the app | — |
| **Python 3.9 or newer** | The app is written in Python | Run python --version (on Mac/Linux, maybe python3 --version). Don't have it? Download it from [python.org](https://www.python.org/downloads/). On Windows, tick **"Add Python to PATH"** during install. |
| An internet connection | The AI runs online | — |
| **One** AI key: Google *or* OpenRouter | Lets the app talk to the AI | See Step 1 |
| A webcam (optional) | To snap photos | You can also upload a photo or just type a question |

No database or server setup, and you don't write any web code.

---

## 🔑 Step 1 — Get an AI key (pick one)

An "API key" is a password that lets the app use an AI service. **You only need one of these two.**

### Option A: Google AI Studio (Gemini)
1. Go to **https://aistudio.google.com/apikey** and sign in with a Google account.
2. Click **Create API key** and copy it.
3. Google AI Studio usually has a free tier, which is fine for a hackathon. Check the current limits on the page.

### Option B: OpenRouter
[OpenRouter](https://openrouter.ai) gives one key for models from many companies (Google, Anthropic, OpenAI, and others).
1. Go to **https://openrouter.ai/keys**, sign in, and click **Create key**. Copy it; it starts with sk-or-.
2. Add a few dollars of credit on OpenRouter, since most models are pay-per-use. Each simulation costs a fraction of a cent to a few cents, depending on the model.

> 🔒 **Keep your key secret.** Don't paste it in chat groups, slides, or GitHub. Anyone with it can spend your quota.

---

## 🚀 Step 2 — Install and run

Open a terminal (Mac: **Terminal**; Windows: **Command Prompt** or **PowerShell**) and run these commands one by one.

**1. Go into the project folder** (wherever you unzipped it):
cd path/to/wondersnap

**2. Create a private Python environment** (keeps this project's packages separate from the rest of your computer):

| Windows | Mac / Linux |
|---|---|
| python -m venv .venv | python3 -m venv .venv |
| .venv\Scripts\activate | source .venv/bin/activate |

Once it's active you'll see (.venv) at the start of the terminal line. Run the *activate* command again each time you open a new terminal.

**3. Install the packages:**
pip install -r requirements.txt

**4. Save your key.** In the .streamlit folder, make a copy of secrets.toml.example and name the copy **`secrets.toml`**. Open it in any text editor and paste your key between the quotes on the matching line:
GEMINI_API_KEY = "paste-your-google-key-here"      # if you chose Option A
OPENROUTER_API_KEY = "sk-or-paste-your-key-here"   # if you chose Option B
Fill in one or both, then save the file.
