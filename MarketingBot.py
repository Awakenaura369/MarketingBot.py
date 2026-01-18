import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="Marketing Beast AI", page_icon="🦁")

# جلب الساروت من Secrets
try:
    # هادي هي السمية اللي خصك تحط في Streamlit Secrets
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("❌ GROQ_API_KEY is missing in Streamlit Secrets!")
    st.stop()

# إطلاق Groq Client
client = Groq(api_key=api_key)

def generate_sniper_ads(product_name, audience, style):
    """دالة توليد الإعلانات والـ Hooks"""
    prompt = f"""
    Act as an expert Facebook Ads Copywriter.
    Create 5 viral Facebook Ads for: {product_name}
    Target Audience: {audience}
    Tone: {style}
    
    Each ad must include:
    - A viral Social Media Hook
    - Engaging body text
    - Strong Call to Action (CTA)
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional marketing bot."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error in Groq API: {str(e)}"

# واجهة المستخدم
st.title("🦁 Marketing Beast AI")
tab1, tab2 = st.tabs(["🚀 Dashboard", "🎯 Facebook Sniper"])

with tab1:
    st.write("Main Dashboard - Ready to scale!")
    st.write("Engine: **Groq AI**")

with tab2:
    st.header("🎯 Facebook Sniper Mode")
    st.subheader("Social Media Hook Generator")
    
    p_name = st.text_input("Product/Service Name:")
    p_audience = st.text_input("Target Audience:")
    p_style = st.selectbox("Style:", ["Aggressive", "Emotional", "Storytelling"])
    
    if st.button("🚀 Launch Sniper"):
        if p_name and p_audience:
            with st.spinner("Sniper is aiming..."):
                output = generate_sniper_ads(p_name, p_audience, p_style)
                st.markdown(output)
        else:
            st.warning("Please fill all fields.")

st.markdown("---")
st.caption("Powered by Groq | Marketing Beast AI 2026")
