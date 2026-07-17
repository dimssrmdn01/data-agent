import os
import shutil
import base64
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from core_agent import create_agent

load_dotenv()

# ===========================================================
# ICON SYSTEM 
# ===========================================================
_ICON_PATHS = {
    "sparkles": ("M12 2L13.8 9.2L21 11L13.8 12.8L12 20L10.2 12.8L3 11L10.2 9.2L12 2Z", "solid"),
    "settings": (
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 '
        '1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 '
        '1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 '
        '9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 '
        '1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 '
        '1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>', "stroke_raw"
    ),
    "lightbulb": (
        '<path d="M9 18h6"/><path d="M10 22h4"/>'
        '<path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.3 1 2.3h6c0-1 .4-1.8 1-2.3A7 7 0 0 0 12 2Z"/>', "stroke_raw"
    ),
    "trash": (
        '<path d="M3 6h18"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'
        '<path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>'
        '<line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>', "stroke_raw"
    ),
    "upload": (
        '<path d="M12 15V3"/><path d="M7 8l5-5 5 5"/>'
        '<path d="M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4"/>', "stroke_raw"
    ),
    "eye": (
        '<path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7Z"/><circle cx="12" cy="12" r="3"/>', "stroke_raw"
    ),
    "key": (
        '<circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.6 12.4 19 4l3 3-2 2-2-2-2 2 2 2-2 2"/>', "stroke_raw"
    ),
    "chat": (
        '<path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 '
        '8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>', "stroke_raw"
    ),
    "bar-chart": (
        '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>',
        "stroke_raw"
    ),
    "user": (
        '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>', "stroke_raw"
    ),
}


def icon_svg(name: str, size: int = 18, color: str = "currentColor") -> str:
    """Return a raw <svg> string for the given icon name."""
    body, kind = _ICON_PATHS[name]
    if kind == "solid":
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 24 24" fill="{color}"><path d="{body}"/></svg>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
    )


def icon_data_uri(name: str, size: int = 64, color: str = "%23B9A6FF") -> str:
    """Base64 data-URI version of an icon, for use as st.chat_message / page avatars."""
    body, kind = _ICON_PATHS[name]
    color_raw = color.replace("%23", "#")
    if kind == "solid":
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color_raw}"><path d="{body}"/></svg>'
    else:
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'fill="none" stroke="{color_raw}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
        )
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64}"


def icon_label(name: str, text: str, size: int = 15, color: str = "#C9C4F0") -> str:
    """Inline icon + text row, for use inside st.markdown(..., unsafe_allow_html=True)."""
    return (
        f'<span class="icon-inline">{icon_svg(name, size, color)}<span>{text}</span></span>'
    )


ASSISTANT_AVATAR = icon_data_uri("sparkles", size=64, color="%23B9A6FF")
USER_AVATAR = icon_data_uri("user", size=64, color="%2338BDF8")
PAGE_ICON = icon_data_uri("sparkles", size=64, color="%237C3AED")

