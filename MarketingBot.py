import streamlit as st
from groq import Groq
import os
import requests
from bs4 import BeautifulSoup

# 1. إعدادات الواجهة والديزاين (v2.0 - المستقرة)
st.set_page_config(page_title="Marketing Beast AI v2.0", page_icon="⚡", layout="wide")

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
    .content-box {
        background-color: #1e293b; padding: 20px; border-radius: 15px;
        border: 1px solid #3b82f6; margin-top: 20px;
    }
    .image-prompt-box {
        background-color: #0f172a; padding: 15px; border-radius: 10px;
        border: 1px dotted #00ffcc; margin-top: 10px; font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الدوال الأساسية
def get_config(key):
    if key in st.secrets: return st.secrets[key]
    return os.environ.get(key)

NICHES = {
    "Spirituality & Awareness": "Vibrations, manifestation, and emotional healing.",
    "Make Money Online / Affiliate": "Passive income, financial freedom, and urgency.",
    "Health & Fitness": "Body transformation, energy, and self-confidence.",
    "Relationships & Dating": "Attraction, psychological connection, and confidence.",
    "Tech & AI Tools": "Efficiency, future-proofing, and saving time."
}

# --- دالة توليد المحتوى ووصف الصور ---
def generate_all(niche, p_name, p_desc, p_pain, p_link, platform):
    client = Groq(api_key=get_config("GROQ_API_KEY"))
    niche_focus = NICHES.get(niche, "")
    
    # برومبت مركب باش يخرج المحتوى والوصف فدقة وحدة
    prompt = f"""
    You are a Master Marketer. 
    Task 1: Write a high-converting {platform} post for '{p_name}' (Benefits: {p_desc}, Pain: {p_pain}, Link: {p_link}).
    Task 2: Create a 'Masterpiece Image Prompt' for AI (like Midjourney). The image should be psychological, eye-catching, and represent the niche {niche}.
    
    Format:
    ---COPY---
    [Your Post Content]
    ---IMAGE---
    [Detailed Visual AI Prompt]
    """
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": f"Expert in {niche_focus}"}, {"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def fetch_trends():
    try:
        url = "https://trends.google.com/trending/rss?geo=US"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'xml')
        titles = [item.title.text for item in soup.find_all('item')[:10]]
        api_key = get_config("GROQ_API_KEY")
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"Analyze trends: {', '.join(titles)}. Top 3 niches & viral hooks."}]
        )
        return completion.choices[0].message.content
    except: return "⚠️ Trends offline."

# 3. الواجهة
st.title("⚡ The Marketing Beast v2.0")
st.caption("AI-Powered Content & Visual Strategy")

with st.sidebar:
    st.header("🎯 Strategy Center")
    selected_niche = st.selectbox("Select Niche", list(NICHES.keys()))
    platform = st.selectbox("Target Platform", ["Facebook Ad", "Instagram Post", "TikTok Script", "Email Blast"])
    st.markdown("---")
    if st.button("Find Trending Niches"):
        with st.spinner("Scanning..."): st.info(fetch_trends())

col1, col2 = st.columns(2)
with col1: p_name = st.text_input("💎 Product Name")
with col2: p_link = st.text_input("🔗 Affiliate Link")

p_pain = st.text_input("💔 Customer Pain Point")
p_desc = st.text_area("🌟 Main Benefits", height=100)

if st.button("🚀 UNLEASH THE BEAST"):
    if p_name and p_desc and p_link:
        with st.spinner("Generating Marketing Arsenal..."):
            full_result = generate_all(selected_niche, p_name, p_desc, p_pain, p_link, platform)
            
            # تقسيم النتيجة لعرضها بشكل منظم
            copy_part = full_result.split("---IMAGE---")[0].replace("---COPY---", "")
            image_part = full_result.split("---IMAGE---")[1] if "---IMAGE---" in full_result else "No prompt generated."

            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown("### 🔥 Your Sales Copy:")
            st.markdown(copy_part)
            st.markdown("---")
            st.markdown("### 🎨 AI Image Generator Prompt:")
            st.info(image_part)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.balloons()
    else:
        st.error("Fill all fields first!")
