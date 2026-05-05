import streamlit as st
from styles import apply_styles, feature_card
from features import text_detector
from features import text_insights
from features import email_generator
from features import fact_checker
from features import image_detector

st.set_page_config(

    page_title="AI SmartSuite",

    page_icon="🤖",

    layout="wide",

    initial_sidebar_state="collapsed"

)

st.markdown("""

<style>

#MainMenu {visibility: hidden;}

header {visibility: hidden;}

footer {visibility: hidden;}

</style>

""", unsafe_allow_html=True)

# Apply styling
apply_styles()

# Sidebar navigation
with st.sidebar:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("media/logo.jpeg", width=60)
    with col2:
        st.markdown("""
            <div style="padding:8px 0 0 4px;">
                <p style="margin:0; font-size:13px; font-weight:700; color:white;">AI SmartSuite</p>
                <p style="margin:2px 0 0; font-size:11px; color:#a78bfa;">Your AI toolkit</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("<hr style='border:none; border-top:1px solid rgba(255,255,255,0.08); margin:12px 0;'>", unsafe_allow_html=True)

    # Navigation items - each is a button
    features = {
        "🔍 Text Detector": "Detect AI vs Human text",
        "🖼️ Image Detector": "Detect AI images",
        "📧 Email Generator": "Write emails fast",
        "✅ Fact Checker": "Verify any claim",
        "📊 Text Insights": "Analyze your text"
    }

    # Track which feature is selected
    if "selected" not in st.session_state:
        st.session_state.selected = "🔍 Text Detector"

    for name, subtitle in features.items():
        is_active = st.session_state.selected == name
        if st.button(name, key=name, use_container_width=True):
            st.session_state.selected = name
            st.rerun()

# Load the selected feature
feature = st.session_state.selected

if feature == "🔍 Text Detector":
    feature_card("🔍 AI Text Detector", "Paste any text to detect if it was written by AI or a human")
    text_detector.show()

elif feature == "🖼️ Image Detector":
    feature_card("🖼️ AI Image Detector", "Upload an image to check if it was AI generated")
    image_detector.show()

elif feature == "📧 Email Generator":
    feature_card("📧 Email Generator", "Describe your email and let AI write it for you")
    email_generator.show()

elif feature == "✅ Fact Checker":
    feature_card("✅ Fact Checker", "Enter any claim and we'll verify it")
    fact_checker.show()

elif feature == "📊 Text Insights":
    feature_card("📊 Text Insights", "Get readability, sentiment and tone analysis")
    text_insights.show()
