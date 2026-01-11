import streamlit as st
from groq import Groq

# 1. إعدادات الواجهة
st.set_page_config(page_title="Groq Beast v1.1", page_icon="👹", layout="wide")

def get_config(key):
    return st.secrets.get(key)

# 🧠 محرك الكتابة البشرية (Groq Stable Mode)
def generate_article_with_groq(keyword, title, p_link):
    client = Groq(api_key=get_config("GROQ_API_KEY"))
    
    prompt = f"""
    Act as a professional human blogger. Write a 1000-word SEO article in ARABIC.
    Topic: {keyword}. Title: {title}.
    Affiliate Link: {p_link}
    
    INSTRUCTIONS:
    - Language: Professional and engaging Arabic.
    - Format: Use HTML tags (<h2>, <h3>, <p>, <ul>).
    - Add a placeholder for image: <img src='IMAGE_URL' style='width:100%'/>
    - Output ONLY HTML code.
    """
    
    # استخدام الموديل الأكثر استقراراً لتجنب BadRequestError
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192", 
        messages=[{"role": "user", "content": prompt}]
    )
    return chat_completion.choices[0].message.content

# --- الواجهة ---
st.title("👹 The Pure Groq Beast v1.1")
st.write("Stable & Fast. No more errors.")

keyword = st.text_input("🔑 Keyword", value="Spiritual")
title = st.text_input("📝 Title", value="💎 The Spiritual Freedom Code: Escape the Matrix")
p_link = st.text_input("🔗 Link", value="https://go.hotmart.com/L103130074K")

if st.button("🚜 Unleash Groq"):
    if keyword and title:
        with st.spinner("Groq is working..."):
            try:
                article = generate_article_with_groq(keyword, title, p_link)
                st.success("✅ Success!")
                
                t1, t2 = st.tabs(["📄 HTML Code", "👁️ Preview"])
                with t1:
                    st.code(article, language="html")
                with t2:
                    st.markdown(article, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.info("Status: Stable Mode")
