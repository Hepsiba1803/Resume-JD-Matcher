from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_score(text1: str, text2: str) -> float:
    """
    Calculate the cosine similarity score between two text strings.

    Args:
        text1 (str): The first text string.
        text2 (str): The second text string.

    Returns:
        float: The cosine similarity score between the two texts, ranging from 0.0 to 1.0.
    """
    if not isinstance(text1, str) or not isinstance(text2, str):
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    
    # Calculate cosine similarity
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    return similarity_score if similarity_score is not None else 0.0
