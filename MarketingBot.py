import streamlit as st
from groq import Groq

st.set_page_config(page_title="Marketing Beast AI", page_icon="🦁", layout="wide")

try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("❌ API Key Missing")
    st.stop()

client = Groq(api_key=api_key)

def generate_killer_ads(product, audience, style):
    # Prompt هاد المرة فيه خطة هجومية إعلانية
    prompt = f"""
    You are a world-class Direct Response Copywriter (think David Ogilvy meets modern FB Ads experts).
    Deliver 5 VIRAL Ad Sets for: '{product}' targeting '{audience}'.
    Style focus: {style}
    
    CRITICAL INSTRUCTIONS:
    1. THE HOOK: Must be a pattern-interrupter. Use bold claims, shocking statistics, or relatable pain points.
    2. THE BODY: Use the AIDA (Attention, Interest, Desire, Action) framework. 
    3. THE IMAGE PROMPT: Must be cinematic, high-quality, and describe lighting/composition for a professional look.
    
    FORMAT FOR EACH AD:
    ---
    ### 🎯 AD SET # [Number]
    
    🪝 **THE VIRAL HOOK:**
    [Killer Hook Here]
    
    📖 **PERSUASIVE AD COPY:**
    [Engaging Story/Benefit-driven copy]
    
    🖼️ **AI IMAGE GENERATOR PROMPT:**
    [Detailed prompt for Midjourney/DALL-E]
    
    🔘 **CALL TO ACTION:**
    [Punchy CTA]
    ---
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an aggressive sales-driven AI. You don't write generic fluff. You write copy that prints money."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9 # زدنا فـ الإبداع باش ما يجيش داكشي ممل
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

st.title("🦁 Marketing Beast AI V4.0 (Money-Maker)")

tab1, tab2 = st.tabs(["🚀 Dashboard", "🎯 Facebook Sniper"])

with tab2:
    st.header("🎯 Facebook Sniper (Advanced Mode)")
    col1, col2 = st.columns(2)
    with col1:
        prod = st.text_input("Product/Service:", placeholder="e.g., Magnetic Eyelashes")
        aud = st.text_input("Audience:", placeholder="e.g., Busy Moms 25-40")
    with col2:
        stl = st.selectbox("Ad Strategy:", ["Fear of Missing Out", "Problem-Agitate-Solve", "Celebrity Status", "Pure Logic"])

    if st.button("🚀 Launch Sniper Attack"):
        if prod and aud:
            with st.spinner("Analyzing market... Writing viral copy..."):
                results = generate_killer_ads(prod, aud, stl)
                st.session_state['final_ads'] = results
                st.markdown(results)
                
                st.download_button(
                    label="📥 Download This Delivery (.txt)",
                    data=results,
                    file_name=f"Sniper_Ads_{prod}.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Enter product and audience details first.")
