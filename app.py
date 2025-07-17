from flask import Flask, render_template, request
from newsapi import NewsApiClient
import os
from datetime import datetime, timedelta
import sys
import requests

app = Flask(__name__)

def fetch_category_news(category=None, query=None):
    try:
        # Initialize News API client
        newsapi = NewsApiClient(api_key='229e61142038490da8371bb42379c6a2')
        
        today = datetime.now()
        
        if category:
            # Get top headlines for specific category
            news = newsapi.get_top_headlines(
                category=category,
                language='en',
                page_size=8
            )
        elif query:
            # Get news based on search query
            news = newsapi.get_everything(
                q=query,
                language='en',
                sort_by='publishedAt',
                page_size=30
            )
        else:
            # Get general top headlines
            news = newsapi.get_top_headlines(
                language='en',
                page_size=12
            )
        
        return news
    except Exception as e:
        print(f"Error fetching news: {str(e)}", file=sys.stderr)
        return None

def get_sample_news():
    current_date = datetime.now().strftime('%B %d, %Y')
    return {
        'top_news': [
            {
                'title': 'Major Climate Agreement Reached at Global Summit',
                'description': 'World leaders have agreed to ambitious new climate targets at the latest international summit.',
                'url': '#',
                'urlToImage': 'https://via.placeholder.com/400x200.png?text=Climate+News',
                'formatted_date': current_date
            },
            {
                'title': 'Tech Giant Unveils Revolutionary AI Platform',
                'description': 'A leading technology company has announced a groundbreaking artificial intelligence system.',
                'url': '#',
                'urlToImage': 'https://via.placeholder.com/400x200.png?text=Tech+News',
                'formatted_date': current_date
            }
        ],
        'technology': [
            {
                'title': 'New Smartphone Features Breakthrough Battery Technology',
                'description': 'Latest smartphone release promises week-long battery life with innovative technology.',
                'url': '#',
                'urlToImage': 'https://via.placeholder.com/400x200.png?text=Technology',
                'formatted_date': current_date
            }
        ],
        'business': [
            {
                'title': 'Global Markets Hit Record High',
                'description': 'Stock markets worldwide reach unprecedented levels amid strong economic data.',
                'url': '#',
                'urlToImage': 'https://via.placeholder.com/400x200.png?text=Business',
                'formatted_date': current_date
            }
        ],
        'entertainment': [
            {
                'title': 'Blockbuster Movie Breaks Box Office Records',
                'description': 'Latest superhero film becomes highest-grossing release of the year.',
                'url': '#',
                'urlToImage': 'https://via.placeholder.com/400x200.png?text=Entertainment',
                'formatted_date': current_date
            }
        ],
        'sports': [
            {
                'title': 'Historic Victory in World Championship Final',
                'description': 'Underdog team claims surprising victory in international tournament.',
                'url': '#',
                'urlToImage': 'https://via.placeholder.com/400x200.png?text=Sports',
                'formatted_date': current_date
            }
        ],
        'health': [
            {
                'title': 'Breakthrough in Medical Research',
                'description': 'Scientists announce promising results in treatment of chronic diseases.',
                'url': '#',
                'urlToImage': 'https://via.placeholder.com/400x200.png?text=Health',
                'formatted_date': current_date
            }
        ]
    }

@app.route('/')
def home():
    try:
        # Fetch news for different categories
        top_news = fetch_category_news()
        technology = fetch_category_news(category='technology')
        business = fetch_category_news(category='business')
        entertainment = fetch_category_news(category='entertainment')
        sports = fetch_category_news(category='sports')
        health = fetch_category_news(category='health')
        
        # Process all news data
        news_data = {}
        
        if top_news and 'articles' in top_news:
            for article in top_news['articles']:
                if article.get('publishedAt'):
                    try:
                        date = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                        article['formatted_date'] = date.strftime('%B %d, %Y')
                    except Exception as e:
                        article['formatted_date'] = 'Date not available'
            news_data['top_news'] = top_news['articles']
        
        categories = {
            'technology': technology,
            'business': business,
            'entertainment': entertainment,
            'sports': sports,
            'health': health
        }
        
        for category, data in categories.items():
            if data and 'articles' in data:
                for article in data['articles']:
                    if article.get('publishedAt'):
                        try:
                            date = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                            article['formatted_date'] = date.strftime('%B %d, %Y')
                        except Exception as e:
                            article['formatted_date'] = 'Date not available'
                news_data[category] = data['articles']
            else:
                news_data[category] = []
        
        # If no news data available, use sample data
        if not news_data:
            news_data = get_sample_news()
            
        return render_template('index.html', news=news_data)
    except Exception as e:
        print(f"Error in home route: {str(e)}", file=sys.stderr)
        return render_template('index.html', 
                             news=get_sample_news(),
                             error=str(e))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    try:
        news_data = fetch_category_news(query=query)
            
        if news_data and 'articles' in news_data:
            for article in news_data['articles']:
                if article.get('publishedAt'):
                    try:
                        date = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                        article['formatted_date'] = date.strftime('%B %d, %Y')
                    except Exception as e:
                        article['formatted_date'] = 'Date not available'
            return render_template('search.html', 
                                 articles=news_data['articles'],
                                 query=query)
        return render_template('search.html', 
                             articles=[],
                             query=query,
                             error="No results found")
    except Exception as e:
        print(f"Error in search route: {str(e)}", file=sys.stderr)
        return render_template('search.html', 
                             articles=[],
                             query=query,
                             error=str(e))

from flask import jsonify

@app.route('/refresh')
def refresh():
    try:
        # Fetch news for different categories
        top_news = fetch_category_news()
        technology = fetch_category_news(category='technology')
        business = fetch_category_news(category='business')
        entertainment = fetch_category_news(category='entertainment')
        sports = fetch_category_news(category='sports')
        health = fetch_category_news(category='health')

        news_data = {}
        if top_news and 'articles' in top_news:
            for article in top_news['articles']:
                if article.get('publishedAt'):
                    try:
                        date = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                        article['formatted_date'] = date.strftime('%B %d, %Y')
                    except Exception as e:
                        article['formatted_date'] = 'Date not available'
            news_data['top_news'] = top_news['articles']
        categories = {
            'technology': technology,
            'business': business,
            'entertainment': entertainment,
            'sports': sports,
            'health': health
        }
        for category, data in categories.items():
            if data and 'articles' in data:
                for article in data['articles']:
                    if article.get('publishedAt'):
                        try:
                            date = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                            article['formatted_date'] = date.strftime('%B %d, %Y')
                        except Exception as e:
                            article['formatted_date'] = 'Date not available'
                news_data[category] = data['articles']
            else:
                news_data[category] = []
        return jsonify(news_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=True)
