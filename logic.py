import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MovieRecLogic")

def get_movie_recommendations(movie_title, movies_df, similarity_matrix, num_recommendations=5):
    """
    Core logic for movie recommendations. 
    Separated from UI for testability.
    """
    if movies_df.empty or similarity_matrix is None:
        logger.error("Recommendation failed: Dataframes or similarity matrix not loaded.")
        return [], "Data not loaded"
        
    if movie_title not in movies_df['title'].values:
        logger.warning(f"Recommendation failed: Movie '{movie_title}' not found in database.")
        return [], "Movie not found"
    
    try:
        logger.info(f"Generating recommendations for: '{movie_title}'")
        movie_index = movies_df[movies_df['title'] == movie_title].index[0]
        distances = list(enumerate(similarity_matrix[movie_index]))
        # Sort by similarity score (x[1]) descending
        distances = sorted(distances, key=lambda x: x[1], reverse=True)
        
        recommended_movies = []
        # Skip the first one as it's the movie itself
        for i in distances[1:num_recommendations+1]:
            movie_data = {
                'title': movies_df.iloc[i[0]].title,
                'similarity_score': round(float(i[1]) * 100, 1)
            }
            recommended_movies.append(movie_data)
        
        logger.info(f"Successfully generated {len(recommended_movies)} recommendations for '{movie_title}'")
        return recommended_movies, None
    except Exception as e:
        logger.error(f"Unexpected error during recommendation: {str(e)}", exc_info=True)
        return [], f"Error: {str(e)}"

def validate_data_integrity(movies_df):
    """Checks if the dataframe has required columns."""
    required_columns = ['title']
    return all(col in movies_df.columns for col in required_columns)
