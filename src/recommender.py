import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

MOOD_WEIGHT_POINTS = 45.0
DANCEABILITY_WEIGHT_POINTS = 35.0
SINGER_NOTORIETY_WEIGHT_POINTS = 20.0
TOTAL_WEIGHT_POINTS = MOOD_WEIGHT_POINTS + DANCEABILITY_WEIGHT_POINTS + SINGER_NOTORIETY_WEIGHT_POINTS

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    singer_notoriety: float = 0.5

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    preferred_danceability: Optional[float] = None
    preferred_singer_notoriety: float = 0.5

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(self.songs, key=lambda song: _score_for_user_profile(user, song), reverse=True)
        return ranked[:max(0, k)]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        target_danceability = user.preferred_danceability
        if target_danceability is None:
            target_danceability = user.target_energy

        breakdown = _score_breakdown(
            user_mood=user.favorite_mood,
            user_danceability=target_danceability,
            user_singer_notoriety=user.preferred_singer_notoriety,
            song_mood=song.mood,
            song_danceability=song.danceability,
            song_singer_notoriety=song.singer_notoriety,
        )

        return (
            f"Score {breakdown['score']:.2f}: "
            f"mood points={breakdown['mood_points']:.1f}/{MOOD_WEIGHT_POINTS:.0f}, "
            f"danceability points={breakdown['danceability_points']:.1f}/{DANCEABILITY_WEIGHT_POINTS:.0f}, "
            f"singer notoriety points={breakdown['singer_notoriety_points']:.1f}/{SINGER_NOTORIETY_WEIGHT_POINTS:.0f}"
        )


def _clamp_01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _to_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _score_breakdown(
    user_mood: object,
    user_danceability: object,
    user_singer_notoriety: object,
    song_mood: object,
    song_danceability: object,
    song_singer_notoriety: object,
) -> Dict[str, float]:
    mood_match = 1.0 if str(user_mood).strip().lower() == str(song_mood).strip().lower() else 0.0

    user_dance = _clamp_01(_to_float(user_danceability, 0.5))
    song_dance = _clamp_01(_to_float(song_danceability, 0.5))
    danceability_match = 1.0 - abs(song_dance - user_dance)

    user_notoriety = _clamp_01(_to_float(user_singer_notoriety, 0.5))
    song_notoriety = _clamp_01(_to_float(song_singer_notoriety, 0.5))
    singer_notoriety_match = 1.0 - abs(song_notoriety - user_notoriety)

    mood_points = MOOD_WEIGHT_POINTS * mood_match
    danceability_points = DANCEABILITY_WEIGHT_POINTS * _clamp_01(danceability_match)
    singer_notoriety_points = SINGER_NOTORIETY_WEIGHT_POINTS * _clamp_01(singer_notoriety_match)
    total_points = mood_points + danceability_points + singer_notoriety_points

    return {
        "mood_match": mood_match,
        "danceability_match": _clamp_01(danceability_match),
        "singer_notoriety_match": _clamp_01(singer_notoriety_match),
        "mood_points": mood_points,
        "danceability_points": danceability_points,
        "singer_notoriety_points": singer_notoriety_points,
        "points": total_points,
        "score": total_points / TOTAL_WEIGHT_POINTS,
    }


def _score_for_user_profile(user: UserProfile, song: Song) -> float:
    target_danceability = user.preferred_danceability
    if target_danceability is None:
        target_danceability = user.target_energy

    breakdown = _score_breakdown(
        user_mood=user.favorite_mood,
        user_danceability=target_danceability,
        user_singer_notoriety=user.preferred_singer_notoriety,
        song_mood=song.mood,
        song_danceability=song.danceability,
        song_singer_notoriety=song.singer_notoriety,
    )
    return breakdown["score"]


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a single song dictionary against a user preference dictionary.
    Uses mood, danceability, and singer notoriety as primary features.
    """
    breakdown = _score_breakdown(
        user_mood=user_prefs.get("mood", ""),
        user_danceability=user_prefs.get("danceability", user_prefs.get("energy", 0.5)),
        user_singer_notoriety=user_prefs.get("singer_notoriety", 0.5),
        song_mood=song.get("mood", ""),
        song_danceability=song.get("danceability", 0.5),
        song_singer_notoriety=song.get("singer_notoriety", 0.5),
    )

    explanation = (
        f"mood points={breakdown['mood_points']:.1f}/{MOOD_WEIGHT_POINTS:.0f}, "
        f"danceability points={breakdown['danceability_points']:.1f}/{DANCEABILITY_WEIGHT_POINTS:.0f}, "
        f"singer notoriety points={breakdown['singer_notoriety_points']:.1f}/{SINGER_NOTORIETY_WEIGHT_POINTS:.0f}"
    )
    return breakdown["score"], explanation

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            songs.append(dict(row))
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:max(0, k)]
