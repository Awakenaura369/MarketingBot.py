import streamlit as st
from groq import Groq

# 1. إعدادات الواجهة الاحترافية
st.set_page_config(page_title="Global All-in-One Beast v1.4", page_icon="👑", layout="wide")

def get_config(key):
    return st.secrets.get(key)

# 🧠 محرك الذكاء الشامل (Groq Llama 3.3)
def unleash_the_beast(keyword, title, p_link):
    client = Groq(api_key=get_config("GROQ_API_KEY"))
    
    # برومبت يجمع كل المهام في طلب واحد لتوفير السرعة
    main_prompt = f"""
    You are a master of Tier-1 Affiliate Marketing and SEO. Execute these 3 tasks for:
    Keyword: {keyword}
    Title: {title}
    Link: {p_link}

    TASK 1: Write a 1200-word high-converting SEO article in Perfect English. Include psychology of sales, human-touch, and 2026 trends. Use HTML tags.
    TASK 2: Generate 5 high-traffic 'Trending Keywords' related to this niche.
    TASK 3: Generate a professional AI Image Prompt for the article's main banner.
    
    Format the output as follows:
    [KEYWORDS]...[/KEYWORDS]
    [IMAGE_PROMPT]...[/IMAGE_PROMPT]
    [ARTICLE_HTML]...[/ARTICLE_HTML]
    """
    
    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[{"role": "user", "content": main_prompt}]
    )
    return chat_completion.choices[0].message.content

# --- الواجهة ---
st.title("👑 Global All-in-One Beast v1.4")
st.write("Content, Keywords, & Image Prompts in a Single Click.")

col1, col2 = st.columns([2, 1])

with col1:
    keyword = st.text_input("🔑 Main Keyword", value="Financial Freedom")
    blog_title = st.text_input("📝 English Title", value="The Hidden Path to Wealth in 2026")
    p_link = st.text_input("🔗 Affiliate Link", value="https://go.hotmart.com/L103130074K")

with col2:
    st.info("✨ This version handles SEO Research + Content + Visual Ideas.")

if st.button("🚀 UNLEASH THE BEAST (All-in-One)"):
    if keyword and blog_title:
        with st.spinner("The Beast is researching and writing everything for you..."):
            try:
                raw_result = unleash_the_beast(keyword, blog_title, p_link)
                st.success("✅ Masterpiece Ready!")
                
                # تقطيع النتائج (Parsing)
                keywords_part = raw_result.split("[KEYWORDS]")[1].split("[/KEYWORDS]")[0].strip()
                image_prompt_part = raw_result.split("[IMAGE_PROMPT]")[1].split("[/IMAGE_PROMPT]")[0].strip()
                article_html_part = raw_result.split("[ARTICLE_HTML]")[1].split("[/ARTICLE_HTML]")[0].strip()
                
                # عرض النتائج في تابات منظمة
                t1, t2, t3 = st.tabs(["📄 HTML Article", "📸 Image Prompt", "📈 Trending Keywords"])
                
                with t1:
                    st.code(article_html_part, language="html")
                    st.markdown("### Live Preview")
                    st.markdown(article_html_part, unsafe_allow_html=True)
                
                with t2:
                    st.warning("Use this prompt in Leonardo.ai or Midjourney:")
                    st.write(image_prompt_part)
                
                with t3:
                    st.success("Add these tags to your Blogger post:")
                    st.write(keywords_part)
                    
            except Exception as e:
                st.error("Error splitting results. Try generating again.")
                st.write(raw_result)

st.sidebar.markdown("---")
st.sidebar.write("🛡️ **System:** All-in-One Groq Mode")
