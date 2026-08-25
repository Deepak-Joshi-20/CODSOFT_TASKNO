"""
Automated tests for recommender.py
Run with:  python -m pytest test_recommender.py -v
       or:  python test_recommender.py
"""

import unittest
from recommender import (
    cosine_similarity,
    movie_genre_vector,
    content_based_recommend,
    find_similar_users,
    collaborative_recommend,
    MOVIES,
    USER_RATINGS,
)


class TestCosineSimilarity(unittest.TestCase):

    def test_identical_vectors_similarity_is_one(self):
        v = [1, 2, 3]
        self.assertAlmostEqual(cosine_similarity(v, v), 1.0)

    def test_orthogonal_vectors_similarity_is_zero(self):
        self.assertAlmostEqual(cosine_similarity([1, 0], [0, 1]), 0.0)

    def test_zero_vector_returns_zero_not_error(self):
        self.assertEqual(cosine_similarity([0, 0, 0], [1, 2, 3]), 0.0)

    def test_mismatched_length_raises(self):
        with self.assertRaises(ValueError):
            cosine_similarity([1, 2], [1, 2, 3])

    def test_opposite_direction_is_less_than_identical(self):
        a = [1, 1, 0]
        b = [1, 1, 1]
        sim_partial = cosine_similarity(a, b)
        self.assertTrue(0 < sim_partial < 1)


class TestContentBasedFiltering(unittest.TestCase):

    def test_genre_vector_length_matches_all_genres(self):
        from recommender import ALL_GENRES
        vec = movie_genre_vector("The Matrix")
        self.assertEqual(len(vec), len(ALL_GENRES))

    def test_unknown_movie_raises(self):
        with self.assertRaises(ValueError):
            content_based_recommend("A Movie That Does Not Exist")

    def test_similar_scifi_movies_are_recommended(self):
        results = content_based_recommend("The Matrix")
        recommended_titles = [m for m, _ in results]
        # Inception and Interstellar share the Sci-Fi genre with The Matrix
        self.assertTrue(
            "Inception" in recommended_titles or "Interstellar" in recommended_titles
        )

    def test_recommendations_never_include_the_query_movie_itself(self):
        results = content_based_recommend("Toy Story")
        titles = [m for m, _ in results]
        self.assertNotIn("Toy Story", titles)

    def test_results_sorted_descending_by_similarity(self):
        results = content_based_recommend("The Dark Knight")
        scores = [s for _, s in results]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_top_n_is_respected(self):
        results = content_based_recommend("The Matrix", top_n=2)
        self.assertLessEqual(len(results), 2)

    def test_every_movie_in_catalog_can_be_queried_without_error(self):
        # Fool-proofing: make sure no movie in the catalog crashes the function
        for movie in MOVIES:
            results = content_based_recommend(movie)
            self.assertIsInstance(results, list)


class TestCollaborativeFiltering(unittest.TestCase):

    def test_unknown_user_raises_for_similarity(self):
        with self.assertRaises(ValueError):
            find_similar_users("NotARealUser")

    def test_unknown_user_raises_for_recommendation(self):
        with self.assertRaises(ValueError):
            collaborative_recommend("NotARealUser")

    def test_similar_users_excludes_self(self):
        results = find_similar_users("Deepak")
        users = [u for u, _ in results]
        self.assertNotIn("Deepak", users)

    def test_sci_fi_fans_are_similar(self):
        # Deepak and Neha both love Sci-Fi movies -> should be similar
        results = find_similar_users("Deepak")
        top_user = results[0][0]
        self.assertIn(top_user, ("Ankit", "Neha"))

    def test_recommendations_exclude_already_rated_movies(self):
        results = collaborative_recommend("Deepak")
        recommended_titles = [m for m, _ in results]
        already_rated = set(USER_RATINGS["Deepak"].keys())
        self.assertTrue(already_rated.isdisjoint(recommended_titles))

    def test_results_sorted_descending_by_predicted_score(self):
        results = collaborative_recommend("Deepak")
        scores = [s for _, s in results]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_every_user_can_be_queried_without_error(self):
        # Fool-proofing: make sure no user in the DB crashes the function
        for user in USER_RATINGS:
            results = collaborative_recommend(user)
            self.assertIsInstance(results, list)

    def test_predicted_scores_within_valid_rating_range(self):
        # Since ratings are 1-5, predicted (weighted-average) scores must be too
        for user in USER_RATINGS:
            for movie, score in collaborative_recommend(user):
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
