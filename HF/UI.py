import sys
import os
import json
import streamlit as st
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BrandNewDAI",
    layout="wide",
    page_icon="✦",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #111111;
    color: #f0f0f0;
}
.stApp { background-color: #111111; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 2rem 2.5rem; max-width: 1400px; }

/* ── Topbar ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 0 2rem 0; border-bottom: 1px solid #222; margin-bottom: 2.5rem;
}
.topbar-logo { font-size: 1.35rem; font-weight: 800; letter-spacing: -0.03em; }
.logo-brand { color: #e03a9a; }
.logo-new   { color: #f0f0f0; }
.logo-dai   { color: #f2880b; }
.topbar-nav { display: flex; gap: 2rem; font-size: 0.85rem; font-weight: 500; color: #888; }
.topbar-nav span.active { color: #e03a9a; border-bottom: 1.5px solid #e03a9a; padding-bottom: 2px; }
.ai-badge {
    display: inline-flex; align-items: center; gap: 0.35rem;
    background: rgba(242,136,11,0.15); border: 1px solid rgba(242,136,11,0.3);
    border-radius: 20px; padding: 0.25rem 0.75rem;
    font-size: 0.68rem; font-weight: 700; color: #f2880b;
    letter-spacing: 0.06em; text-transform: uppercase;
}

/* ── Section label ── */
.section-label {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.18em;
    text-transform: uppercase; color: #e03a9a; margin-bottom: 0.35rem;
}

/* ── Card ── */
.card {
    background: #181818; border: 1px solid #252525; border-radius: 14px;
    padding: 1.5rem; margin-bottom: 1.2rem;
}
.card-label {
    font-size: 0.62rem; color: #484848; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.45rem;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #1e1e1e !important; border: 1px solid #2e2e2e !important;
    border-radius: 10px !important; color: #f0f0f0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #e03a9a !important;
    box-shadow: 0 0 0 2px rgba(224,58,154,0.15) !important;
}
label, .stTextInput label, .stTextArea label, .stSelectbox label {
    color: #888 !important; font-size: 0.78rem !important;
    font-weight: 500 !important; letter-spacing: 0.04em !important;
}

/* ── ALL buttons: ghost by default ── */
.stButton > button {
    background: #1a1a1a !important;
    border: 1px solid #2e2e2e !important;
    border-radius: 10px; color: #888 !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.82rem; font-weight: 600; letter-spacing: 0.03em;
    padding: 0.6rem 1rem; width: 100%;
    transition: all 0.18s;
}
.stButton > button:hover {
    border-color: #e03a9a !important;
    color: #e03a9a !important;
    background: rgba(224,58,154,0.06) !important;
}

/* Primary button wrapper */
.primary-btn .stButton > button {
    background: linear-gradient(135deg, #e03a9a, #f2880b) !important;
    border: none !important; color: #fff !important; font-weight: 700 !important;
}
.primary-btn .stButton > button:hover {
    opacity: 0.88; color: #fff !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent; gap: 0.25rem; border-bottom: 1px solid #222;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; border: none; color: #555;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.78rem; font-weight: 600; letter-spacing: 0.06em;
    text-transform: uppercase; padding: 0.5rem 0.9rem; border-radius: 8px 8px 0 0;
}
.stTabs [aria-selected="true"] {
    color: #e03a9a !important;
    border-bottom: 2px solid #e03a9a !important;
    background: transparent !important;
}

/* ── Result box (fallback) ── */
.result-box {
    background: #161616; border: 1px solid #252525; border-radius: 12px;
    padding: 1.25rem 1.5rem; font-family: 'DM Mono', monospace;
    font-size: 0.78rem; color: #bbb; line-height: 1.7;
    white-space: pre-wrap; word-break: break-word;
}

/* ── Empty state ── */
.empty-state {
    color: #2e2e2e; font-size: 0.8rem; padding: 3rem 0;
    text-align: center; line-height: 2.2;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #e03a9a !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in {
    "result_identity": None,
    "result_palette":  None,
    "result_naming":   None,
    "result_tone":     None,
    "logo_image":      None,
    "do_logo":         False,
    "do_identity":     False,
    "do_palette":      False,
    "do_naming":       False,
    "do_tone":         False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

if "api" not in st.session_state:
    try:
        from brandNewDAI import brandNewDAI
        st.session_state.api = brandNewDAI()
    except Exception:
        st.session_state.api = None

# ── Render helpers ─────────────────────────────────────────────────────────────
def safe_json(val):
    if val is None: return None
    if isinstance(val, dict): return val
    try: return json.loads(val)
    except Exception: return None

def render_identity(data):
    d = safe_json(data)
    if not d:
        st.markdown('<div class="result-box">' + str(data) + '</div>', unsafe_allow_html=True); return
    persona = d.get("brand_persona", "—")
    slogan  = d.get("slogan", "—")
    values  = d.get("core_values", [])
    st.markdown(f"""
    <div class="card">
      <div class="card-label">Persona</div>
      <p style="font-size:0.88rem;color:#ccc;margin:0;line-height:1.55">{persona}</p>
    </div>
    <div class="card">
      <div class="card-label">Slogan</div>
      <p style="font-size:1rem;font-weight:700;color:#e03a9a;font-style:italic;margin:0">"{slogan}"</p>
    </div>
    <div class="card">
      <div class="card-label">Core Values</div>
      <div style="display:flex;gap:0.5rem;flex-wrap:wrap">
        {"".join(f'<span style="background:rgba(224,58,154,0.1);border:1px solid rgba(224,58,154,0.25);border-radius:20px;padding:0.28rem 0.8rem;font-size:0.74rem;color:#e03a9a;font-weight:600">{v}</span>' for v in values)}
      </div>
    </div>
    """, unsafe_allow_html=True)

def render_palette(data):
    d = safe_json(data)
    if not d:
        st.markdown('<div class="result-box">' + str(data) + '</div>', unsafe_allow_html=True); return
    colours = d.get("palette", [])
    colours.sort(key=lambda c: {"primary":0,"secondary":1,"accent":2,"neutral":3}.get(c.get("type",""),9))
    for c in colours:
        hex_val = c.get("hex", "#888888")
        name    = c.get("name", "—")
        ctype   = c.get("type", "").capitalize()
        expl    = c.get("explanation", "")
        try:
            r,g,b   = int(hex_val[1:3],16), int(hex_val[3:5],16), int(hex_val[5:7],16)
            lbl_col = "#111" if (0.299*r + 0.587*g + 0.114*b) > 140 else "#fff"
        except Exception:
            lbl_col = "#fff"
        st.markdown(f"""
        <div class="card" style="display:flex;gap:1.1rem;align-items:center;padding:0.9rem 1.1rem">
          <div style="min-width:56px;height:56px;border-radius:10px;background:{hex_val};flex-shrink:0;
                      display:flex;align-items:center;justify-content:center;
                      border:1px solid rgba(255,255,255,0.07)">
            <span style="font-size:0.5rem;font-family:'DM Mono',monospace;color:{lbl_col};font-weight:600">{hex_val}</span>
          </div>
          <div>
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.2rem">
              <span style="font-size:0.88rem;font-weight:700;color:#ddd">{name}</span>
              <span style="background:rgba(255,255,255,0.05);border-radius:8px;padding:0.1rem 0.45rem;
                           font-size:0.58rem;color:#555;font-weight:700;text-transform:uppercase;
                           letter-spacing:0.08em">{ctype}</span>
            </div>
            <p style="font-size:0.75rem;color:#5a5a5a;margin:0;line-height:1.45">{expl}</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

def render_naming(data):
    d = safe_json(data)
    if not d:
        st.markdown('<div class="result-box">' + str(data) + '</div>', unsafe_allow_html=True); return
    for i, n in enumerate(d.get("naming_suggestions", [])):
        name    = n.get("name", "—")
        concept = n.get("concept", "")
        vibe    = n.get("vibe", "")
        st.markdown(f"""
        <div class="card" style="position:relative">
          <div style="position:absolute;top:0.9rem;right:1.1rem;font-size:0.58rem;
                      font-family:'DM Mono',monospace;color:#252525;font-weight:700">0{i+1}</div>
          <div style="font-size:1.05rem;font-weight:800;color:#fff;letter-spacing:-0.02em;margin-bottom:0.3rem">{name}</div>
          <p style="font-size:0.77rem;color:#666;margin:0 0 0.5rem 0;line-height:1.5">{concept}</p>
          <span style="background:rgba(242,136,11,0.1);border:1px solid rgba(242,136,11,0.22);
                       border-radius:20px;padding:0.22rem 0.7rem;font-size:0.68rem;
                       color:#f2880b;font-weight:600">{vibe}</span>
        </div>
        """, unsafe_allow_html=True)

def render_tone(data):
    d = safe_json(data)
    if not d:
        st.markdown('<div class="result-box">' + str(data) + '</div>', unsafe_allow_html=True); return
    tp         = d.get("tone_profile", {})
    tone_name  = tp.get("tone_name", "—")
    formality  = int(tp.get("formality_level", 5))
    enthusiasm = int(tp.get("enthusiasm", 5))
    vocab      = tp.get("vocabulary_style", "—")
    traits     = tp.get("voice_traits", [])
    example    = tp.get("example_sentence", "")

    st.markdown(f"""
    <div class="card">
      <div style="font-size:1.05rem;font-weight:800;color:#fff;margin-bottom:0.15rem">{tone_name}</div>
      <p style="font-size:0.75rem;color:#484848;margin:0">Vocabulary: <span style="color:#777">{vocab}</span></p>
    </div>
    """, unsafe_allow_html=True)
    f_pct = formality * 10
    st.markdown(f"""
    <div class="card">
      <div class="card-label">Formality</div>
      <div style="display:flex;align-items:center;gap:0.7rem">
        <div style="flex:1;height:5px;background:#222;border-radius:3px;overflow:hidden">
          <div style="width:{f_pct}%;height:100%;background:#e03a9a;border-radius:3px"></div>
        </div>
        <span style="font-size:0.68rem;font-family:'DM Mono',monospace;color:#484848;min-width:26px;text-align:right">{formality}/10</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    e_pct = enthusiasm * 10
    st.markdown(f"""
    <div class="card">
      <div class="card-label">Enthusiasm</div>
      <div style="display:flex;align-items:center;gap:0.7rem">
        <div style="flex:1;height:5px;background:#222;border-radius:3px;overflow:hidden">
          <div style="width:{e_pct}%;height:100%;background:#f2880b;border-radius:3px"></div>
        </div>
        <span style="font-size:0.68rem;font-family:'DM Mono',monospace;color:#484848;min-width:26px;text-align:right">{enthusiasm}/10</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    traits_html = "".join(
        f'<span style="background:rgba(224,58,154,0.08);border:1px solid rgba(224,58,154,0.2);'
        f'border-radius:20px;padding:0.25rem 0.75rem;font-size:0.72rem;color:#e03a9a;font-weight:600">{t}</span>'
        for t in traits
    )
    st.markdown(f"""
    <div class="card">
      <div class="card-label">Voice Traits</div>
      <div style="display:flex;gap:0.45rem;flex-wrap:wrap">{traits_html}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
      <div class="card-label">Example</div>
      <p style="font-size:0.85rem;color:#999;font-style:italic;margin:0;line-height:1.6;
                border-left:2px solid #e03a9a;padding-left:0.8rem">"{example}"</p>
    </div>
    """, unsafe_allow_html=True)

# ── Topbar ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="topbar-logo">
    <span class="logo-brand">Brand</span><span class="logo-new">New</span><span class="logo-dai">DAI</span>
  </div>
  <div class="topbar-nav">
    <span class="active">Design Brand</span>
    <span>Edit Brand</span>
    <span>Marketing</span>
  </div>
  <div class="ai-badge">✦ AI Studio</div>
</div>
""", unsafe_allow_html=True)

# ── Collect button presses BEFORE column split ─────────────────────────────────
# We read inputs and buttons here so gen_all can set all flags atomically.

col_in, col_out = st.columns([1, 1.5], gap="large")

with col_in:
    st.markdown('<div class="section-label">Brand Setup</div>', unsafe_allow_html=True)
    brand_name = st.text_input("Brand name", placeholder="e.g. Lumina Arch")
    purpose    = st.text_area("What does it do?", placeholder="Describe the mission and core values…", height=100)

    st.markdown('<div class="section-label" style="margin-top:1rem">Aesthetic</div>', unsafe_allow_html=True)
    style  = st.selectbox("Style direction", ["Minimalist","Cyberpunk","Organic","Luxury","Flat Design","Brutalist","Art Deco"], label_visibility="collapsed")
    colors = st.text_input("Colour palette hint", placeholder="e.g. Neon pink and deep black")
    uploaded = st.file_uploader("Upload aesthetic reference", type=["png","jpg","jpeg","webp"])

    st.markdown("<hr style='border-color:#222;margin:1.2rem 0'>", unsafe_allow_html=True)

    # ── Generate All (primary) ──
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    gen_all = st.button("✦  Generate All", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # ── Individual buttons: 2×2 grid ──
    r1a, r1b = st.columns(2)
    with r1a:
        gen_logo     = st.button("Logo",     use_container_width=True)
    with r1b:
        gen_identity = st.button("Identity", use_container_width=True)

    r2a, r2b = st.columns(2)
    with r2a:
        gen_palette  = st.button("Palette",  use_container_width=True)
    with r2b:
        gen_naming   = st.button("Naming",   use_container_width=True)

    gen_tone = st.button("Brand Tone", use_container_width=True)

# ── Resolve what to run ────────────────────────────────────────────────────────
do_logo     = gen_logo     or gen_all
do_identity = gen_identity or gen_all
do_palette  = gen_palette  or gen_all
do_naming   = gen_naming   or gen_all
do_tone     = gen_tone     or gen_all

ready  = bool(brand_name and purpose)
api    = st.session_state.api
api_ok = api is not None
any_action = any([do_logo, do_identity, do_palette, do_naming, do_tone])

# ── Run API calls ──────────────────────────────────────────────────────────────
if any_action and not ready:
    with col_in:
        st.warning("Fill in Brand Name and Purpose first.")
elif any_action and not api_ok:
    with col_in:
        st.error("API not initialised — check your brandNewDAI import.")
elif any_action and ready and api_ok:
    if do_logo:
        with st.spinner("Drawing logo…"):
            try:
                st.session_state.logo_image = api.generateLogoFromScratch(brand_name, style, purpose, colors)
            except Exception as e:
                st.error(f"Logo error: {e}")
    if do_identity:
        with st.spinner("Building identity…"):
            try:
                st.session_state.result_identity = api.generateIdentity(brand_name, purpose)
            except Exception as e:
                st.error(f"Identity error: {e}")
    if do_palette:
        with st.spinner("Picking colours…"):
            try:
                st.session_state.result_palette = api.generatePalette(brand_name, purpose)
            except Exception as e:
                st.error(f"Palette error: {e}")
    if do_naming:
        with st.spinner("Brainstorming names…"):
            try:
                st.session_state.result_naming = api.generateNaming(purpose, style)
            except Exception as e:
                st.error(f"Naming error: {e}")
    if do_tone:
        with st.spinner("Defining voice…"):
            try:
                st.session_state.result_tone = api.generateTone(brand_name, purpose)
            except Exception as e:
                st.error(f"Tone error: {e}")

# ── Right column: all results in tabs ─────────────────────────────────────────
with col_out:
    st.markdown('<div class="section-label">Generated Assets</div>', unsafe_allow_html=True)
    tabs = st.tabs(["Logo", "Identity", "Palette", "Naming", "Tone"])

    with tabs[0]:
        if st.session_state.logo_image:
            st.image(st.session_state.logo_image, use_container_width=True)
        elif uploaded:
            st.image(Image.open(uploaded), caption="Reference uploaded", use_container_width=True)
        else:
            st.markdown('<div class="empty-state">✦<br>Logo will appear here<br><span style="font-size:0.7rem;color:#252525">Press Logo or Generate All</span></div>', unsafe_allow_html=True)

    with tabs[1]:
        if st.session_state.result_identity:
            render_identity(st.session_state.result_identity)
        else:
            st.markdown('<div class="empty-state">✦<br>Identity will appear here</div>', unsafe_allow_html=True)

    with tabs[2]:
        if st.session_state.result_palette:
            render_palette(st.session_state.result_palette)
        else:
            st.markdown('<div class="empty-state">✦<br>Palette will appear here</div>', unsafe_allow_html=True)

    with tabs[3]:
        if st.session_state.result_naming:
            render_naming(st.session_state.result_naming)
        else:
            st.markdown('<div class="empty-state">✦<br>Name ideas will appear here</div>', unsafe_allow_html=True)

    with tabs[4]:
        if st.session_state.result_tone:
            render_tone(st.session_state.result_tone)
        else:
            st.markdown('<div class="empty-state">✦<br>Tone will appear here</div>', unsafe_allow_html=True)