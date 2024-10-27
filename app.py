from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'your_tmdb_api_key'  # Replace with your TMDb API key
BASE_URL = 'https://api.themoviedb.org/3'

def fetch_from_tmdb(endpoint, params=None):
    """Helper function to fetch data from TMDb API."""
    params = params or {}
    params['api_key'] = API_KEY
    params['language'] = 'en-US'
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    title = request.args.get('title')
    min_rating = request.args.get('min_rating')
    genre_id = request.args.get('genre')
    content_type = request.args.get('type', 'movie')  # 'movie' or 'tv'

    # Search for movie or TV series by title
    search_results = fetch_from_tmdb(f"search/{content_type}", {"query": title}) if title else {}

    # Filter by rating and genre if applicable
    if search_results and (min_rating or genre_id):
        search_results['results'] = [
            item for item in search_results.get('results', [])
            if (float(item['vote_average']) >= float(min_rating) if min_rating else True) and
               (genre_id in [str(g) for g in item['genre_ids']] if genre_id else True)
        ]

    return jsonify(search_results)

@app.route('/details/<content_type>/<int:item_id>')
def details(content_type, item_id):
    """Fetch details for a specific movie/series."""
    details = fetch_from_tmdb(f"{content_type}/{item_id}")
    return render_template('details.html', details=details)

if __name__ == '__main__':
    app.run(debug=True)

