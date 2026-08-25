"""
CODSOFT_TASKSNO - Task 4: Recommendation System
Author: Deepak Joshi (0251CYS023)

A movie recommendation system implementing TWO classic approaches from
scratch (no external ML library needed - pure Python, so it always runs):

1. Content-Based Filtering
   Recommends movies similar to a movie the user likes, based on
   genre overlap (cosine similarity over genre vectors).

2. Collaborative Filtering (user-based)
   Recommends movies liked by OTHER users whose ratings closely
   match the target user's ratings (cosine similarity over rating
   vectors), i.e. "users like you also enjoyed...".

A small built-in dataset of movies/genres/ratings is included so the
script is fully self-contained and demoable with zero setup.

Concepts demonstrated:
    - Vector representation of items/users
    - Cosine similarity
    - Content-based filtering
    - User-based collaborative filtering
"""

import math
from typing import Dict, List, Tuple


# ----------------------------------------------------------------------
# Sample dataset
# ----------------------------------------------------------------------
MOVIES: Dict[str, List[str]] = {
    "The Matrix":            ["Sci-Fi", "Action"],
    "Inception":              ["Sci-Fi", "Thriller"],
    "Interstellar":           ["Sci-Fi", "Drama"],
    "The Dark Knight":        ["Action", "Crime", "Drama"],
    "John Wick":               ["Action", "Thriller"],
    "The Notebook":           ["Romance", "Drama"],
    "La La Land":             ["Romance", "Musical"],
    "Toy Story":              ["Animation", "Family", "Comedy"],
    "Shrek":                  ["Animation", "Comedy", "Family"],
    "The Conjuring":          ["Horror", "Thriller"],
    "Get Out":                ["Horror", "Thriller"],
    "Superbad":                ["Comedy"],
    "The Hangover":           ["Comedy"],
}

# Ratings on a 1-5 scale; a missing entry means "not rated / not watched"
USER_RATINGS: Dict[str, Dict[str, float]] = {
    "Deepak":  {"The Matrix": 5, "Inception": 5, "Interstellar": 4, "John Wick": 4},
    "Ankit":   {"The Matrix": 4, "Inception": 5, "The Dark Knight": 5, "John Wick": 5},
    "Priya":   {"The Notebook": 5, "La La Land": 4, "Toy Story": 3},
    "Riya":    {"Toy Story": 5, "Shrek": 5, "Superbad": 4},
    "Karan":   {"The Conjuring": 5, "Get Out": 4, "John Wick": 3},
    "Neha":    {"The Matrix": 5, "Interstellar": 5, "Inception": 4, "The Dark Knight": 4},
}

ALL_GENRES: List[str] = sorted({g for genres in MOVIES.values() for g in genres})


# ----------------------------------------------------------------------
# Vector math helpers (pure Python - no numpy required)
# ----------------------------------------------------------------------
def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Standard cosine similarity between two equal-length vectors.
    Returns 0.0 if either vector has zero magnitude (avoids div-by-zero).
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must be the same length.")

    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))

    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def movie_genre_vector(movie: str) -> List[float]:
    """One-hot style vector: 1.0 for each genre this movie has."""
    genres = MOVIES.get(movie, [])
    return [1.0 if g in genres else 0.0 for g in ALL_GENRES]


# ----------------------------------------------------------------------
# 1) Content-Based Filtering
# ----------------------------------------------------------------------
def content_based_recommend(liked_movie: str, top_n: int = 5) -> List[Tuple[str, float]]:
    """Recommend movies most similar to `liked_movie` by genre overlap."""
    if liked_movie not in MOVIES:
        raise ValueError(f"'{liked_movie}' is not in the movie catalog.")

    target_vec = movie_genre_vector(liked_movie)
    scores = []
    for movie in MOVIES:
        if movie == liked_movie:
            continue
        sim = cosine_similarity(target_vec, movie_genre_vector(movie))
        if sim > 0:
            scores.append((movie, round(sim, 3)))

    scores.sort(key=lambda pair: pair[1], reverse=True)
    return scores[:top_n]


