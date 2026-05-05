import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

def check_fact(claim):
    prompt = f"""You are a fact checker. Analyze the following claim.

Claim: {claim}

Respond in this EXACT format, nothing else:
VERDICT: [True / False / Unclear]
CONFIDENCE: [High / Medium / Low]
EXPLANATION: [2-3 sentences explaining your verdict]
SOURCES: [Mention 1-2 reliable sources]"""

    response = requests.post(
        GEMINI_URL,
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]

def parse_result(text):
    lines = text.strip().split("\n")
    data = {}
    for line in lines:
        if line.startswith("VERDICT:"):
            data["verdict"] = line.replace("VERDICT:", "").strip()
        elif line.startswith("CONFIDENCE:"):
            data["confidence"] = line.replace("CONFIDENCE:", "").strip()
        elif line.startswith("EXPLANATION:"):
            data["explanation"] = line.replace("EXPLANATION:", "").strip()
        elif line.startswith("SOURCES:"):
            data["sources"] = line.replace("SOURCES:", "").strip()
    return data

def show():
    st.markdown("### Enter a claim to verify")

    claim = st.text_area(
        "Your claim",
        height=150,
        placeholder="e.g. The Great Wall of China is visible from space..."
    )

    if st.button("Check Fact"):
        if not claim.strip():
            st.warning("Please enter a claim to verify.")
        else:
            with st.spinner("Verifying..."):
                raw = check_fact(claim)
                data = parse_result(raw)

                verdict = data.get("verdict", "Unclear")
                confidence = data.get("confidence", "Low")
                explanation = data.get("explanation", "No explanation available.")
                sources = data.get("sources", "No sources available.")

                # Color coding based on verdict
                if "True" in verdict:
                    verdict_color = "#4ade80"
                    verdict_bg = "#052e16"
                    verdict_emoji = "✅"
                elif "False" in verdict:
                    verdict_color = "#f87171"
                    verdict_bg = "#2d0a0a"
                    verdict_emoji = "❌"
                else:
                    verdict_color = "#fbbf24"
                    verdict_bg = "#2d1f00"
                    verdict_emoji = "⚠️"

                # Verdict + Confidence row
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                        <div style="background:{verdict_bg};
                                    border:1px solid {verdict_color}55;
                                    border-radius:14px;
                                    padding:20px;
                                    text-align:center;">
                            <p style="margin:0 0 8px; font-size:12px; color:{verdict_color}; 
                                      text-transform:uppercase; letter-spacing:0.1em;">Verdict</p>
                            <p style="margin:0; font-size:24px; font-weight:700; color:{verdict_color};">
                                {verdict_emoji} {verdict}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                        <div style="background:#1e0a3c;
                                    border:1px solid rgba(124,58,237,0.3);
                                    border-radius:14px;
                                    padding:20px;
                                    text-align:center;">
                            <p style="margin:0 0 8px; font-size:12px; color:#a78bfa; 
                                      text-transform:uppercase; letter-spacing:0.1em;">Confidence</p>
                            <p style="margin:0; font-size:24px; font-weight:700; color:white;">
                                {confidence}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Explanation box
                st.markdown(f"""
                    <div style="background:#1e0a3c;
                                border:1px solid rgba(124,58,237,0.3);
                                border-radius:14px;
                                padding:20px;
                                margin-bottom:12px;">
                        <p style="margin:0 0 8px; font-size:12px; color:#a78bfa; 
                                  text-transform:uppercase; letter-spacing:0.1em;">Explanation</p>
                        <p style="margin:0; font-size:14px; color:white; line-height:1.7;">{explanation}</p>
                    </div>
                """, unsafe_allow_html=True)

                # Sources box
                st.markdown(f"""
                    <div style="background:#1e0a3c;
                                border:1px solid rgba(124,58,237,0.3);
                                border-radius:14px;
                                padding:20px;
                                margin-bottom:12px;">
                        <p style="margin:0 0 8px; font-size:12px; color:#a78bfa; 
                                  text-transform:uppercase; letter-spacing:0.1em;">Sources</p>
                        <p style="margin:0; font-size:14px; color:white; line-height:1.7;">{sources}</p>
                    </div>
                """, unsafe_allow_html=True)

                st.caption("⚠️ AI fact checking may not be 100% accurate. Always verify with trusted sources.")