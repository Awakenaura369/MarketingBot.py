import streamlit as st
from groq import Groq
import os
import requests
from bs4 import BeautifulSoup
import json

# ================== UI Setup ==================

st.set_page_config(page_title="Marketing Beast AI v3.3", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
    background-color: #1e293b !important; color: white !important;
    border: 1px solid #334155 !important; border-radius: 10px !important;
}
.stButton>button {
    background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
    color: white; border: none; padding: 12px 24px; border-radius: 10px;
    font-weight: bold; width: 100%; transition: 0.3s;
}
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4); }
[data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #334155; }
</style>""", unsafe_allow_html=True)

# ================== Helper Functions ==================

def get_config(key):
    if key in st.secrets:
        return st.secrets[key]
    return os.environ.get(key)

NICHES = {
    "Spirituality & Awareness": "Vibrations, manifestation, and emotional healing.",
    "Make Money Online / Affiliate": "Passive income, financial freedom, and urgency.",
    "Health & Fitness": "Body transformation, energy, and self-confidence.",
    "Relationships & Dating": "Attraction, psychological connection, and confidence.",
    "Tech & AI Tools": "Efficiency, future-proofing, and saving time."
}

STYLES = ["Aggressive", "Spiritual", "Storytelling", "Direct"]
PLATFORMS = ["Facebook Ad", "Instagram Post", "TikTok Script", "Email Blast"]
EMOTIONS = ["Peace", "Power", "Mystery", "Fear"]

def generate_groq_content(prompt):
    api_key = get_config("GROQ_API_KEY")
    if not api_key:
        return "⚠️ API Key missing! Please set GROQ_API_KEY."
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ================== Sidebar ==================

with st.sidebar:
    st.header("🎯 Strategy Center")
    selected_niche = st.selectbox("Select Niche", list(NICHES.keys()))
    selected_style = st.selectbox("Select Style", STYLES)
    selected_platform = st.selectbox("Target Platform", PLATFORMS)
    selected_emotion = st.selectbox("Image Emotion", EMOTIONS)

# ================== Main Tabs ==================

tab1, tab2 = st.tabs(["🚀 Content Generator", "🎯 Facebook Sniper"])

with tab1:
    st.title("Marketing Beast Content AI")
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input("Product Name")
        p_desc = st.text_area("Benefits")
    with col2:
        p_pain = st.text_input("Pain Point")
        p_link = st.text_input("Affiliate Link")

    if st.button("Generate Ads & Image Prompt"):
        niche_focus = NICHES.get(selected_niche, "")
        prompt = f"Expert {niche_focus} Marketer. Generate 3 {selected_platform} posts ({selected_style} style) for {p_name}. Benefits: {p_desc}. Pain: {p_pain}. Link: {p_link}. Include A/B variations and an AI Image prompt for {selected_emotion}."
        result = generate_groq_content(prompt)
        st.markdown(f"### Results\n{result}")

with tab2:
    st.title("🪝 Facebook Sniper: Hook Generator")
    topic = st.text_input("Enter your post topic or niche focus")
    if st.button("Generate Viral Hooks"):
        hook_prompt = f"Generate 5 viral Facebook hooks for the topic: '{topic}'. Focus on high engagement, stopping the scroll, and curiosity. Style: {selected_style}."
        hooks = generate_groq_content(hook_prompt)
        st.markdown(f"### Viral Hooks\n{hooks}")
