import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
url = ('https://newsapi.org/v2/everything?'
       'q=tariffs$'
       'language=en&'
       'sortBy=publishedAt&'
       f'apiKey={api_key}')

response = requests.get(url)
articles = response.json()['articles']

print("Requests module imported successfully!")


## article test
if articles:
    first_article= articles[0]
    print("Title:", first_article['title'])
    print("Source ID:", first_article.get('source', {}).get('id'))
    print("Source Name:", first_article.get('source', {}).get('name'))
    print("Link:", first_article['url'])
    print("Date:", first_article['publishedAt'])
else:
    print("No articles found.")