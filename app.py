from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'a211e041c39243724424cedbb1fd8286'  # Replace with your TMDb API key
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
    # Fetch genres list to show in dropdown
    genres = fetch_from_tmdb("genre/movie/list")["genres"]
    return render_template('index.html', genres=genres)

@app.route('/search', methods=['GET'])
def search():
    min_rating = request.args.get('min_rating')
    genre_id = request.args.get('genre')
    content_type = request.args.get('type', 'movie')  # 'movie' or 'tv'

    # Discover movies or TV shows based on provided filters
    search_params = {
        "vote_average.gte": min_rating,
        "with_genres": genre_id,
    }
    search_results = fetch_from_tmdb(f"discover/{content_type}", search_params)

    return jsonify(search_results)

@app.route('/details/<content_type>/<int:item_id>')
def details(content_type, item_id):
    """Fetch details for a specific movie/series."""
    details = fetch_from_tmdb(f"{content_type}/{item_id}")
    return render_template('details.html', details=details)

if __name__ == '__main__':
    app.run(debug=True)
