import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.models import SessionLocal, Article
from descriptive.sentiment import analyze_sentiment

def check_database():
    if not os.path.exists("articles.db"):
        print("❌ Database file 'articles.db' not found.")
        return False
    print("✅ Database file found.")
    return True

def check_articles_content():
    session = SessionLocal()
    articles = session.query(Article).all()
    session.close()

    if not articles:
        print("❌ No articles found in the database.")
        return False

    articles_with_content = [a for a in articles if a.content and a.content.strip()]
    print(f"📰 Total articles: {len(articles)}")
    print(f"📝 Articles with content: {len(articles_with_content)}")

    if len(articles_with_content) < 10:
        print("⚠️ Not enough content for meaningful training. Consider extracting more full text.")
        return False

    return True

def test_sentiment_on_sample():
    session = SessionLocal()
    article = session.query(Article).filter(Article.content != None).first()
    session.close()

    if not article:
        print("❌ No article with usable content to test sentiment.")
        return False

    try:
        score = analyze_sentiment(article.content)
        print(f"✅ Sentiment score test passed. Example score: {score:.2f}")
        return True
    except Exception as e:
        print(f"❌ Sentiment function failed: {e}")
        return False

if __name__ == "__main__":
    all_good = True
    if not check_database():
        all_good = False
    if not check_articles_content():
        all_good = False
    if not test_sentiment_on_sample():
        all_good = False

    if all_good:
        print("\n🎯 All pre-training checks passed. You’re ready to train the model.")
    else:
        print("\n🛑 Fix issues above before training.")
