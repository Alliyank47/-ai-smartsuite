import streamlit as st
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()
SIGHTENGINE_USER = os.getenv("SIGHTENGINE_USER")
SIGHTENGINE_SECRET = os.getenv("SIGHTENGINE_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

def detect_image(image_bytes):
    response = requests.post(
        'https://api.sightengine.com/1.0/check.json',
        files={'media': image_bytes},
        data={
            'models': 'genai',
            'api_user': SIGHTENGINE_USER,
            'api_secret': SIGHTENGINE_SECRET
        }
    )
    return response.json()

def explain_image(image_bytes, verdict):
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    prompt = f"""This image has been detected as {verdict} by an AI detection system.
Please analyze this image and explain in 3-4 sentences:
- What visual clues suggest it is {verdict}
- Any specific features like lighting, textures, skin, background, or artifacts that stand out
- Keep it simple and easy to understand"""
    response = requests.post(
        GEMINI_URL,
        json={
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_b64
                    }}
                ]
            }]
        }
    )
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]

def show():
    st.markdown("""
        <div style="background:#1e0a3c;
                    border: 2px dashed rgba(124,58,237,0.5);
                    border-radius:16px;
                    padding:30px;
                    text-align:center;
                    margin-bottom:20px;">
            <p style="margin:0 0 8px; font-size:32px;">🖼️</p>
            <p style="margin:0 0 4px; font-size:16px; font-weight:600; color:white;">Upload an Image</p>
            <p style="margin:0; font-size:13px; color:#a78bfa;">Supports JPG and PNG • Max 5MB</p>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded_file is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(uploaded_file, use_container_width=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze = st.button("🔍 Detect AI", use_container_width=True)

        if analyze:
            file_size = uploaded_file.size / (1024 * 1024)
            if file_size > 5:
                st.warning("File too large. Please upload an image under 5MB.")
            else:
                with st.spinner("Analyzing image..."):
                    result = detect_image(uploaded_file.getvalue())

                    try:
                        ai_score = result["type"]["ai_generated"]
                        human_score = 1 - ai_score
                        verdict = "AI Generated" if ai_score > 0.5 else "Real Photo"
                        ai_pct = f"{ai_score * 100:.1f}%"
                        human_pct = f"{human_score * 100:.1f}%"

                        if ai_score > 0.5:
                            verdict_color = "#f87171"
                            verdict_bg = "#2d0a0a"
                            verdict_emoji = "🤖"
                        else:
                            verdict_color = "#4ade80"
                            verdict_bg = "#052e16"
                            verdict_emoji = "📷"

                        st.markdown("<br>", unsafe_allow_html=True)

                        st.markdown(f"""
                            <div style="background:{verdict_bg};
                                        border:2px solid {verdict_color}55;
                                        border-radius:20px;
                                        padding:30px;
                                        text-align:center;
                                        margin-bottom:16px;">
                                <p style="margin:0 0 8px; font-size:40px;">{verdict_emoji}</p>
                                <p style="margin:0 0 4px; font-size:28px; font-weight:800; color:{verdict_color};">
                                    {verdict}
                                </p>
                                <p style="margin:0; font-size:13px; color:{verdict_color}88;">
                                    Analysis complete
                                </p>
                            </div>
                        """, unsafe_allow_html=True)

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"""
                                <div style="background:#2d0a0a;
                                            border:1px solid #f8717155;
                                            border-radius:16px;
                                            padding:24px;
                                            text-align:center;">
                                    <p style="margin:0 0 8px; font-size:12px; color:#f87171;
                                              text-transform:uppercase; letter-spacing:0.1em;">🤖 AI Probability</p>
                                    <p style="margin:0; font-size:36px; font-weight:800; color:#f87171;">{ai_pct}</p>
                                </div>
                            """, unsafe_allow_html=True)

                        with col2:
                            st.markdown(f"""
                                <div style="background:#052e16;
                                            border:1px solid #4ade8055;
                                            border-radius:16px;
                                            padding:24px;
                                            text-align:center;">
                                    <p style="margin:0 0 8px; font-size:12px; color:#4ade80;
                                              text-transform:uppercase; letter-spacing:0.1em;">📷 Real Probability</p>
                                    <p style="margin:0; font-size:36px; font-weight:800; color:#4ade80;">{human_pct}</p>
                                </div>
                            """, unsafe_allow_html=True)

                        with st.spinner("Getting detailed analysis..."):
                            explanation = explain_image(uploaded_file.getvalue(), verdict)
                            st.markdown(f"""
                                <div style="background:#1e0a3c;
                                            border:1px solid rgba(124,58,237,0.3);
                                            border-radius:16px;
                                            padding:24px;
                                            margin-top:16px;">
                                    <p style="margin:0 0 10px; font-size:12px; color:#a78bfa;
                                              text-transform:uppercase; letter-spacing:0.1em;">🔍 Why?</p>
                                    <p style="margin:0; font-size:14px; color:white; line-height:1.8;">{explanation}</p>
                                </div>
                            """, unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)
                        st.caption("⚠️ AI image detection may not be 100% accurate.")

                    except:
                        st.error("Something went wrong. Please try again.")