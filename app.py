import streamlit as st
import pickle
import pandas as pd
import os

# Load dumped similarity matrix
with open("models/similarity_matrix_first.pkl", "rb") as file:
    similarity_matrix = pickle.load(file)

# Load movie dataset
movies = pd.read_csv("dataset/movies.csv")  # Ensure this file is in the same directory
movie_titles = movies['title'].tolist()

# Streamlit App
st.set_page_config(page_title="Movie Recommendation System", layout="wide")

# Header and Description
st.title("🎥 Movie Recommendation System")
st.image("images/netflix-image.jpg", caption="Discover Your Next Favorite Movie!")
st.markdown("""
Welcome to the Movie Recommendation System!  
- **Model**: Cosine Similarity on Movie Ratings  
- **Working**: Provide a movie title, and we'll suggest similar movies based on ratings and user preferences.  
- **Dataset**: MovieLens  

### Input Format
- Enter the exact movie title as it appears in the dataset. For example:  
  - `"Kolya (1996)"`  
  - `"Toy Story (1995)"`  
  - `"Star Wars (1977)"` 
In other words, movie name with proper space, then space, open bracket, year, & lastly close bracket.

""")

# Input Section
st.subheader("Find Movies Similar to Your Favorite")
movie_name = st.text_input("Enter a movie name", placeholder="e.g., Kolya (1996)")

# Recommendation Logic
if st.button("Recommend"):
    if movie_name in movie_titles:
        # Get index of the movie
        movie_idx = movie_titles.index(movie_name)
        
        # Fetch similarity scores and recommend top 5
        similar_movies = sorted(
            list(enumerate(similarity_matrix[movie_idx])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]  # Skip the first one as it's the input movie itself
        
        st.subheader(f"Movies similar to '{movie_name}':")
        for idx, score in similar_movies:
            st.write(f"- {movies.iloc[idx]['title']} (Similarity Score: {score:.2f})")
    else:
        st.error("Movie not found. Please check the spelling, input format (name, space, brackets, year) or try another movie.")
