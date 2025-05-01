import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import re
from gensim.parsing.preprocessing import remove_stopwords
from database.models import SessionLocal, Article
from descriptive.sentiment import analyze_sentiment
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import html
from word_cloud import word_cloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def word_cloud(text,title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  
    plt.title(f"{title} word cloud for news articles")

    plt.show()


def main():

    session = SessionLocal()
    articles = session.query(Article).filter(Article.content != None).all()
    session.close()

    if not articles:
        print("⚠️ No articles with content found.")
        return

    scores = []
    sentiment_labels = {"Positive": [], "Negative": []}

    for art in articles:
        content = art.content or ""
        cleaned_text = html.unescape(content)
        cleaned_text = re.sub('<[^<]+?>', '', cleaned_text)
        filtered_text = remove_stopwords(cleaned_text)
        token_text = filtered_text.split()
      
        token_text = [word.lower() for word in token_text if word.isalpha()]
        for word in token_text:
            score = analyze_sentiment(word)
            if score > 0:
                sentiment_labels["Positive"].append(word)
            elif score < 0:
                sentiment_labels["Negative"].append(word)
       
    positive_text = " ".join(sentiment_labels["Positive"])
    negative_text = " ".join(sentiment_labels["Negative"])


    if positive_text:
        word_cloud(positive_text, "Positive")
    if negative_text:
        word_cloud(negative_text, "Negative")




    

if __name__ == "__main__":
    main()