# ===========================================================
# PAGE CONFIG
# ===========================================================
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===========================================================
# CUSTOM CSS
# ===========================================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* ---------- Global ---------- */
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}
h1, h2, h3, .app-title {
    font-family: 'Space Grotesk', sans-serif !important;
}
.stApp {
    background: radial-gradient(circle at 15% 20%, #1b1035 0%, #0b0c1e 45%, #05050c 100%);
    background-attachment: fixed;
    color: #EDEBF7;
}
/* Hide default streamlit chrome */
#MainMenu, footer {visibility: hidden;}
.stDeployButton {display: none;}
/* ---------- Icon helpers ---------- */
.icon-inline {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    vertical-align: middle;
}
.icon-inline svg { flex-shrink: 0; display: block; }
/* ---------- Hero header ---------- */
.hero {
    padding: 2.2rem 2.2rem 1.8rem 2.2rem;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(124,58,237,0.35), rgba(56,189,248,0.18));
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(236,72,153,0.35), transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 4px 12px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #C9C4F0;
    margin-bottom: 0.8rem;
}
.hero-badge svg { color: #C9C4F0; }
.hero-title {
    font-size: 2.1rem;
    font-weight: 700;
    background: linear-gradient(90deg, #ffffff, #b9a6ff 60%, #7dd3fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero-sub {
    color: #ACA6D6;
    font-size: 0.95rem;
    margin-top: 0.4rem;
    max-width: 640px;
}
/* ---------- Glass cards ---------- */
.glass-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    padding: 1.3rem 1.4rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
}
/* ---------- Metric pills ---------- */
.metric-row { display: flex; gap: 0.9rem; margin: 1rem 0 1.4rem 0; flex-wrap: wrap; }
.metric-pill {
    flex: 1;
    min-width: 140px;
    background: linear-gradient(145deg, rgba(124,58,237,0.20), rgba(56,189,248,0.10));
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 0.9rem 1.1rem;
}
.metric-pill .label { font-size: 0.72rem; color: #A79EDB; text-transform: uppercase; letter-spacing: 0.05em; }
.metric-pill .value { font-size: 1.5rem; font-weight: 700; color: #fff; font-family: 'Space Grotesk', sans-serif; }
/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #120b26 0%, #0a0a18 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    color: #fff;
}
.sidebar-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #fff;
    margin-bottom: 0.2rem;
}
.sidebar-title svg { color: #A78EFF; }
.sidebar-caption { color: #8A83B8; font-size: 0.8rem; margin-bottom: 1.2rem; }
/* ---------- Upload label ---------- */
.upload-label {
    font-weight: 600;
    color: #EDEBF7;
    font-size: 0.95rem;
    margin-bottom: 0.4rem;
}
.upload-label svg { color: #7dd3fc; }
/* ---------- Preview label ---------- */
.preview-label {
    font-weight: 600;
    color: #EDEBF7;
    font-size: 0.92rem;
    margin: 0.2rem 0 0.6rem 0;
}
.preview-label svg { color: #A78EFF; }
/* ---------- File uploader ---------- */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(124,58,237,0.08) !important;
    border: 1.5px dashed rgba(167,142,255,0.45) !important;
    border-radius: 16px !important;
}
/* ---------- Dataframe ---------- */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}
/* ---------- Chat bubbles ---------- */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 0.4rem 0.6rem;
    margin-bottom: 0.6rem;
    animation: fadeInUp 0.35s ease;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
/* ---------- Chat input ---------- */
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
    color: #fff !important;
}
/* ---------- Buttons ---------- */
.stButton>button {
    background: linear-gradient(90deg, #7C3AED, #38BDF8);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.5rem 1.1rem;
    font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(124,58,237,0.45);
}
/* ---------- Empty state ---------- */
.empty-state {
    text-align: center;
    padding: 3.5rem 1.5rem;
    border-radius: 20px;
    border: 1px dashed rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.02);
}
.empty-state .icon-wrap {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    border-radius: 16px;
    background: linear-gradient(145deg, rgba(124,58,237,0.25), rgba(56,189,248,0.12));
    border: 1px solid rgba(255,255,255,0.1);
}
.empty-state .icon-wrap svg { color: #C9C4F0; }
.empty-state h3 { color: #fff; margin: 0.8rem 0 0.3rem 0; }
.empty-state p { color: #8A83B8; font-size: 0.92rem; }
/* ---------- Divider ---------- */
.soft-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    margin: 1.4rem 0;
    border: none;
}
</style>
""", unsafe_allow_html=True)


def empty_state(icon_name: str, title: str, subtitle: str, color: str = "#C9C4F0"):
    st.markdown(f"""
    <div class="empty-state">
        <span class="icon-wrap">{icon_svg(icon_name, 26, color)}</span>
        <h3>{title}</h3>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


# ===========================================================
# HERO HEADER
# ===========================================================
st.markdown(f"""
<div class="hero">
    <span class="hero-badge">{icon_svg('sparkles', 14, '#C9C4F0')}Powered by Groq + LangChain</span>
    <p class="hero-title">AI Data Analyst Agent</p>
    <p class="hero-sub">Upload dataset kamu, lalu ngobrol langsung dengannya — minta insight, ringkasan,
    atau visualisasi tanpa nulis satu baris kode pun.</p>
</div>
""", unsafe_allow_html=True)

# ===========================================================
# SESSION STATE
# ===========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===========================================================
# SIDEBAR
# ===========================================================
# Sidebar panel
with st.sidebar:
    st.markdown(f'<p class="sidebar-title">{icon_label("settings", "Konfigurasi")}</p>', unsafe_allow_html=True)
    env_api_key = os.getenv("GROQ_API_KEY")
    if env_api_key:
        groq_api_key = env_api_key
        st.markdown('<p class="sidebar-caption" style="color:#10B981;">✅ API Key otomatis terdeteksi dari sistem.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="sidebar-caption">Masukkan API Key untuk mengaktifkan agent.</p>', unsafe_allow_html=True)
        groq_api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")

    st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)

    st.markdown(f'<p class="sidebar-title">{icon_label("lightbulb", "Contoh Pertanyaan")}</p>', unsafe_allow_html=True)
    example_prompts = [
        "Ringkas dataset ini dalam 3 poin",
        "Buatkan grafik distribusi kolom numerik",
        "Kolom mana yang paling banyak missing value?",
        "Tunjukkan korelasi antar variabel",
    ]
    for p in example_prompts:
        st.markdown(f"<div style='color:#B9B3E8; font-size:0.83rem; padding:4px 0;'>• {p}</div>", unsafe_allow_html=True)

    st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)
    if st.session_state.messages:
        if st.button("Hapus Riwayat Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ===========================================================
# FILE UPLOAD
# ===========================================================
st.markdown(f'<p class="upload-label">{icon_label("upload", "Upload file CSV kamu di sini", 16, "#EDEBF7")}</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    #Overview metrics
    n_missing = int(df.isna().sum().sum())
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-pill"><div class="label">Baris</div><div class="value">{df.shape[0]:,}</div></div>
        <div class="metric-pill"><div class="label">Kolom</div><div class="value">{df.shape[1]:,}</div></div>
        <div class="metric-pill"><div class="label">Missing Values</div><div class="value">{n_missing:,}</div></div>
        <div class="metric-pill"><div class="label">Ukuran</div><div class="value">{uploaded_file.size/1024:.1f} KB</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<p class="preview-label">{icon_label("eye", "Lihat Preview Data", 15, "#EDEBF7")}</p>', unsafe_allow_html=True)
    with st.expander("Preview Data", expanded=True):
        st.dataframe(df.head(10), use_container_width=True)

    st.markdown('<hr class="soft-divider">', unsafe_allow_html=True)

    if not groq_api_key:
        empty_state("key", "API Key belum diisi", "Masukkan Groq API Key di sidebar untuk mulai ngobrol dengan datamu.")
        st.stop()
    # -------------------------------------------------------
    # RIWAYAT CHAT LAMA
    # -------------------------------------------------------
    # Chat history
    if not st.session_state.messages:
        # Auto-EDA
        with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
            with st.spinner("Menganalisis pola data otomatis..."):
                agent = create_agent(df, groq_api_key)
                try:
                    eda_prompt = (
                        "Berikan ringkasan eksekutif super singkat (maksimal 3 poin utama) "
                        "mengenai dataset ini. Sebutkan insight menarik, tren, atau anomali jika ada. "
                        "Hanya gunakan bahasa Indonesia santai tapi profesional. Jangan tulis kode apapun."
                    )
                    result = agent.invoke({"input": eda_prompt})
                    
                    # Save intro
                    intro_text = f"👋 Halo! Aku sudah membaca datamu. Berikut *insight* kilat yang kutemukan:\n\n{result['output']}\n\nAda bagian yang mau kita gali lebih dalam atau divisualisasikan?"
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": intro_text,
                        "is_image": False,
                        "is_file": False
                    })
                    st.rerun()
                    
                except Exception:
                    # Fallback empty
                    empty_state("chat", "Siap berdiskusi!", "Tanya sesuatu tentang datamu di kolom chat bawah.")
    else:
        # Load messages
        for i, msg in enumerate(st.session_state.messages):
            avatar = USER_AVATAR if msg["role"] == "user" else ASSISTANT_AVATAR
            with st.chat_message(msg["role"], avatar=avatar):
                if msg.get("is_image"):
                    st.image(msg["content"])
                elif msg.get("is_file"):
                    st.markdown(msg["content"])
                    st.download_button(
                        label="⬇️ Download Data Bersih (CSV)",
                        data=msg["file_bytes"],
                        file_name="cleaned_dataset.csv",
                        mime="text/csv",
                        key=f"dl_btn_{i}"
                    )
                else:
                    st.markdown(msg["content"])

    # -------------------------------------------------------
    # INPUT BARU
    # -------------------------------------------------------
    query = st.chat_input("Tanya sesuatu tentang data ini...")

    if query:
        st.session_state.messages.append({"role": "user", "content": query, "is_image": False})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(query)

        with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
            with st.spinner("Menganalisis data..."):
                agent = create_agent(df, groq_api_key)
                try:
                    chat_history = "\n".join(
                        [f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:-1] if not m.get("is_image") and not m.get("is_file")]
                    )

                    # INI DIA INSTRUKSI SAKTINYA KITA UPGRADE
                    secret_prompt = (
                        "\n\nATURAN SISTEM SUPER KETAT:\n"
                        "1. Jika membuat grafik, WAJIB simpan dengan plt.savefig('temp_chart.png'). Dilarang pakai plt.show().\n"
                        "2. Jika user meminta membersihkan, menghapus missing values, atau memodifikasi data, kamu WAJIB menyimpan dataframe hasil akhirnya menjadi CSV dengan kode: df.to_csv('temp_cleaned.csv', index=False)."
                    )

                    contextual_query = (
                        f"Riwayat chat:\n{chat_history}\n\nPertanyaan: {query}{secret_prompt}"
                        if chat_history else query + secret_prompt
                    )

                    result = agent.invoke({"input": contextual_query})
                    
                    # Cek apakah AI menghasilkan file CSV (Data Bersih)
                    if os.path.exists("temp_cleaned.csv"):
                        with open("temp_cleaned.csv", "rb") as f:
                            csv_bytes = f.read()
                        
                        st.markdown(result["output"])
                        st.download_button(
                            label="⬇️ Download Data Bersih (CSV)",
                            data=csv_bytes,
                            file_name="cleaned_dataset.csv",
                            mime="text/csv",
                            key=f"dl_btn_new_{len(st.session_state.messages)}"
                        )
                        
                        # Simpan ke memori sebagai 'is_file'
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": result["output"], 
                            "is_image": False,
                            "is_file": True,
                            "file_bytes": csv_bytes
                        })
                        
                        os.remove("temp_cleaned.csv") 
                        
                    # Cek apakah AI menghasilkan Gambar
                    elif os.path.exists("temp_chart.png"):
                        with open("temp_chart.png", "rb") as f:
                            img_bytes = f.read()
                            
                        st.markdown(result["output"])
                        st.image(img_bytes)
                        
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": result["output"], 
                            "is_image": False
                        })
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": img_bytes, 
                            "is_image": True,
                            "is_file": False
                        })
                        
                        os.remove("temp_chart.png")
                        
                    # Kalau cuma chat biasa
                    else:
                        st.markdown(result["output"])
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": result["output"], 
                            "is_image": False,
                            "is_file": False
                        })

                except Exception as e:
                    st.error(f"Error: {e}")

else:
    empty_state("bar-chart", "Belum ada file yang diupload", "Upload file CSV di atas untuk mulai eksplorasi data dengan bantuan AI.")
