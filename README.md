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
> 💡 Can't see the .streamlit folder? Folders starting with a dot are hidden by default. Mac: press Cmd + Shift + . in Finder. Windows: in File Explorer choose **View → Show → Hidden items**. You can also skip this step and paste your key into the app's sidebar each time you run it.

**5. Start the app:**
streamlit run app.py
Your browser opens at **http://localhost:8501**. 🎉 To stop the app, go back to the terminal and press Ctrl + C.

---

## 🎮 Step 3 — Using the app

1. **Check the sidebar (left).** Under **AI provider**, pick *Google Gemini* or *OpenRouter*. The app picks whichever one has a saved key. If you see "🔑 Using … from secrets", you're set.
2. **Choose your input** at the top:
   - **📷 Camera:** use your webcam. Click *Take Photo*. The first time, the browser asks permission to use the camera; click *Allow*.
   - **🖼 Upload / phone camera:** choose a photo file. On a phone this opens the normal rear camera.
   - **💬 Just a question:** no photo; type something like *"How does a microwave heat food?"*
3. **Optionally add a question**, for example *"Why does the chain need oil?"*
4. **Pick a level:** 7-Year-Old, High Schooler or Engineer.
5. Click **✨ Make it playable** and wait about 10–30 seconds. The progress bar counts characters as the AI writes your page.
6. **Play!** Move the sliders, watch the animation change, then press **🧠 Test yourself**.

**Extra features (sidebar):**
- **Compare two levels side by side:** makes two versions (for example 7-Year-Old vs Engineer) and shows them in tabs. Takes about twice as long.
- **Offline demo mode:** plays a saved simulation with no AI call. Useful if the internet drops.
- **💾 Save as backup demo** (under each result): saves a result you like into the demos folder so offline mode can play it later.

---

## 🎤 Tips for a live demo

- ✅ **Save 3 backups the day before.** Try a French press, a bicycle and a Wi-Fi router, then press *Save as backup demo* on each good result. If the Wi-Fi or the AI fails on stage, turn on **Offline demo mode**. (Backups don't need the AI, but their styling still downloads from the internet, so without any internet they work but look plain.)
- ✅ **Show the same object at two levels.** It's the quickest way to show the AI adapts to the learner.
- ✅ **Use the wait.** Say *"it's writing a brand-new app just for this photo right now."*
- ✅ **Asking the same thing twice is instant,** because results are remembered while the app is running.
- 📱 **Demoing on a phone?** Phones only allow the camera on secure (https://) sites. Put the app online for free with [Streamlit Community Cloud](https://share.streamlit.io): upload the folder to GitHub (without secrets.toml!), deploy it, then paste your key into the app's **Settings → Secrets** box in the same format as secrets.toml.

---

## 🧠 How it works (in plain language)

 📷 Photo / 💬 question  +  level
            │
            ▼
   WonderSnap (app.py) shrinks the photo and adds
   detailed instructions (prompts.py)
            │
            ▼
   🤖 AI model (Google Gemini or via OpenRouter)
   "This is a bicycle → gear ratios → here is a web page"
            │
            ▼
   WonderSnap cleans up the reply, checks it looks like
   a working page (retries once if not)
            │
            ▼
   🎮 The page runs in a sealed-off box on your screen

- **The instructions (system prompt)** in prompts.py tell the AI exactly what to build: layout, number of sliders, quiz rules, style, and to use only the Tailwind styling library.
- **Safety:** AI-written code runs inside an isolated frame (data: URL), so even buggy code can't touch the rest of the app or your data.
- **Speed:** photos are shrunk to 1024 px before upload, and the app asks the model for "low thinking" mode when the model supports it.

---

## 📁 What's in the folder
wondersnap/
├── app.py                       ← the app: buttons, camera, talking to the AI, showing results
├── prompts.py                   ← the instructions given to the AI (edit this to change the output)
├── requirements.txt             ← list of Python packages to install
├── demos/
│   └── bicycle-gears.html       ← a ready-made simulation for offline mode
├── .streamlit/
│   └── secrets.toml.example     ← template for your API keys
└── .gitignore                   ← stops your secrets file from being uploaded to GitHub

---

## 🛠 Changing things

| I want to… | Do this |
|---|---|
| **Use a different AI model** | Type its name in the sidebar's **Model** box. Google uses names like gemini-3.7-flash; see the model list in [AI Studio](https://aistudio.google.com). OpenRouter uses names like google/gemini-3.7-flash; browse [openrouter.ai/models](https://openrouter.ai/models) and copy the ID. Pick a model that accepts **images** if you want photo input. |
| **Change the default model permanently** | Edit the PROVIDERS section near the top of app.py, or set GEMINI_MODEL / OPENROUTER_MODEL as environment variables. |
| **Change what the pages look like or include** | Edit SYSTEM_PROMPT in prompts.py (for example *"use a dark theme"* or *"add a fun fact box"*). |
| **Change how each level explains things** | Edit LEVELS in prompts.py. You can add a new level there too; it appears in the app automatically. |
| **Make the result window taller** | Change FRAME_HEIGHT near the top of app.py. |

---

## 🩺 Troubleshooting

| Problem | Fix |
|---|---|
| python or pip "is not recognized" / "command not found" | Use python3 and pip3 instead, or reinstall Python with **"Add Python to PATH"** ticked (Windows). |
| streamlit: command not found | Your private environment isn't active. Run the *activate* command from Step 2, or run python -m streamlit run app.py. |
| "Add your … API key in the sidebar" | The key isn't saved. Check that the file is named exactly secrets.toml (not secrets.toml.txt), sits inside .streamlit, and has the key inside quotes. Then restart the app. |
| Error says **404 / model not found / no longer available** | That model was renamed or retired. Pick a current one (see *Changing things*) and type it in the sidebar. |
| Error says **401 / invalid key** | The key was copied wrong or deleted. Make a new one and paste it again. |
| Error says **402** (OpenRouter) | Your OpenRouter account is out of credit. Add some at openrouter.ai. |
| Error says **429 / quota / rate limit** | Too many requests too fast. Wait a minute, or switch provider in the sidebar. |
| Camera box is blank or says "allow access" | Click the camera icon in the browser's address bar and allow access. Close other apps that use the camera (Zoom, Teams). |
| Simulation shows but a slider or animation doesn't work | The AI wrote buggy code. Click **Make it playable** again with a slightly different question; every attempt is new. |
| Result looks unstyled (plain black text) | The Tailwind styling library couldn't download. Check your internet connection. |
| It's slow (more than 40 s) | Try a faster or "lite" model, use the 7-Year-Old level (shorter pages), or check your Wi-Fi. |

---

Built for a hackathon with ❤️, Streamlit, and Gemini.

```
