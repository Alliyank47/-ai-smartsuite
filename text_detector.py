import streamlit as st
import requests
import os
from dotenv import load_dotenv
from styles import result_cards

load_dotenv()
SAPLING_API_KEY = os.getenv("SAPLING_API_KEY")

def detect_text(text):
    response = requests.post(
        "https://api.sapling.ai/api/v1/aidetect",
        json={"key": SAPLING_API_KEY, "text": text}
    )
    return response.json()

def show():
    user_text = st.text_area(
        "Paste your text here",
        height=200,
        placeholder="Enter at least 50 words for accurate results..."
    )

    if st.button("Analyze Text"):
        if not user_text.strip():
            st.warning("Please enter some text first.")
        elif len(user_text.split()) < 10:
            st.warning("Please enter at least 10 words for accurate results.")
        else:
            with st.spinner("Analyzing..."):
                result = detect_text(user_text)

                try:
                    score = result["score"]  # 0 = human, 1 = AI
                    verdict = "AI Generated" if score > 0.5 else "Human Written"
                    confidence = f"{score * 100:.1f}%" if score > 0.5 else f"{(1 - score) * 100:.1f}%"
                    word_count = str(len(user_text.split()))

                    result_cards({
                        "Verdict": verdict,
                        "Confidence": confidence,
                        "Word Count": word_count
                    })

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.caption("⚠️ AI detection is not 100% accurate. Results are indicative only.")

                except:
                    st.error("Something went wrong. Please try again.")