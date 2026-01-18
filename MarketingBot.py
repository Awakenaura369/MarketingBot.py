import streamlit as st
from groq import Groq

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marketing Beast AI", page_icon="🦁", layout="wide")

# --- التأكد من الساروت في Secrets ---
try:
    # كايجبد الساروت من Streamlit Secrets
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("❌ GROQ_API_KEY missing! Please add it to Streamlit Secrets.")
    st.stop()

# إطلاق محرك Groq
client = Groq(api_key=api_key)

# --- الدوال البرمجية (Functions) ---

def generate_sniper_content(product_name, target_audience, selected_style):
    """دالة توليد إعلانات فيسبوك Sniper"""
    prompt = f"""
    You are an expert Facebook Ads Copywriter. 
    Create 5 high-converting Facebook Ads for: {product_name}.
    Target Audience: {target_audience}
    Writing Style: {selected_style}
    
    Each ad must have:
    1. A Scroll-Stopping Hook (Social Media Hook Generator)
    2. Engaging Body Text
    3. Strong Call to Action (CTA)
    4. Suggested Emoji usage
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a marketing beast specialized in viral sales copy."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error in Groq API: {str(e)}"

# --- واجهة المستخدم (UI) ---

st.title("🦁 Marketing Beast AI v3.0")
st.markdown("---")

# إنشاء التابات كما طلبت
tab1, tab2 = st.tabs(["🚀 Main Dashboard", "🎯 Facebook Sniper"])

with tab1:
    st.header("Main Marketing Tools")
    st.info("Welcome back! Use the Facebook Sniper tab for high-converting ads.")
    st.write("Current Engine: **Groq AI (Fast Mode)**")

with tab2:
    st.header("🎯 Facebook Sniper Mode")
    st.subheader("Social Media Hook & Ad Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product = st.text_input("Product/Service Name:", placeholder="e.g., Luxury Watches")
        audience = st.text_input("Target Audience:", placeholder="e.g., Entrepreneurs 25-45")
    
    with col2:
        style = st.selectbox("Copywriting Style:", [
            "Aggressive & Direct", 
            "Emotional Storytelling", 
            "Question-based (Curiosity)", 
            "Professional & Trustworthy",
            "Urgency/Scarcity"
        ])
        
    if st.button("🎯 Launch Sniper (Generate 5 Ads)"):
        if product and audience:
            with st.spinner("Sniper is aiming... Generating viral hooks and copy..."):
                results = generate_sniper_content(product, audience, style)
                st.markdown("---")
                st.markdown(results)
                st.balloons()
        else:
            st.warning("⚠️ Please fill in both Product Name and Target Audience.")

# --- Footer ---
st.markdown("---")
st.caption("Powered by Groq AI Engine | Marketing Beast AI 2026")
