from nltk.corpus import sentiwordnet as swn, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def analyze_sentiment(text):
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)

    total_score = 0
    count = 0

    for word, tag in tagged:
        wn_tag = get_wordnet_pos(tag)
        if wn_tag:
            lemma = lemmatizer.lemmatize(word, wn_tag)
            synsets = list(swn.senti_synsets(lemma, wn_tag))
            if synsets:
                syn = synsets[0]  # take the first synset
                score = syn.pos_score() - syn.neg_score()
                total_score += score
                count += 1

    return total_score / count if count > 0 else 0.0
