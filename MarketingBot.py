import streamlit as st
from groq import Groq
import os

# ================== UI Setup ==================

st.set_page_config(page_title="Marketing Beast AI v3.5", page_icon="⚡", layout="wide")

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
    api_key = get_config("GROQ_API_KEY") #
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
    st.title("🪝 Facebook Sniper: Full Ad Report") #
    st.write("Generate 5 complete Viral Ads (Hook + Ad Copy + Image Prompt) with one click.")
    
    topic = st.text_input("Enter your product or niche focus", placeholder="e.g., Orthopedic Neck Pillow")
    
    if st.button("Generate Full Sniper Report 🚀"):
        if topic:
            # البرومبت اللي كيجمع كلشي فـ تقرير واحد
            sniper_prompt = f"""
            Task: Generate a FULL Ad Report for 5 high-converting Facebook Ads.
            Product/Topic: {topic}
            Style: {selected_style}
            
            For EACH of the 5 ads, follow this EXACT structure:
            1. [AD NUMBER]
            2. [HOOK]: A scroll-stopping, aggressive opening line.
            3. [AD COPY]: Persuasive body text focusing on benefits and pain points.
            4. [IMAGE PROMPT]: A detailed description for an AI image generator (like Midjourney) reflecting '{selected_emotion}' emotion.
            5. [CTA]: A strong call to action.
            
            Language: English. Focus on conversion and urgency.
            """
            
            with st.spinner("Calculating viral trajectories..."):
                report_content = generate_groq_content(sniper_prompt) #
            
            st.divider()
            st.markdown("### 📋 Final Report")
            
            # عرض التقرير فـ Text Area باش يقدر ينسخو كامل
            st.text_area("Your 5 Ads Report:", value=report_content, height=450)
            
            # زر النسخ التلقائي للتقرير كامل (Streamlit Native Feature)
            st.copy_to_clipboard(report_content, before_text="Copy Full Report to Clipboard 📋", after_text="Report Copied! ✅")
            
            st.success("Report generated! Use the button above to copy everything to your clipboard.")
        else:
            st.warning("Please enter a topic or niche focus first!")
