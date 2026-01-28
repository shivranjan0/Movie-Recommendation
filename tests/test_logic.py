import pytest
import pandas as pd
import numpy as np
from logic import get_movie_recommendations, validate_data_integrity

@pytest.fixture
def mock_data():
    """Provides a small mock dataset for testing."""
    movies_df = pd.DataFrame({
        'title': ['Movie A', 'Movie B', 'Movie C', 'Movie D']
    })
    # Simple similarity matrix: A is similar to B, C is similar to D
    # Diagonal is 1.0 (self-similarity)
    similarity_matrix = np.array([
        [1.0, 0.8, 0.2, 0.1], # A
        [0.8, 1.0, 0.1, 0.1], # B
        [0.2, 0.1, 1.0, 0.9], # C
        [0.1, 0.1, 0.9, 1.0], # D
    ])
    return movies_df, similarity_matrix

def test_recommendation_logic(mock_data):
    movies_df, similarity_matrix = mock_data
    
    # Test: Searching for Movie A should return Movie B as top recommendation
    recs, error = get_movie_recommendations('Movie A', movies_df, similarity_matrix, num_recommendations=1)
    
    assert error is None
    assert len(recs) == 1
    assert recs[0]['title'] == 'Movie B'
    assert recs[0]['similarity_score'] == 80.0

def test_movie_not_found(mock_data):
    movies_df, similarity_matrix = mock_data
    recs, error = get_movie_recommendations('Unknown Movie', movies_df, similarity_matrix)
    
    assert error == "Movie not found"
    assert len(recs) == 0

def test_data_integrity():
    valid_df = pd.DataFrame({'title': ['A', 'B']})
    invalid_df = pd.DataFrame({'name': ['A', 'B']})
    
    assert validate_data_integrity(valid_df) == True
    assert validate_data_integrity(invalid_df) == False

def test_num_recommendations(mock_data):
    movies_df, similarity_matrix = mock_data
    recs, _ = get_movie_recommendations('Movie A', movies_df, similarity_matrix, num_recommendations=2)
    assert len(recs) == 2
