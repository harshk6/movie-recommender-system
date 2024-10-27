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
    # Get movie and TV genres separately
    movie_genres = fetch_from_tmdb("genre/movie/list").get("genres", [])
    tv_genres = fetch_from_tmdb("genre/tv/list").get("genres", [])
    return render_template('index.html', movie_genres=movie_genres, tv_genres=tv_genres)

@app.route('/search', methods=['GET'])
def search():
    # Get user input for rating, genre, and content type (movie or TV)
    min_rating = request.args.get('min_rating')
    genre_id = request.args.get('genre')
    content_type = request.args.get('type', 'movie')

    # Define parameters for filtering content
    search_params = {
        "vote_average.gte": min_rating,
        "with_genres": genre_id,
    }

    # Use the correct TMDb discover endpoint for the content type
    search_results = fetch_from_tmdb(f"discover/{content_type}", search_params)
    return jsonify(search_results)

@app.route('/details/<content_type>/<int:item_id>')
def details(content_type, item_id):
    # Fetch specific details based on content type (movie or TV)
    details = fetch_from_tmdb(f"{content_type}/{item_id}")
    return render_template('details.html', details=details)

if __name__ == '__main__':
    app.run(debug=True)
