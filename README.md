# DataMining_Final

Technique focus: Web/Text Mining or Big Data & Cloud Mining

Question: Are media outlets reporting positvely or negatively on Trump-Tariffs?

Answer:
- Defined by our analysis from NEWS.API- other??

## Add File organization
- List folders and describe use
- Specific Techniques
  - Descriptive
    - Classification (sentiment analysis of text)
    - 
  - Predictive
  - Text Mining
  - Big Data/Cloud Mining

## To Do List
- Add "Creative" Title to project
- Define Keywords
- Visuals (tabular, plot-based, command-line etc.)
- Presentation Format

## Setup
-	Suggest creating virtual Environment
-	Pip installs
```
pip install requests python-dotenv sqlalchemy nltk newspaper3k matplotlib lxml_html_clean
``` 
-	Create .env file
```
API_KEY=your_newsapi_key_here
``` 
-	Download NLTK Data
```
python3 -c "import nltk; [nltk.download(p) for p in ['punkt', 'wordnet', 'sentiwordnet', 'averaged_perceptron_tagger']]"
``` 
-	Initialize the Database
```
python scripts/init_db.py
``` 
-	Fetch and Store News Articles
```
python scripts/scrape_and_store.py
``` 
-	Extract Full Text from URLs
```
python scripts/extract_full_text.py
``` 
-	Analyze Sentiment and Visualize Results
```
python scripts/analyze_sentiment.py
``` 




## Software/Tools Used
- [News API](https://newsapi.org/)
- Geeks for Geeks
  - [Removing stop words with NLTK](https://www.geeksforgeeks.org/removing-stop-words-nltk-python/)
- Stack Overflow
  - [Strip HTML ffrom strings in Python](https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python)
- [Overleaf](https://www.overleaf.com/)

Research Paper
- Format: IEEE – Institute of Electrical and Electronics Engineers
- References: (Minimum 5, including 3 papers, the Textbook, )
- Sections:
1.	Title
2.	Authors + Affiliations
3.	Abstract
4.	Keywords (3–6)
5.	Introduction
6.	Related Work
7.	Approach & Implementation
8.	Experiments & Results
9.	Conclusion & Future Work
10.	Acknowledgments (optional)
11.	References (Minimum: 5, including at least 3 papers, textbooks, and software/tools)
