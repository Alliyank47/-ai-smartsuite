import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

def generate_email(topic, tone, additional_info):
    prompt = f"""Write a professional email with the following details:
    Topic: {topic}
    Tone: {tone}
    Additional Info: {additional_info}
    
    Format the response as:
    Subject: [subject line]
    
    [email body]
    
    Keep it concise and professional."""

    response = requests.post(
        GEMINI_URL,
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]

def show():
    st.markdown("### What's your email about?")

    topic = st.text_input(
        "Email Topic",
        placeholder="e.g. Request for meeting, Job application, Follow up..."
    )

    tone = st.selectbox("Select Tone", [
        "Professional",
        "Formal",
        "Friendly",
        "Apologetic",
        "Urgent"
    ])

    additional_info = st.text_area(
        "Any additional details?",
        height=100,
        placeholder="e.g. Meeting on Friday, Project deadline next week..."
    )

    if st.button("Generate Email"):
        if not topic.strip():
            st.warning("Please enter an email topic.")
        else:
            with st.spinner("Generating your email..."):
                email = generate_email(topic, tone, additional_info)

                st.markdown("### Generated Email")
                st.markdown(f"""
                    <div style="background:#1e0a3c;
                                border:1px solid rgba(124,58,237,0.3);
                                border-radius:14px;
                                padding:20px;
                                white-space: pre-wrap;
                                color:white;
                                font-size:14px;
                                line-height:1.6;">
                        {email}
                    </div>
                """, unsafe_allow_html=True)

                st.button("📋 Copy to Clipboard")