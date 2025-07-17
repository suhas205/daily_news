# Sports News Hub Application
## A Modern Web-Based News Platform

---

## Project Overview
- A Flask-based web application for sports news aggregation
- Real-time news updates using NewsAPI integration
- Modern and responsive user interface
- Easy-to-use news browsing experience

---

## Technical Stack

### Frontend:
- HTML5, CSS3, JavaScript
- Bootstrap 5.1.3 for responsive design
- Custom animations and styling

### Backend:
- Python Flask framework
- NewsAPI for data fetching
- RESTful architecture

---

## Key Features
- Real-time sports news updates
- Responsive card-based UI
- Article previews with images
- Direct links to full articles
- 30-day news archive
- Clean and modern design

---

## Architecture
1. Flask Backend Server
2. NewsAPI Integration
3. Template Engine (Jinja2)
4. Bootstrap Frontend
5. Custom CSS Styling
6. JavaScript Interactivity

---

## User Interface
- Navigation bar with branding
- Card-based article display
- Hover animations
- Image thumbnails
- Formatted dates
- Read More buttons

---

## Code Structure
```
/news app
  ├── app.py (Main application)
  ├── templates/
  │   └── index.html
  ├── static/
  │   ├── style.css
  │   └── script.js
  └── requirements.txt
```

---

## Implementation Highlights

### Backend (app.py):
```python
@app.route('/')
def home():
    news_data = fetch_sports_news()
    return render_template('index.html', articles=news_data['articles'])
```

### Frontend (index.html):
```html
<div class="card h-100">
    <img src="{{ article.urlToImage }}" class="card-img-top">
    <div class="card-body">
        <h5 class="card-title">{{ article.title }}</h5>
        <p class="card-text">{{ article.description }}</p>
    </div>
</div>
```

---

## Future Enhancements
- Category-based filtering
- Search functionality
- User authentication
- Bookmarking features
- Social media sharing
- Push notifications

---

## Thank You
### Questions & Discussion
