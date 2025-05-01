import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.models import SessionLocal, Article
from newspaper import Article as NewsArticle
from time import sleep

def extract_and_update_full_text():
    session = SessionLocal()
    articles = session.query(Article).filter((Article.content == None) | (Article.content == "")).all()

    if not articles:
        print("✅ All articles already have content.")
        return

    for i, art in enumerate(articles, start=1):
        try:
            print(f"[{i}] Extracting: {art.url}")
            n_article = NewsArticle(art.url)
            n_article.download()
            n_article.parse()
            art.content = n_article.text
            session.commit()
            print(f"✅ Extracted: {art.title[:60]}")
        except Exception as e:
            print(f"❌ Failed: {art.url} — {e}")
            session.rollback()
        sleep(1)  # Be polite and avoid being rate-limited

    session.close()
    print("✅ Extraction completed.")

if __name__ == "__main__":
    extract_and_update_full_text()