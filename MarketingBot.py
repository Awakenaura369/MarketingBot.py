import streamlit as st
from groq import Groq
import os
import requests
from bs4 import BeautifulSoup

# 1. إعدادات الواجهة والديزاين (Professional SaaS Look)
st.set_page_config(page_title="Marketing Beast AI v2.0", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    
    /* Input Fields Styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: #1e293b !important; color: white !important;
        border: 1px solid #334155 !important; border-radius: 10px !important;
    }
    
    /* Buttons Styling */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white; border: none; padding: 12px 24px; border-radius: 10px;
        font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4); }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #334155; }
    
    /* Result Box Styling */
    .content-box {
        background-color: #1e293b; padding: 20px; border-radius: 15px;
        border: 1px solid #3b82f6; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الدوال الأساسية (The Logic)
def get_config(key):
    if key in st.secrets: return st.secrets[key]
    return os.environ.get(key)

NICHES = {
    "Spirituality & Awareness": "Focus on vibrations, manifestation, and emotional healing.",
    "Make Money Online / Affiliate": "Focus on passive income, financial freedom, and urgency.",
    "Health & Fitness": "Focus on body transformation, energy, and self-confidence.",
    "Relationships & Dating": "Focus on attraction, psychological connection, and confidence.",
    "Tech & AI Tools": "Focus on efficiency, future-proofing, and saving time."
}

def fetch_trends():
    try:
        url = "https://trends.google.com/trending/rss?geo=US"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'xml')
        titles = [item.title.text for item in soup.find_all('item')[:10]]
        titles_str = ", ".join(titles)
        
        client = Groq(api_key=get_config("GROQ_API_KEY"))
        prompt = f"Analyze these global trends: {titles_str}. Suggest top 3 hot niches for digital products and a viral hook for each. Be concise."
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except:
        return "⚠️ Couldn't fetch live trends. Use evergreen niches like Wealth or Spirit."

def generate_marketing_copy(niche, p_name, p_desc, p_pain, p_link, platform):
    client = Groq(api_key=get_config("GROQ_API_KEY"))
    niche_focus = NICHES.get(niche, "")
    
    system_prompt = f"You are a world-class Marketing Copywriter expert in {niche}. Style: {niche_focus}. Language: English."
    user_prompt = f"""
    Create a viral {platform} post for:
    Product: {p_name}
    Benefits: {p_desc}
    Customer Pain: {p_pain}
    Link: {p_link}
    
    Include:
    1. Attention-grabbing headline.
    2. Story/Problem section.
    3. Transformation/Solution.
    4. Call to Action (CTA) with the link integrated naturally.
    5. Visual/Image idea.
    6. 10 Trending hashtags.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.8
    )
    return completion.choices[0].message.content

# 3. واجهة المستخدم (The Interface)
st.title("⚡ The Marketing Beast v2.0")
st.caption("Your Ultimate Digital Marketing Dashboard for Hotmart & Beyond")

with st.sidebar:
    st.header("🎯 Strategy Center")
    selected_niche = st.selectbox("Select Niche", list(NICHES.keys()))
    platform = st.selectbox("Target Platform", ["Facebook Ad", "Instagram Post", "Twitter/X Thread", "TikTok Script", "Email Blast"])
    st.markdown("---")
    st.header("🔎 Trend Hunter")
    if st.button("Find Trending Niches"):
        with st.spinner("Scanning Google Trends..."):
            report = fetch_trends()
            st.info(report)

# Main Inputs
col1, col2 = st.columns(2)
with col1:
    p_name = st.text_input("💎 Product Name", placeholder="e.g. 15-Minute Manifestation")
with col2:
    p_link = st.text_input("🔗 Affiliate/Product Link", placeholder="https://hotmart.com/...")

p_pain = st.text_input("💔 Customer Pain Point", placeholder="e.g. Stressed, feeling stuck, low energy")
p_desc = st.text_area("🌟 Key Benefits / Transformation", placeholder="What will the customer get?", height=100)

st.markdown("---")

if st.button("🚀 UNLEASH THE BEAST (Generate Content)"):
    if p_name and p_desc and p_link:
        with st.spinner("The Beast is crafting your content..."):
            result = generate_marketing_copy(selected_niche, p_name, p_desc, p_pain, p_link, platform)
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.markdown("### 🔥 Your High-Converting Content:")
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Marketing Copy",
                data=result,
                file_name=f"{p_name}_marketing.txt",
                mime="text/plain"
            )
            st.balloons()
    else:
        st.error("Please fill in: Product Name, Benefits, and Link!")

st.markdown("---")
st.caption("Built for Personal Use | Groq AI Engine 2026")
