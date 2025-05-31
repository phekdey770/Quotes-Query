import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_from_quotable(keyword, limit=50):
    url = f"https://api.quotable.io/quotes"
    params = {"query": keyword, "limit": limit}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return [(quote['content'], quote['author']) for quote in data.get('results', [])]
    except Exception as e:
        return [f"Error fetching from Quotable: {e}"]

def fetch_from_zenquotes(keyword, limit=50):
    url = "https://zenquotes.io/api/quotes/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [(quote['q'], quote['a']) for quote in data if keyword.lower() in quote['q'].lower()][:limit]
    except Exception as e:
        return [f"Error fetching from ZenQuotes: {e}"]

def fetch_from_inspirational_quotes(keyword, limit=50):
    url = f"https://type.fit/api/quotes"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [(quote['text'], quote.get('author', 'Unknown')) for quote in data if keyword.lower() in quote['text'].lower()][:limit]
    except Exception as e:
        return [f"Error fetching from Inspirational Quotes: {e}"]

def fetch_from_programming_quotes(keyword, limit=50):
    url = f"https://programming-quotes-api.herokuapp.com/quotes"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [(quote['en'], quote['author']) for quote in data if keyword.lower() in quote['en'].lower()][:limit]
    except Exception as e:
        return [f"Error fetching from Programming Quotes: {e}"]

def get_all_quotes(keyword, limit=50):
    apis = [fetch_from_quotable, fetch_from_zenquotes, fetch_from_inspirational_quotes, fetch_from_programming_quotes]
    
    all_quotes = []
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(api, keyword, limit): api.__name__ for api in apis}
        for future in as_completed(futures):
            result = future.result()
            # Filter out error messages or invalid responses
            valid_quotes = [item for item in result if isinstance(item, tuple) and len(item) == 2]
            all_quotes.extend(valid_quotes)
    
    return all_quotes

# Example usage:
keyword = "inspiration"
quotes = get_all_quotes(keyword, limit=100)

for i, (quote, author) in enumerate(quotes, start=1):
    print(f"{i}. \"{quote}\" - {author}\n")
