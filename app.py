import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4Y2U3MDJlM2YwM2NlMzRiNjE4YzdiN2VhYTdkYjQ3OCIsInN1YiI6IjY1NzQ0MzZkYTFkMzMyMDBhY2I4MjhmMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ZVjgbpSiW5B9Yo5IHEin5vcS8Hy8oOsmnAeoAa5eZtU"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w185/"+data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # sort these distances and extract the top 5 movies
    movielist = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    poster = []
    for i in movielist:
        #         print(i[0])
        poster.append(fetch_poster(movies.iloc[i[0]].movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, poster


movies = pickle.load(open('movies.pkl','rb'))
movies_list = movies['title'].values
similarity=pickle.load(open('similarity.pkl','rb'))
st.title('Movie recommendation system')

option = st.selectbox(
    'Which movie do you like to watch ?',
    movies_list)

st.write('The recommended movies based on:', option)

# st.button("Reset", type="primary")

if st.button('Recommend'):
    names,posters=recommend(option)
    columns = st.columns(5)
    for i in range(5):
        with columns[i]:
            st.image(posters[i], width=130, caption=names[i])