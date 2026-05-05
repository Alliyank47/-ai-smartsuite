import streamlit as st
from textblob import TextBlob
import textstat
from styles import result_cards
def show():
    user_text = st.text_area(
        "Paste your text here",
        height=200,
        placeholder="Enter at least 50 words for best results..."
    )

    if st.button("Analyze Text"):
        if not user_text.strip():
            st.warning("Please enter some text first.")
        elif len(user_text.split()) < 10:
            st.warning("Please enter at least 10 words.")
        else:
            # TextBlob handles sentiment
            blob = TextBlob(user_text)
            sentiment_score = blob.sentiment.polarity

            if sentiment_score > 0.1:
                sentiment = "Positive 😊"
            elif sentiment_score < -0.1:
                sentiment = "Negative 😞"
            else:
                sentiment = "Neutral 😐"

            # Textstat handles readability
            readability = textstat.flesch_reading_ease(user_text)
            if readability >= 70:
                readability_label = f"{readability:.0f} (Easy)"
            elif readability >= 50:
                readability_label = f"{readability:.0f} (Moderate)"
            else:
                readability_label = f"{readability:.0f} (Difficult)"

            word_count = len(user_text.split())
            sentence_count = len(blob.sentences)
            avg_word_length = f"{sum(len(w) for w in user_text.split()) / word_count:.1f} chars"

            # Display results
            result_cards({
                "Sentiment": sentiment,
                "Readability": readability_label,
                "Words": str(word_count),
                "Sentences": str(sentence_count),
                "Avg Word Length": avg_word_length
            })