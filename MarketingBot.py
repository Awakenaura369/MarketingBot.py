import streamlit as st
import google.generativeai as genai
from groq import Groq
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json

# 1. إعدادات الواجهة
st.set_page_config(page_title="Alpha King v5.0", page_icon="👑", layout="wide")

def get_config(key):
    return st.secrets.get(key)

# 2. إعدادات OAuth2 للنشر التلقائي
CLIENT_CONFIG = {
    "web": {
        "client_id": get_config("CLIENT_ID"),
        "client_secret": get_config("CLIENT_SECRET"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

# 3. دالة النشر في بلوجر
def publish_to_blogger(title, content):
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=['https://www.googleapis.com/auth/blogger'],
        redirect_uri='urn:ietf:wg:oauth:2.0:oob' # هادي للموافقة اليدوية السريعة
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    st.write(f"🔐 [برك هنا باش تعطي التصريح للوحش]({auth_url})")
    code = st.text_input("حط الكود اللي غايعطيك جوجل هنا:")
    
    if code:
        flow.fetch_token(code=code)
        creds = flow.credentials
        service = build('blogger', 'v3', credentials=creds)
        
        body = {
            "kind": "blogger#post",
            "title": title,
            "content": content,
            "blog": {"id": get_config("BLOG_ID")}
        }
        
        posts = service.posts()
        result = posts.insert(blogId=get_config("BLOG_ID"), body=body).execute()
        return result.get('url')
    return None

# --- المحرك الرئيسي ---
st.title("👑 Alpha King v5.0: The Ultimate Marketer")

with st.sidebar:
    st.header("⚙️ Configuration")
    st.success("Groq & Gemini: Online")
    st.info(f"Blog ID: {get_config('BLOG_ID')}")

tab1, tab2 = st.tabs(["🧪 SEO Lab", "🚀 Social Engine"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input("🔑 Keyword")
        blog_title = st.text_input("📝 Title")
    with col2:
        p_link = st.text_input("🔗 Affiliate Link")
        img_url = st.text_input("🖼️ Image URL")

    if st.button("🚜 Generate Masterpiece"):
        with st.spinner("The King is writing..."):
            # محرك Gemini للكتابة البشرية
            genai.configure(api_key=get_config("GOOGLE_API_KEY"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Write a 1500-word human-style SEO article in Arabic about {keyword}. Title: {blog_title}. Link: {p_link}. Use HTML tags."
            res = model.generate_content(prompt)
            
            article = res.text
            if img_url:
                article = f"<img src='{img_url}' style='width:100%'/><br>" + article
            
            st.session_state['final_post'] = article
            st.markdown(article, unsafe_allow_html=True)

    if 'final_post' in st.session_state:
        if st.button("🚀 Publish Directly to Blogger"):
            post_url = publish_to_blogger(blog_title, st.session_state['final_post'])
            if post_url:
                st.success(f"🔥 تم النشر بنجاح! شوفو هنا: {post_url}")

# محرك Groq للسرعة (Social Media)
with tab2:
    st.write("Social Engine is ready for lightning speed!")
