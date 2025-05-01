import streamlit as st
from predictive.model_utils import load_model, preprocess
import joblib

# Load sentiment model and vectorizer
sentiment_model, sentiment_vectorizer = load_model(
    model_path="sentiment_classifier.pkl",
    vec_path="vectorizer.pkl"
)

# Load tariff model and vectorizer
def load_tariff_model(model_path="tariff_classifier.pkl", vec_path="tariff_vectorizer.pkl"):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    return model, vectorizer

tariff_model, tariff_vectorizer = load_tariff_model()

# Streamlit interface
st.title("News Article Analyzer")
st.write("This tool analyzes text for both **Sentiment** and **Tariff Relevance**.")

text_input = st.text_area("✍️ Enter article text:")

if st.button("Analyze"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        cleaned = preprocess(text_input)

        # Sentiment Prediction
        vec_sent = sentiment_vectorizer.transform([cleaned])
        sentiment = sentiment_model.predict(vec_sent)[0]

        # Tariff Relevance Prediction
        vec_tariff = tariff_vectorizer.transform([cleaned])
        relevance = tariff_model.predict(vec_tariff)[0]

        st.markdown(f"### 🧠 Predicted Sentiment: **{sentiment}**")
        st.markdown(f"### 📦 Tariff-Related Article: **{relevance}**")
