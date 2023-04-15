from flask import Flask, render_template, request
import pickle
import numpy as np
# Load the pickled files
movies = pickle.load(open("movie_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

# Create the Flask app
app = Flask(__name__)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names

# Define the route for the home page
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/recommend', methods=['POST'])
def recommendation():
    # Get the movie name entered by the user
    movie_name = request.form['movieName']
    top_similar_movies = recommend(movie_name)
    return render_template('main.html', movie_name=movie_name, recommended_movies=top_similar_movies)

if __name__ == '__main__':
    app.run(debug=True)
