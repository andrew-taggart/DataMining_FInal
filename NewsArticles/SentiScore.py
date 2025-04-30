##Download and Load SentiWordNet
import nltk
from nltk.corpus import sentiwordnet as swn
nltk.download('sentiwordnet')
nltk.download('wordnet')
nltk.download('punkt', force=True)
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import csv

##Define POS Tag Converter
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    return None

##Define Sentiment Analyzer Function
def analyze_sentiment(text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)
    
    pos_score = 0
    neg_score = 0
    token_count = 0
    
    for word, tag in tagged_tokens:
        wn_tag = get_wordnet_pos(tag)
        if not wn_tag:
            continue
        
        lemma = lemmatizer.lemmatize(word, pos=wn_tag)
        synsets = list(swn.senti_synsets(lemma, wn_tag))
        if not synsets:
            continue
        
        synset = synsets[0]  # Use the most common sense
        pos_score += synset.pos_score()
        neg_score += synset.neg_score()
        token_count += 1
    
    if token_count == 0:
        return 0.0
    
    score = (pos_score - neg_score) / token_count
    return round(score, 4)

##Analyze a List of Articles(Samples here)
articles = [
    "Opinion mining (OM) is a recent subdiscipline at the crossroads of information retrieval.",
    "OM has a rich set of applications",
    "SENTIWORDNET 3.0 is an improved version of SENTIWORDNET 1.0.",
    "BothSENTIWORDNET 1.0 and 3.0 are the result of automatically annotating all WORDNET synsets according to their degrees of positivity,"
]

####Analyze a List of Articles
results = []

for idx, article in enumerate(articles):
    score = analyze_sentiment(article)
    sentiment = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
    
    print(f"Article {idx+1} | Score: {score} | Sentiment: {sentiment}")
    
    results.append({
        "Article #": idx + 1,
        "Text": article,
        "Score": score,
        "Sentiment": sentiment
    })

###Save Results to CSV
with open("article_sentiments.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Article #", "Text", "Score", "Sentiment"])
    writer.writeheader()
    writer.writerows(results)

print("\n Results saved to 'article_sentiments.csv'")