# ----------------------------------------------------------------------
# 2) User-Based Collaborative Filtering
# ----------------------------------------------------------------------
def _user_rating_vector(user: str) -> List[float]:
    """Vector of this user's ratings across ALL known movies (0 if unrated)."""
    ratings = USER_RATINGS.get(user, {})
    return [ratings.get(movie, 0.0) for movie in MOVIES]


def find_similar_users(target_user: str, top_n: int = 3) -> List[Tuple[str, float]]:
    if target_user not in USER_RATINGS:
        raise ValueError(f"'{target_user}' is not in the user database.")

    target_vec = _user_rating_vector(target_user)
    similarities = []
    for user in USER_RATINGS:
        if user == target_user:
            continue
        sim = cosine_similarity(target_vec, _user_rating_vector(user))
        similarities.append((user, round(sim, 3)))

    similarities.sort(key=lambda pair: pair[1], reverse=True)
    return similarities[:top_n]


def collaborative_recommend(target_user: str, top_n: int = 5,
                             neighbor_count: int = 3) -> List[Tuple[str, float]]:
    """Recommend movies the target user hasn't rated yet, weighted by how
    similar each rating neighbor is and how highly they rated each movie.
    """
    if target_user not in USER_RATINGS:
        raise ValueError(f"'{target_user}' is not in the user database.")

    neighbors = find_similar_users(target_user, top_n=neighbor_count)
    already_rated = set(USER_RATINGS[target_user].keys())

    # weighted_score[movie] = sum(similarity * neighbor_rating) over neighbors
    weighted_scores: Dict[str, float] = {}
    weight_totals: Dict[str, float] = {}

    for neighbor, similarity in neighbors:
        if similarity <= 0:
            continue
        for movie, rating in USER_RATINGS[neighbor].items():
            if movie in already_rated:
                continue
            weighted_scores[movie] = weighted_scores.get(movie, 0.0) + similarity * rating
            weight_totals[movie] = weight_totals.get(movie, 0.0) + similarity

    predictions = [
        (movie, round(weighted_scores[movie] / weight_totals[movie], 3))
        for movie in weighted_scores
        if weight_totals[movie] > 0
    ]
    predictions.sort(key=lambda pair: pair[1], reverse=True)
    return predictions[:top_n]


# ----------------------------------------------------------------------
# Demo / CLI
# ----------------------------------------------------------------------
def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def run_demo():
    print_header("CONTENT-BASED FILTERING")
    liked = "Inception"
    print(f"Because you liked: {liked}")
    for movie, score in content_based_recommend(liked):
        print(f"  -> {movie:<20} (similarity: {score})")

    print_header("USER-BASED COLLABORATIVE FILTERING")
    target_user = "Deepak"
    similar = find_similar_users(target_user)
    print(f"Users most similar to {target_user}:")
    for user, score in similar:
        print(f"  -> {user:<10} (similarity: {score})")

    print(f"\nRecommended for {target_user} (based on similar users' tastes):")
    for movie, score in collaborative_recommend(target_user):
        print(f"  -> {movie:<20} (predicted score: {score})")


def run_interactive():
    print("Recommendation System - choose a mode:")
    print("  1) Content-based (recommend movies similar to one you like)")
    print("  2) Collaborative (recommend movies based on similar users)")
    print("  3) Run built-in demo for both")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        print(f"\nAvailable movies: {', '.join(MOVIES)}")
        movie = input("Enter a movie you like: ").strip()
        try:
            results = content_based_recommend(movie)
            if not results:
                print("No similar movies found.")
            for m, s in results:
                print(f"  -> {m:<20} (similarity: {s})")
        except ValueError as e:
            print(f"Error: {e}")

    elif choice == "2":
        print(f"\nAvailable users: {', '.join(USER_RATINGS)}")
        user = input("Enter a user name: ").strip()
        try:
            results = collaborative_recommend(user)
            if not results:
                print("No recommendations available (not enough overlapping data).")
            for m, s in results:
                print(f"  -> {m:<20} (predicted score: {s})")
        except ValueError as e:
            print(f"Error: {e}")

    else:
        run_demo()


if __name__ == "__main__":
    run_interactive()
