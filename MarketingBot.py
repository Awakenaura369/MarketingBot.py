import streamlit as st
from groq import Groq

# 1. إعدادات الواجهة
st.set_page_config(page_title="Groq Beast v1.0", page_icon="👹", layout="wide")

def get_config(key):
    return st.secrets.get(key)

# 🧠 محرك الكتابة البشرية (Groq Power)
def generate_article_with_groq(keyword, title, p_link):
    client = Groq(api_key=get_config("GROQ_API_KEY"))
    
    # برومبت احترافي باش المقال يجي طويل وبشري
    prompt = f"""
    Act as a high-end human blogger. Write a 1200-word SEO article in ARABIC.
    Topic: {keyword}. Title: {title}.
    Affiliate Link: {p_link}
    
    INSTRUCTIONS:
    - Language: Use professional but warm Arabic.
    - Style: Start with a personal story. Use bullet points and bold text.
    - SEO: Use H2 and H3 tags.
    - Placeholder: Add <img src='PLACE_IMAGE_URL_HERE' style='width:100%'/> after the first section.
    - Format: Output ONLY valid HTML code.
    """
    
    chat_completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile", # الموديل الكبير ديالهم
        messages=[{"role": "user", "content": prompt}]
    )
    return chat_completion.choices[0].message.content

# --- الواجهة ---
st.title("👹 The Pure Groq Beast")
st.write("Speed. Simplicity. No Google Headaches.")

keyword = st.text_input("🔑 Keyword")
title = st.text_input("📝 Title")
p_link = st.text_input("🔗 Link", value="https://hotmart.com/...")

if st.button("🚜 Unleash Groq"):
    if keyword and title:
        with st.spinner("Groq is thinking at lightning speed..."):
            article = generate_article_with_groq(keyword, title, p_link)
            
            st.success("✅ Done!")
            
            t1, t2 = st.tabs(["📄 HTML Code", "👁️ Preview"])
            with t1:
                st.code(article, language="html")
            with t2:
                st.markdown(article, unsafe_allow_html=True)

st.sidebar.info("System: Pure Groq Mode ⚡")
