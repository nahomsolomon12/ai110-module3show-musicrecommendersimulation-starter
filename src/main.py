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


PROFILES = {
    "1": {
        "name": "High-Energy Pop",
        "prefs": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.88,
            "danceability": 0.90,
            "singer_notoriety": 0.85,
        },
    },
    "2": {
        "name": "Chill Lofi",
        "prefs": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.38,
            "danceability": 0.58,
            "singer_notoriety": 0.52,
        },
    },
    "3": {
        "name": "Deep Intense Rock",
        "prefs": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "danceability": 0.62,
            "singer_notoriety": 0.78,
        },
    },
    "4": {
        "name": "Ambiguous Mix (Skew Test)",
        "prefs": {
            "genre": "mixed",
            "mood": "mixed",
            "energy": 0.55,
            "danceability": 0.72,
            "singer_notoriety": 0.98,
        },
    },
}


def choose_profile() -> dict:
    """Prompt for one of the predefined profiles and return its preference dictionary."""
    print("\nChoose a profile:")
    print("1. High-Energy Pop")
    print("2. Chill Lofi")
    print("3. Deep Intense Rock")
    print("4. Ambiguous Mix (Skew Test)")

    choice = input("Enter 1, 2, 3, or 4 (default 1): ").strip()
    if choice not in PROFILES:
        choice = "1"

    selected = PROFILES[choice]
    print(f"Using profile: {selected['name']}")
    return selected["prefs"]


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    songs_csv = project_root / "data" / "songs.csv"
    songs = load_songs(str(songs_csv))
    print(f"Loaded songs: {len(songs)}")

    user_prefs = choose_profile()

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for index, rec in enumerate(recommendations, start=1):
        song, score, _ = rec
        total_points = score * 100
        print(f"{index}. {song['title']} ({total_points:.1f} pts)")


if __name__ == "__main__":
    main()
