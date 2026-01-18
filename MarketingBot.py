import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="Marketing Beast AI", page_icon="🦁", layout="wide")

# جلب الساروت
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("❌ API Key missing in Secrets!")
    st.stop()

client = Groq(api_key=api_key)

def generate_fiverr_style_ads(product, audience, style):
    # Prompt مطور كيركز على الـ Hooks وبرومبت الصور بحال Fiverr Gigs
    prompt = f"""
    Act as a Top-Rated Direct Response Copywriter on Fiverr. 
    Create 5 high-converting Facebook Ad Sets for: {product}.
    Target Audience: {audience}
    Tone: {style}

    For EACH ad, follow this EXACT Fiverr-Delivery format:

    ---
    ### 🎯 AD SET [NUMBER]
    
    🪝 **THE HOOK (Scroll-Stopper):**
    [Write a powerful, viral hook that addresses a pain point or curiosity immediately]

    📖 **AD COPY (The Story/Offer):**
    [Build on the hook. Use short sentences, bullet points, and high-persuasion language. Focus on benefits, not features.]

    🖼️ **IMAGE/CREATIVE PROMPT:**
    [Detailed instruction for a designer or AI image generator that matches the hook. e.g., "A high-contrast photo of..."]

    🔘 **CALL TO ACTION (CTA):**
    [Compelling CTA like "Get Yours Now 50% Off" or "Stop Wasting Money Today"]
    ---
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a world-class copywriter. Your goal is to make the user's audience stop scrolling and click."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- Interface ---
st.title("🦁 Marketing Beast AI (Fiverr Sniper Edition)")

tab1, tab2 = st.tabs(["🚀 Dashboard", "🎯 Facebook Sniper"])

with tab2:
    st.header("🎯 Facebook Sniper Mode")
    st.subheader("Fiverr-Quality Hooks & Ad Copies")
    
    c1, c2 = st.columns(2)
    with c1:
        prod = st.text_input("Product Name:", placeholder="e.g., Anti-Blue Light Glasses")
        aud = st.text_input("Target Audience:", placeholder="e.g., Gamers & Office Workers")
    with c2:
        stl = st.selectbox("Writing Style:", ["Aggressive Sales", "Storytelling", "Scientific/Logical", "Question-Based"])

    if st.button("🚀 Launch Sniper & Generate Ads"):
        if prod and aud:
            with st.spinner("Writing your Fiverr-style ads..."):
                final_results = generate_fiverr_style_ads(prod, aud, stl)
                st.session_state['fiverr_result'] = final_results
                
                st.markdown("### ✅ Your Professional Delivery:")
                st.markdown(final_results)
                
                # زر التحميل كيطلع هنا مورا النتيجة
                st.download_button(
                    label="📥 Download Fiverr-Style Delivery (.txt)",
                    data=final_results,
                    file_name=f"fiverr_ads_{prod}.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Please fill the product and audience fields.")

# زر تحميل احتياطي في الجنب
if 'fiverr_result' in st.session_state:
    st.sidebar.download_button("📥 Re-download Last Ads", st.session_state['fiverr_result'], "fiverr_ads.txt")
