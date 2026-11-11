# ✨ WonderSnap

Snap a photo or ask a question and get a playable physics or engineering simulation, generated live by Gemini.

## Setup (about 5 minutes)

```bash
cd wondersnap
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# paste your key from https://aistudio.google.com/apikey into secrets.toml
streamlit run app.py
```

**Model:** the default is `gemini-3.5-flash`. Google retires models often, so check which Flash models AI Studio currently lists, then change the name in the sidebar or set `GEMINI_MODEL=...` before running.

## Files

| File | What it does |
| --- | --- |
| `app.py` | Streamlit UI: camera / upload / question input, level picker, streaming generation, retry, sandboxed rendering, backup demos |
| `prompts.py` | The system prompt (output contract, layout, quiz rules) and the per-level instructions. **Tune this file the most.** |
| `demos/` | Saved simulations for offline demo mode. Ships with `bicycle-gears.html`. |

## How it works

1. The image is shrunk to 1024 px (faster upload) and sent to Gemini with the system prompt and level.
2. Gemini streams back HTML between `<<<HTML>>>` / `<<<END>>>` markers. A live character counter shows progress.
3. `extract_html()` strips markers and stray markdown fences. If the page has no `<script>` plus `<canvas>`/`<svg>`, the app retries once.
4. The page is shown in an iframe loaded from a `data:` URL, so the generated JavaScript runs on an isolated origin and can't touch the app.
5. Results are cached per photo + question + level, so re-clicking during the demo is instant.

## Demo-day checklist

- [ ] **Pre-bake 3 backups.** Generate a French press, a bicycle and a Wi-Fi router, then use **Save as backup demo** under each result. If the Wi-Fi or API fails, turn on **Offline demo mode** in the sidebar. (Backups don't need the API, but their styling still loads from the Tailwind CDN. Without internet they work but look plain.)
- [ ] **Show the "wow" comparison:** turn on *Compare two levels side by side* and show the 7-Year-Old vs Engineer versions of one object.
- [ ] **Phone demo:** phones need HTTPS for the camera, so deploy free on [Streamlit Community Cloud](https://share.streamlit.io) and add `GEMINI_API_KEY` under the app's *Secrets*. On a phone, use **Upload / phone camera**: it opens the rear camera, whereas the webcam widget often opens the selfie camera.
- [ ] Narrate the wait: "it's writing a brand-new app for you right now."
- [ ] Never commit `.streamlit/secrets.toml` (already in `.gitignore`).
