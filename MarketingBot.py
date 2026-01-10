import streamlit as st
from groq import Groq
import os
import requests
from bs4 import BeautifulSoup

# 1. إعدادات الواجهة
st.set_page_config(page_title="The Marketing Beast AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    .stDownloadButton>button { width: 100%; background-color: #00ffcc; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ The Marketing Beast: Multi-Niche Engine")
st.markdown("---")

def get_config(key):
    if key in st.secrets: return st.secrets[key]
    return os.environ.get(key)

NICHES = {
    "Spirituality & Awareness": "Vibrations, alignment, manifestation, and subconscious mind.",
    "Make Money Online / Affiliate": "Financial freedom, passive income, and urgency.",
    "Health & Fitness": "Body transformation, confidence, and energy.",
    "Relationships & Dating": "Connection, psychology, and attraction.",
    "Tech & AI Tools": "Efficiency, future-proofing, and cutting-edge tech."
}

# --- وظيفة توليد المحتوى ---
def generate_content(niche, p_name, p_desc, p_pain, p_link, platform):
    api_key = get_config("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    
    system_msg = f"You are a Master Copywriter expert in {niche}. Language: English."
    
    user_msg = f"""
    Product Name: {p_name}
    Benefits: {p_desc}
    Pain Point: {p_pain}
    Affiliate Link: {p_link}
    Platform: {platform}
    
    Task: Write a high-converting {platform} post. 
    IMPORTANT: Naturally integrate the provided Affiliate Link into the Call to Action (CTA). 
    Make the link look like the only solution to the customer's problem.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.8
    )
    return completion.choices[0].message.content

# --- وظيفة التريندات ---
def fetch_trends():
    try:
        url = "https://trends.google.com/trending/rss?geo=US"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'xml')
        titles = [item.title.text for item in soup.find_all('item')[:10]]
        titles_str = ", ".join(titles)
        api_key = get_config("GROQ_API_KEY")
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"Analyze these trends and suggest 3 hot niches: {titles_str}"}]
        )
        return completion.choices[0].message.content
    except: return "⚠️ Trends unavailable. Stick to your core niche."

# --- واجهة المستخدم ---
with st.sidebar:
    st.header("🎯 Target Strategy")
    selected_niche = st.selectbox("Select Niche", list(NICHES.keys()))
    platform = st.selectbox("Target Platform", ["Facebook Ad", "Instagram Post", "Twitter/X Thread", "TikTok Script", "Email Blast"])
    st.markdown("---")
    if st.button("🔎 Scan Global Trends"):
        with st.spinner("Hunting..."):
            st.info(fetch_trends())

# مدخلات المنتج
col1, col2 = st.columns(2)
with col1:
    p_name = st.text_input("💎 Product Name")
with col2:
    p_link = st.text_input("🔗 Your Affiliate Link", placeholder="https://hotmart.com/your-link")

p_pain = st.text_input("💔 Customer Pain Point (e.g. Broke, stressed, lonely)")
p_desc = st.text_area("🌟 Main Transformation / Benefits", height=100)

if st.button("🚀 UNLEASH THE BEAST (Generate Content)"):
    if p_name and p_desc and p_link:
        with st.spinner("Crafting your viral ad..."):
            final_content = generate_content(selected_niche, p_name, p_desc, p_pain, p_link, platform)
            st.markdown("### 📄 Your Ready-to-Post Copy:")
            st.markdown(final_content)
            st.download_button("📥 Download Copy", final_content, file_name="marketing_copy.txt")
            st.balloons()
    else:
        st.error("Please fill in: Name, Benefits, and Your Link!")
