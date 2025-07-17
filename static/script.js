// Auto-refresh the page every 30 minutes
setTimeout(() => {
    window.location.reload();
}, 30 * 60 * 1000);

// AJAX Refresh functionality
function renderNewsSection(sectionId, articles, cardHeader, cardColorClass) {
    let html = '';
    if (Array.isArray(articles) && articles.length > 0) {
        articles.forEach(article => {
            html += `<div class="mb-3">
                <h6><a href="${article.url}" class="text-dark text-decoration-none" target="_blank">${article.title}</a></h6>
                <p class="mb-1">${article.description || ''}</p>
                <small class="text-muted">${article.formatted_date || ''}</small>
            </div><hr>`;
        });
        html = html.replace(/<hr>$/,'');
    } else {
        html = '<p>No news available.</p>';
    }
    document.getElementById(sectionId).innerHTML = html;
}

function renderTopNews(articles) {
    let html = '<div class="row">';
    if (Array.isArray(articles) && articles.length > 0) {
        articles.forEach(article => {
            html += `<div class="col-md-4 mb-4">
                <div class="card h-100">
                    ${article.urlToImage ? `<img src="${article.urlToImage}" class="card-img-top" alt="News Image">` : ''}
                    <div class="card-body">
                        <h5 class="card-title">${article.title}</h5>
                        <p class="card-text">${article.description || ''}</p>
                        <p class="card-text"><small class="text-muted">${article.formatted_date || ''}</small></p>
                        <a href="${article.url}" class="btn btn-primary" target="_blank">Read More</a>
                    </div>
                </div>
            </div>`;
        });
    } else {
        html += '<p>No headlines available.</p>';
    }
    html += '</div>';
    document.getElementById('top-news-section').innerHTML = html;
}

document.addEventListener('DOMContentLoaded', () => {
    // Refresh button AJAX
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function(e) {
            e.preventDefault();
            refreshBtn.disabled = true;
            refreshBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Refreshing...';
            fetch('/refresh')
                .then(response => response.json())
                .then(data => {
                    renderTopNews(data.top_news);
                    renderNewsSection('technology-section', data.technology);
                    renderNewsSection('business-section', data.business);
                    renderNewsSection('entertainment-section', data.entertainment);
                    renderNewsSection('sports-section', data.sports);
                    renderNewsSection('health-section', data.health);
                })
                .catch(() => { alert('Failed to refresh news.'); })
                .finally(() => {
                    refreshBtn.disabled = false;
                    refreshBtn.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Refresh';
                });
        });
    }

    // Add smooth scrolling
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('click', (e) => {
            if (!e.target.classList.contains('btn')) {
                const link = card.querySelector('.btn');
                if (link) {
                    window.open(link.href, '_blank');
                }
            }
        });
    });
});
