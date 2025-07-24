from flask import Flask, render_template, request, redirect, url_for, session
import requests
import numpy as np
import csv
import os
import config
import joblib
import re

model = joblib.load("xgb_revenue_model.pkl")

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Basit kullanıcı veritabanı (şifreler düz metin, gerçek sistemde hash kullanılmalı)
users = {
    "admin": {"password": "adminpass", "role": "admin"},
    "user": {"password": "userpass", "role": "user"}
}

API_KEY = config.api_key

movie_store = []  # Web'de gösterilecek verileri geçici tutmak için

def clean_text(text):
    if not text:
        return 'N/A'
    text = re.sub(r'\s+', ' ', text)  # fazla boşlukları kaldır
    text = text.replace('\n', ' ').replace('\r', '')
    return text.strip()[:300]  # en fazla 300 karakter

def sanitize_movie(movie):
    title = clean_text(movie.get('title'))
    release_date = movie.get('release_date', 'N/A')
    overview = clean_text(movie.get('overview'))
    popularity = movie.get('popularity', 0.0)
    vote_average = movie.get('vote_average', 0.0)
    vote_count = movie.get('vote_count', 0)

    movie_id = movie.get('id')
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits,keywords"
    crew_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"

    try:
        details_response = requests.get(details_url)
        details = details_response.json()
        keywords = ', '.join(k['name'] for k in details.get('keywords', {}).get('keywords', []))
        runtime = details.get('runtime', 'N/A')
        cast = ', '.join(m['name'] for m in details.get('credits', {}).get('cast', [])[:5])
        poster_path = details.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else ''
    except:
        keywords, runtime, cast, poster_url = 'N/A', 'N/A', 'N/A', ''

    try:
        crew_response = requests.get(crew_url)
        crew = crew_response.json().get('crew', [])
        directors = ', '.join(m['name'] for m in crew if m['job'] == 'Director')
        editors = ', '.join(m['name'] for m in crew if m['job'] == 'Editor')
    except:
        directors, editors = 'N/A', 'N/A'

    try:
        if popularity and runtime and runtime != 'N/A':
             features = np.array([[float(popularity), float(runtime)]])
             revenue_prediction = model.predict(features)[0]
             revenue_prediction = round(revenue_prediction, 2)
        else:
             revenue_prediction = 'N/A'
    except:
        revenue_prediction = 'N/A'

    return {
        'Title': title,
        'Release Date': release_date,
        'Overview': overview,
        'Popularity': popularity,
        'Vote Average': vote_average,
        'Vote Count': vote_count,
        'Keywords': clean_text(keywords),
        'Runtime': runtime,
        'Cast': clean_text(cast),
        'Director': clean_text(directors),
        'Editor': clean_text(editors),
        'Poster URL': poster_url,
        'Revenue Prediction': revenue_prediction
    }

def get_movie_data(params, file_name, mode):
    api_url = "https://api.themoviedb.org/3/discover/movie"
    all_movies = []
    global movie_store
    movie_store = []

    for page in range(1, (params['num_movies'] // 20) + 2):
        api_params = {
            'api_key': API_KEY,
            'language': 'en-US',
            'sort_by': 'popularity.desc',
            'include_adult': 'false',
            'include_video': 'false',
            'page': page
        }

        if params['release_year']:
            api_params['primary_release_year'] = params['release_year']
        if params['genre']:
            api_params['with_genres'] = params['genre']

        response = requests.get(api_url, params=api_params)
        if response.status_code == 200:
            all_movies.extend(response.json().get('results', []))

    mode_flag = 'a' if mode == 'append' else 'w'
    with open(file_name, mode=mode_flag, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if mode_flag == 'w':
            writer.writerow(['Title', 'Release Date', 'Overview', 'Popularity', 'Vote Average', 'Vote Count', 'Keywords', 'Runtime', 'Cast', 'Director', 'Editor', 'Poster URL'])

        for movie in all_movies[:params['num_movies']]:
            data = sanitize_movie(movie)
            movie_store.append(data)
            writer.writerow(data.values())

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['admin_password']

        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admin_panel'))
            else:
                return redirect(url_for('user_panel'))
        else:
            return "<h3>❌ Giriş başarısız.</h3>"
    return render_template("login.html")

@app.route("/admin")
def admin_panel():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/user")
def user_panel():
    if session.get('role') != 'user':
        return redirect(url_for('login'))
    return render_template("user_panel.html")

@app.route("/search_and_save", methods=["POST"])
def search_and_save():
    if 'username' not in session:
        return redirect(url_for('login'))

    num_movies = int(request.form['num_movies'])
    release_year = request.form.get('release_year', '') if session.get('role') == 'admin' else ''
    file_name = request.form['file_name']
    file_mode = request.form['file_mode']
    genre = request.form.get('genre', '') if session.get('role') == 'admin' else ''

    get_movie_data({
        'num_movies': num_movies,
        'release_year': release_year,
        'genre': genre
    }, file_name, file_mode)

    return redirect(url_for('display_web'))

@app.route("/predict", methods=["POST"])
def predict():
    try:
        popularity = float(request.form["popularity"])
        runtime = float(request.form["runtime"])
        input_data = np.array([[popularity, runtime]])
        prediction = model.predict(input_data)[0]
        prediction = round(prediction, 2)
        return render_template("index.html", prediction=prediction, popularity=popularity, runtime=runtime)
    except Exception as e:
        return render_template("index.html", error=str(e))


@app.route("/csv/<filename>")
def display_csv(filename):
    rows = []
    if os.path.exists(filename):
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    return render_template("csv_view.html", rows=rows)

@app.route("/web")
def display_web():
    return render_template("web_table.html", movies=movie_store)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
