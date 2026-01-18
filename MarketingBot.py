import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="Marketing Beast AI", page_icon="🦁", layout="wide")

# جلب الساروت
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("❌ API Key Missing")
    st.stop()

client = Groq(api_key=api_key)

def generate_aggressive_fiverr_ads(product, audience, style):
    # برومبت يركز على الشراسة التسويقية والـ Luxury Style
    prompt = f"""
    You are a high-ticket Direct Response Copywriter. 
    Task: Create 5 AGGRESSIVE and LUXURY style Facebook Ads for '{product}'.
    Target Audience: {audience}
    Strategy/Style: {style}

    DELIVERY RULES:
    1. THE HOOK: Must be a viral, pattern-interrupting statement.
    2. IMAGE PROMPT: High-end, luxury, cinematic visual description.
    3. AD COPY: Persuasive, elite, and focuses on deep pain points or status.
    4. NO MARKDOWN: Do NOT use asterisks (**) or hashes (#). Use plain text only.

    FORMAT:
    AD SET [Number]
    HOOK: [Text]
    IMAGE PROMPT: [Text]
    AD COPY: [Text]
    CTA: [Text]
    -------------------------------------------
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an aggressive marketing beast. Your copy is elite, expensive, and high-converting. No fluff. No asterisks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9 
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- الواجهة ---
st.title("🦁 Marketing Beast AI (Elite Sniper Edition)")

tab1, tab2 = st.tabs(["🚀 Dashboard", "🎯 Facebook Sniper"])

with tab2:
    st.header("🎯 Facebook Sniper (Aggressive & Luxury)")
    
    col1, col2 = st.columns(2)
    with col1:
        prod = st.text_input("Product Name:", placeholder="e.g., Luxy Watch")
        aud = st.text_input("Audience:", placeholder="e.g., General")
    with col2:
        # رجعنا ليك الخيارات اللي كنتي كترتاح فيها
        stl = st.selectbox("Copywriting Style:", [
            "Aggressive & Direct", 
            "Luxury & Elite", 
            "Problem-Solution", 
            "Storytelling"
        ])

    if st.button("🚀 Launch Sniper Attack"):
        if prod and aud:
            with st.spinner("Sniper is locking on target..."):
                results = generate_aggressive_fiverr_ads(prod, aud, stl)
                st.session_state['elite_ads'] = results
                
                # عرض النص بطريقة بروفيسيونال
                st.text_area("Your Clean & Aggressive Delivery:", results, height=500)
                
                st.download_button(
                    label="📥 Download Elite Ads (.txt)",
                    data=results,
                    file_name=f"Elite_Ads_{prod}.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please enter product and audience.")

# زر احتياطي
if 'elite_ads' in st.session_state:
    st.sidebar.download_button("📥 Re-download Last Ads", st.session_state['elite_ads'], "ads.txt")
