import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.models import SessionLocal, Article
from descriptive.sentiment import analyze_sentiment

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt')
nltk.download('stopwords')

def label_sentiment(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

def preprocess(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    return ' '.join([word for word in tokens if word.isalpha() and word not in stop_words])

def load_and_prepare_data():
    session = SessionLocal()
    articles = session.query(Article).filter(Article.content != None).all()
    session.close()

    texts, labels = [], []
    for article in articles:
        score = analyze_sentiment(article.content)
        label = label_sentiment(score)
        cleaned = preprocess(article.content)
        if cleaned.strip():
            texts.append(cleaned)
            labels.append(label)

    return texts, labels

def train_and_evaluate(texts, labels):
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(texts)
    y = labels

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = MultinomialNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    joblib.dump(model, "sentiment_classifier.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")
    print("✅ Model and vectorizer saved.")

if __name__ == "__main__":
    texts, labels = load_and_prepare_data()
    if texts:
        train_and_evaluate(texts, labels)
    else:
        print("⚠️ No data available for training.")
