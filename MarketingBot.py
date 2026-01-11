import streamlit as st
import google.generativeai as genai
from groq import Groq

# 1. إعدادات بسيطة وانيقة
st.set_page_config(page_title="The Marketing Beast v4.1", page_icon="👹", layout="wide")

def get_config(key):
    try:
        return st.secrets[key]
    except:
        return None

# 🧠 محرك الكتابة البشرية (Gemini)
def generate_article(keyword, title, p_link):
    genai.configure(api_key=get_config("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Write a 1500-word SEO article in ARABIC about '{keyword}' with title '{title}'.
    Target audience: People interested in spiritual wealth and freedom.
    Include this affiliate link naturally: {p_link}
    
    FORMATTING RULES (HTML):
    - Use <h2> and <h3> for subheadings.
    - Write in a storytelling, human, and persuasive tone.
    - Add a 'Table of Contents' at the start.
    - Place this placeholder for the image: <div style='background:#eee; padding:20px; text-align:center; border-radius:10px;'>📸 [PLACE IMAGE HERE: {keyword}]</div>
    - End with a strong Call to Action.
    - Output ONLY HTML code.
    """
    response = model.generate_content(prompt)
    return response.text

# 🎨 محرك وصف الصور (Groq)
def generate_img_prompt(keyword):
    client = Groq(api_key=get_config("GROQ_API_KEY"))
    prompt = f"Create a high-quality AI image prompt for {keyword}. Cinematic, 8k, professional blog style."
    res = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content

# --- الواجهة ---
st.title("👹 The Marketing Beast (Copy/Paste Edition)")
st.write("Keep it simple, keep it fast. Generate, Copy, and Dominate.")

col1, col2 = st.columns(2)
with col1:
    keyword = st.text_input("🔑 Keyword")
    title = st.text_input("📝 Article Title")
with col2:
    p_link = st.text_input("🔗 Affiliate Link", value="https://hotmart.com/your-link")

if st.button("🚜 Generate Masterpiece"):
    if not get_config("GOOGLE_API_KEY"):
        st.error("❌ GOOGLE_API_KEY is missing in Secrets!")
    else:
        with st.spinner("Writing your article..."):
            # توليد المقال
            article = generate_article(keyword, title, p_link)
            # توليد وصف الصورة
            img_p = generate_img_prompt(keyword)
            
            st.session_state['article'] = article
            st.session_state['img_p'] = img_p

if 'article' in st.session_state:
    tab1, tab2, tab3 = st.tabs(["📄 HTML Code", "👁️ Preview", "📸 Image Prompt"])
    
    with tab1:
        st.code(st.session_state['article'], language="html")
        st.button("📋 Copy Code (Manually)")
    
    with tab2:
        st.markdown(st.session_state['article'], unsafe_allow_html=True)
        
    with t3:
        st.info(st.session_state['img_p'])
