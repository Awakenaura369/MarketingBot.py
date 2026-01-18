import streamlit as st
from groq import Groq

# إعداد العميل (تأكد من وضع API Key الخاص بك)
client = Groq(api_key="YOUR_GROQ_API_KEY")

def generate_sniper_content(product, niche, style):
    # الـ Prompt السنايبر: يمنع الرموز (*) ويركز على 5 إعلانات تجارية كاملة
    prompt = f"""
    You are the "Facebook Ads Sniper". Your mission is to generate 5 Viral Ads for: {product}.
    Niche: {niche}
    Tone: {style}

    RULES:
    1. Generate exactly 5 Ads.
    2. DO NOT use asterisks (*) or any markdown bold symbols.
    3. Use only plain text.
    4. For each ad, provide: HOOK, AD COPY, IMAGE PROMPT, VIDEO SCRIPT, and CTA.
    5. Separate each ad with a line of dashes: --------------------------
    6. Ignore spiritual or irrelevant content. Focus on sales and conversion.

    STRUCTURE PER AD:
    AD [Number]
    HOOK: [Scroll-stopper]
    AD COPY: [Persuasive body]
    IMAGE PROMPT: [AI Image description]
    VIDEO SCRIPT: [15-second viral script]
    CTA: [Call to Action]
    """
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="mixtral-8x7b-32768", # أو أي موديل كتستعمله فـ Groq
    )
    return chat_completion.choices[0].message.content

# --- SIDEBAR (Strategy Center) ---
st.sidebar.title("🎯 Strategy Center")
# حيدنا الروحانيات وخلينا الـ Niches التجارية اللي غتحتاج فـ Fiverr
niches = ["E-commerce", "Real Estate", "Health & Beauty", "Digital Marketing", "Local Business"]
selected_niche = st.sidebar.selectbox("Select Niche:", niches)
selected_style = st.sidebar.selectbox("Select Style:", ["Aggressive", "Professional", "Storytelling", "Urgent"])

# --- MAIN APP ---
st.title("🦁 Marketing Beast AI")
st.markdown("### Facebook Sniper Mode")

# المدخل الوحيد دبا هو Facebook Sniper (حيدنا Create Content)
product_name = st.text_input("Enter your Product or Service Name:", placeholder="e.g. Anti-Hair Loss Serum")

if st.button("🎯 Launch Sniper (Generate 5 Viral Ads)"):
    if product_name:
        with st.spinner('🎯 Sniper is targeting your audience...'):
            result = generate_sniper_content(product_name, selected_niche, selected_style)
            
            st.success("✅ 5 Viral Ads Generated Successfully!")
            # عرض النتائج فـ Text Area باش يسهل الكوبي-كولي بلا نجمات
            st.text_area("Your Ready-to-Use Content (PDF Style):", result, height=600)
            
            # زر التحميل (بسيط)
            st.download_button(
                label="📥 Download Results for PDF",
                data=result,
                file_name=f"Facebook_Sniper_{product_name}.txt",
                mime="text/plain"
            )
    else:
        st.warning("Please enter a product name first!")
