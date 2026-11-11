"""WonderSnap: snap a photo or ask a question, get a playable science simulation."""

import base64
import hashlib
import io
import os
import re
import time
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

from prompts import LEVELS, SYSTEM_PROMPT, build_user_prompt

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")  # check AI Studio for the newest Flash
DEMO_DIR = Path(__file__).parent / "demos"
FRAME_HEIGHT = 820

st.set_page_config(page_title="WonderSnap", page_icon="✨", layout="centered")


# ---------- helpers ----------
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")


def extract_html(text: str) -> str:
    """Pull the HTML document out of whatever the model returned."""
    m = re.search(r"<<<HTML>>>(.*?)(?:<<<END>>>|$)", text, re.S)
    html = m.group(1) if m else text
    html = re.sub(r"^\s*```(?:html)?", "", html.strip())
    html = re.sub(r"```\s*$", "", html).strip()
    low = html.lower()
    start = low.find("<!doctype")
    if start < 0:
        start = low.find("<html")
    if start > 0:
        html = html[start:]
    end = html.lower().rfind("</html>")
    if end >= 0:
        html = html[: end + 7]
    return html.strip()


def looks_valid(html: str) -> bool:
    low = html.lower()
    return "<script" in low and ("<canvas" in low or "<svg" in low) and low.endswith("</html>")


def prepare_image(raw: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    img.thumbnail((1024, 1024))  # smaller upload = faster response
    return img


def call_gemini(api_key, model, img, level, question, status):
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    contents = ([img] if img is not None else []) + [build_user_prompt(level, question, img is not None)]

    def make_config(fast: bool):
        kwargs = dict(system_instruction=SYSTEM_PROMPT, temperature=0.7)
        if fast:
            kwargs["thinking_config"] = types.ThinkingConfig(thinking_level="low")
        return types.GenerateContentConfig(**kwargs)

    last_err = None
    for fast in (True, False):  # some models reject thinking_level; retry without it
        try:
            text, t0 = "", time.time()
            for chunk in client.models.generate_content_stream(
                model=model, contents=contents, config=make_config(fast)
            ):
                text += chunk.text or ""
                status.update(label=f"✍️ Writing your simulation… {len(text):,} characters ({time.time()-t0:.0f}s)")
            return text
        except Exception as e:  # noqa: BLE001
            last_err = e
            if not fast or "thinking" not in str(e).lower():
                break
    raise last_err


def generate(api_key, model, img, level, question, status):
    """Generate, validate, retry once if the code looks broken."""
    for attempt in (1, 2):
        html = extract_html(call_gemini(api_key, model, img, level, question, status))
        if looks_valid(html):
            return html
        status.update(label="🔧 First draft looked broken, retrying once…")
    return html  # show it anyway; better than nothing


def list_demos():
    return sorted(p.stem for p in DEMO_DIR.glob("*.html"))


def show(html: str):
    """Render AI-generated HTML in an isolated iframe.

    A data: URL gives the page an opaque origin, so generated JavaScript can't
    reach the Streamlit app (cookies, DOM, session) even if it misbehaves.
    """
    src = "data:text/html;base64," + base64.b64encode(html.encode("utf-8")).decode()
    if hasattr(st, "iframe"):  # Streamlit >= 1.5x
        st.iframe(src, height=FRAME_HEIGHT)
    else:
        components.iframe(src, height=FRAME_HEIGHT, scrolling=True)


# ---------- sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")
    model = st.text_input("Gemini model", DEFAULT_MODEL, help="Use the newest Flash model listed in AI Studio.")
    api_key = get_api_key() or st.text_input("Gemini API key", type="password")
    compare = st.toggle("Compare two levels side by side", help="Generates a second version at another level (twice as slow).")
    st.divider()
    st.subheader("🛟 Backup demos")
    demo_mode = st.toggle("Offline demo mode", help="Play a saved simulation, no API needed.")
    demos = list_demos()
    demo_pick = st.selectbox("Saved demo", demos) if demos else None

# ---------- main ----------
st.title("✨ WonderSnap")
st.caption("Snap anything. Ask anything. Play with the science behind it.")

if demo_mode:
    if demo_pick:
        show((DEMO_DIR / f"{demo_pick}.html").read_text(encoding="utf-8"))
    else:
        st.info("No saved demos yet.")
    st.stop()

src = st.radio("Input", ["📷 Camera", "🖼️ Upload / phone camera", "💬 Just a question"], horizontal=True,
               label_visibility="collapsed")
raw = None
if src == "📷 Camera":
    shot = st.camera_input("Point at something you're curious about")
    raw = shot.getvalue() if shot else None
elif src == "🖼️ Upload / phone camera":
    up = st.file_uploader("On a phone this opens your rear camera", type=["jpg", "jpeg", "png", "webp", "heic"])
    raw = up.getvalue() if up else None

question = st.text_input("Your question (optional with a photo)", placeholder="e.g. How does a French press work?")
level = st.segmented_control("Explain it like I'm a…", list(LEVELS), default="High Schooler") or "High Schooler"
level2 = None
if compare:
    others = [l for l in LEVELS if l != level]
    level2 = st.segmented_control("…and compare with", others, default=others[0]) or others[0]

go = st.button("✨ Make it playable", type="primary", use_container_width=True,
               disabled=not (raw or question.strip()))

if go:
    if not api_key:
        st.error("Add a Gemini API key in the sidebar (or .streamlit/secrets.toml).")
        st.stop()
    try:
        img = prepare_image(raw) if raw else None
    except Exception:
        st.error("Couldn't read that image. Try a JPG or PNG.")
        st.stop()
    key = hashlib.sha1((raw or b"") + f"|{question}|{model}".encode()).hexdigest()
    cache = st.session_state.setdefault("cache", {})
    results = {}
    for lv in [level] + ([level2] if level2 else []):
        ck = f"{key}|{lv}"
        if ck in cache:
            results[lv] = cache[ck]
            continue
        with st.status(f"🔍 Looking closely ({lv})…", expanded=False) as status:
            try:
                cache[ck] = results[lv] = generate(api_key, model, img, lv, question, status)
                status.update(label=f"✅ Ready ({lv})", state="complete")
            except Exception as e:  # noqa: BLE001
                status.update(label="❌ Generation failed", state="error")
                st.error(f"Gemini error: {e}")
                st.info("Turn on **Offline demo mode** in the sidebar to keep the demo going.")
                st.stop()
    st.session_state["results"] = results

results = st.session_state.get("results")
if results:
    if len(results) == 1:
        show(next(iter(results.values())))
    else:
        for tab, (lv, html) in zip(st.tabs(list(results)), results.items()):
            with tab:
                show(html)
    with st.expander("💾 Save as backup demo / download"):
        lv, html = next(iter(results.items()))
        name = st.text_input("Demo name", value="my-demo")
        c1, c2 = st.columns(2)
        if c1.button("Save to demos/"):
            DEMO_DIR.mkdir(exist_ok=True)
            safe = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-") or "demo"
            (DEMO_DIR / f"{safe}.html").write_text(html, encoding="utf-8")
            st.success(f"Saved demos/{safe}.html")
        c2.download_button("Download HTML", html, file_name=f"{name}.html", mime="text/html")
