import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from newsapi.fetch_articles import fetch_articles
from database.models import SessionLocal, Article
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def store_articles(articles):
    session = SessionLocal()
    for item in articles:
        article = Article(
            title=item.get("title", "No Title"),
            author=item.get("author"),
            url=item.get("url"),
            published_at=datetime.fromisoformat(item["publishedAt"].replace("Z", "+00:00")),
            content=item.get("content")
        )
        try:
            session.add(article)
            session.commit()
            print(f"✅ Stored: {article.title}")
        except IntegrityError:
            session.rollback()
            print(f"⚠️ Skipped duplicate: {article.title}")
    session.close()

def main():
    print("Fetching and storing articles...\n")
    articles = fetch_articles(query="tariffs")
    if articles:
        store_articles(articles)
    else:
        print("No articles found.")

if __name__ == "__main__":
    main()
