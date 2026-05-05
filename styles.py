import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* Main background */
        .stApp {
            background: #1a0533;
        }

        /* Sidebar background */
        [data-testid="stSidebar"] {
            background: #120228;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        /* Button */
        .stButton>button {
            background: linear-gradient(90deg, #7c3aed, #4f46e5);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 28px;
            font-weight: 600;
            width: 100%;
            font-size: 14px;
        }

        /* All text white */
        .stApp, p, h1, h2, h3, label, .stMarkdown {
            color: white !important;
        }

        /* Text input and text area boxes */
        .stTextArea textarea, .stTextInput input {
            background: #120228 !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            border-radius: 10px !important;
        }

        /* Hide default streamlit menu and footer */
        #MainMenu {visibility: hidden;}
                /* Zoom fix */
                    .stApp {
                        zoom: 1.1;
                        font-size: 16px;
                    }
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)


def feature_card(title, subtitle):
    st.markdown(f"""
        <div style="background:linear-gradient(135deg,#2d1b69,#1e1254);
                    border:1px solid rgba(124,58,237,0.3);
                    border-radius:16px;
                    padding:20px 24px;
                    margin-bottom:20px;">
            <p style="margin:0 0 4px; font-size:20px; font-weight:700;">{title}</p>
            <p style="margin:0; font-size:13px; color:#a78bfa;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def result_cards(data):
    cols = st.columns(len(data))
    for col, (label, value) in zip(cols, data.items()):
        with col:
            st.markdown(f"""
                <div style="background:#1e0a3c;
                            border:1px solid rgba(124,58,237,0.3);
                            border-radius:14px;
                            padding:16px;
                            text-align:center;">
                    <p style="margin:0 0 6px; font-size:11px; color:#a78bfa;
                               text-transform:uppercase; letter-spacing:0.05em;">{label}</p>
                    <p style="margin:0; font-size:18px; font-weight:700;">{value}</p>
                </div>
            """, unsafe_allow_html=True)



            