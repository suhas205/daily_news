from newsapi import NewsApiClient
import sys

def check_api():
    try:
        newsapi = NewsApiClient(api_key='c10510cd97f14bceba92dee890627a03')
        sources = newsapi.get_sources()
        print(f"API is active. Found {len(sources.get('sources', []))} sources.")
        return True
    except Exception as e:
        print(f"API Error: {str(e)}")
        return False

if __name__ == '__main__':
    sys.exit(0 if check_api() else 1)
