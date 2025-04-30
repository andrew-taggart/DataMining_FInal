import requests

api_key = 'a3fca4a804504596bf27e4b001e4f8e7'
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