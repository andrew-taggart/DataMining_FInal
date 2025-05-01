import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import re
from gensim.parsing.preprocessing import remove_stopwords
from database.models import SessionLocal, Article
from descriptive.sentiment import analyze_sentiment
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import html
import spacy
import gensim.corpora as corpora
import gensim.models
from gensim.models import CoherenceModel
import pandas as pd
import matplotlib.colors as mcolors

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
import matplotlib.pyplot as plt

from collections import Counter



def lemmatize(tokens):
    doc = nlp(" ".join(tokens))
    return [token.lemma_ for token in doc]

def main():
    session = SessionLocal()
    articles = session.query(Article).filter(Article.content != None).all()
    session.close()

    if not articles:
        print("⚠️ No articles with content found.")
        return

    all_lemmas = []
    sentiment_labels = {"Positive": [], "Negative": []}

    for art in articles:
        content = art.content or ""
        cleaned_text = html.unescape(content)
        cleaned_text = re.sub('<[^<]+?>', '', cleaned_text)
        filtered_text = remove_stopwords(cleaned_text)
        token_text = filtered_text.split()
        token_text = [word.lower() for word in token_text if word.isalpha()]

        lemmas = lemmatize(token_text)
        cleanedtext = []

        # Use spaCy again to check for stopwords after lemmatization
        for item in nlp(" ".join(lemmas)):
            if not item.is_stop:
                cleanedtext.append(item.lemma_)  # safer to use lemma_ to ensure it's still normalized

        all_lemmas.append(cleanedtext)
       

        for word in lemmas:
            score = analyze_sentiment(word)
            if score > 0:
                sentiment_labels["Positive"].append(word)
            elif score < 0:
                sentiment_labels["Negative"].append(word)


    id2word = corpora.Dictionary(all_lemmas)
    corpus = [id2word.doc2bow(text) for text in all_lemmas]

    lda_model = gensim.models.LdaModel(
        corpus=corpus,
        id2word=id2word,
        num_topics=4,
        random_state=100,
        update_every=1,
        chunksize=100,
        passes=10,
        alpha='auto',
        per_word_topics=True
    )
    topics = lda_model.print_topics(num_words=10)
    for topic in topics:
        print(topic)
    coherence_model_lda = CoherenceModel(model=lda_model, texts=all_lemmas, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherence_lda)
 

  
        
    topics = lda_model.show_topics(formatted=False)

    # Flatten just the words for counting
    all_words = [word for _, topic in topics for word, _ in topic]
    counter = Counter(all_words)

    out = []
    for i, topic in topics:
        for word, weight in topic:
            out.append([word, i, weight, counter[word]])


    


   

if __name__ == "__main__":
    main()
