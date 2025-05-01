import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from predictive.model_utils import load_model, preprocess
import argparse

def predict_sentiment(text):
    model, vectorizer = load_model()
    processed = preprocess(text)
    vectorized = vectorizer.transform([processed])
    prediction = model.predict(vectorized)[0]
    return prediction

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict sentiment of input text.")
    parser.add_argument("--text", type=str, required=True, help="Text to analyze")
    args = parser.parse_args()

    result = predict_sentiment(args.text)
    print(f"🧠 Predicted Sentiment: {result}")
