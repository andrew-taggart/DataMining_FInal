import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.models import SessionLocal, Article
from descriptive.sentiment import analyze_sentiment
import matplotlib.pyplot as plt

def main():
    session = SessionLocal()
    articles = session.query(Article).filter(Article.content != None).all()
    session.close()

    if not articles:
        print("⚠️ No articles with content found.")
        return

    scores = []
    sentiment_labels = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for art in articles:
        score = analyze_sentiment(art.content)
        scores.append(score)
        if score > 0:
            sentiment_labels["Positive"] += 1
        elif score < 0:
            sentiment_labels["Negative"] += 1
        else:
            sentiment_labels["Neutral"] += 1

    # Plot histogram of scores
    plt.figure(figsize=(10, 5))
    plt.hist(scores, bins=20, edgecolor="black")
    plt.title("Sentiment Score Distribution")
    plt.xlabel("Sentiment Score")
    plt.ylabel("Number of Articles")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot pie chart    
    plt.figure(figsize=(6, 6))
    labels = list(sentiment_labels.keys())
    sizes = list(sentiment_labels.values())
    colors = ["lightgreen", "lightcoral", "lightgray"]
    explode = (0.05, 0.05, 0.05)

    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, colors=colors, explode=explode)
    plt.title("Sentiment Classification (Pie Chart)")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

    print(f"Total articles with content: {len(articles)}")

if __name__ == "__main__":
    main()

