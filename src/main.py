"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from pathlib import Path

try:
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    songs_csv = project_root / "data" / "songs.csv"
    songs = load_songs(str(songs_csv))
    print(f"Loaded songs: {len(songs)}")

    # Static target profile for repeatable recommendations
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.78,
        "danceability": 0.82,
        "singer_notoriety": 0.75,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for index, rec in enumerate(recommendations, start=1):
        song, score, _ = rec
        total_points = score * 100
        print(f"{index}. {song['title']} ({total_points:.1f} pts)")


if __name__ == "__main__":
    main()
