# Project Overview
In this project, we will give movie recommendations based on a movie you select.

## Dataset

## Model
A content-based filtering approach was used to create our model. I used cast, crew, keywords, genres, and production_companies as the features for training our model. From the crew, I got the director's name and from the cast, keywords, 
genres, and production companies the top 3 are taken. Then a metadata soup is created by adding the features we extracted earlier. These were passed to a count vectorizer and the obtained matrix is passed to a cosine_similarity function 
to get the similarity indices. A recommendation function is created with the movie name passed as an argument, we obtain the movie's similarity index, and using that we obtain the indices of similar movies and on using those indices in the original table
we obtain the movie title.

You can find the code [here](https://github.com/dachuvg/Movie-Recommendation-System/blob/main/Movie-Recommendation-System.ipynb)

## Client App
Streamlit, a cloud based deployment platform is used for the app creation and deployment. We use the TMDB API to fetch the movie posters. A selectbox is created with all the movie titles and a predict button which on clicking will 
give us the movie titles of similar movies.

Feel free to try the [app](https://movierecommender-bydarshanvg.streamlit.app/)

## Local Setup
All requirements are available [here](https://github.com/dachuvg/Movie-Recommendation-System/blob/main/requirements.txt)

## Screenshots
![pic1](https://github.com/dachuvg/Movie-Recommendation-System/blob/main/screenshots/pic1.png)
![pic2](https://github.com/dachuvg/Movie-Recommendation-System/blob/main/screenshots/pic2.png)
