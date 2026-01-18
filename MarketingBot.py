import streamlit as st
from groq import Groq
import re

st.set_page_config(page_title="Marketing Beast AI", page_icon="🦁", layout="wide")

try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("❌ API Key Missing")
    st.stop()

client = Groq(api_key=api_key)

def clean_text(text):
    """دالة لمسح النجمات والرموز لتنظيف النص"""
    return text.replace("**", "").replace("###", "---").replace("`", "")

def generate_fiverr_pro_ads(product, audience, style):
    prompt = f"""
    Act as a Fiverr Pro Copywriter. Generate 5 high-converting Facebook Ads.
    Product: {product}
    Audience: {audience}
    Style: {style}

    For each ad, provide:
    1. VIRAL HOOK: A pattern-interrupting opening.
    2. AD COPY: Persuasive body text focusing on benefits.
    3. IMAGE PROMPT: A detailed visual description for AI/Designers.
    4. CALL TO ACTION: A punchy closing.

    IMPORTANT: Do not use markdown formatting like asterisks or bold text. Keep it professional.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a direct response marketing expert. You write clean, professional ad copy without special symbols."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- الواجهة ---
st.title("🦁 Marketing Beast (Clean Delivery Edition)")

tab1, tab2 = st.tabs(["🚀 Dashboard", "🎯 Facebook Sniper"])

with tab2:
    st.header("🎯 Facebook Sniper (Fiverr Pro)")
    col1, col2 = st.columns(2)
    with col1:
        prod = st.text_input("Product/Service Name:")
        aud = st.text_input("Target Audience:")
    with col2:
        stl = st.selectbox("Strategy:", ["Problem-Solution", "Direct Offer", "Curiosity Loop"])

    if st.button("🚀 Generate Clean Ads"):
        if prod and aud:
            with st.spinner("Creating your professional delivery..."):
                raw_results = generate_fiverr_pro_ads(prod, aud, stl)
                # تنظيف النص من النجمات
                clean_results = clean_text(raw_results)
                
                st.session_state['clean_ads'] = clean_results
                
                # عرض النتيجة منظمة
                st.text_area("Your Clean Ad Copy (Ready for Fiverr):", clean_results, height=400)
                
                st.download_button(
                    label="📥 Download Clean Text File",
                    data=clean_results,
                    file_name=f"Fiverr_Delivery_{prod}.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please fill the details.")
