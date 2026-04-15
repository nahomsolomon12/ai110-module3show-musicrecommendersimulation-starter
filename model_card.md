# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.

 TuneMatch Lite.

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

What kind of recommendations does it generate?
 It suggests top songs from a small class dataset.

What assumptions does it make about the user?
 It assumes users can describe mood, danceability, and artist notoriety they want.

Is this for real users or classroom exploration?
 It is for classroom exploration and testing.

---

## 3. How the Model Works

Explain your scoring approach in simple language.

What features of each song are used (genre, energy, mood, etc.)?
 It uses mood, danceability, and singer notoriety.

What user preferences are considered?
 It uses favorite mood, preferred danceability, and preferred singer notoriety.

How does the model turn those into a score?
 Mood is a yes or no match. Danceability and notoriety use distance, so closer values score higher. The weighted points are mood 45, danceability 35, and singer notoriety 20.

What changes did you make from the starter logic?
 I made a clearer weighted scoring breakdown and explanation text for each recommendation.

---

## 4. Data

Describe the dataset the model uses.

How many songs are in the catalog?
 18 songs.

What genres or moods are represented?
 Genres include pop, lofi, rock, ambient, jazz, classical, house, hip hop, and more. Moods include happy, chill, intense, focused, relaxed, moody, and energetic.

Did you add or remove data?
 No. I used the provided dataset as is.

Are there parts of musical taste missing in the dataset?
 Yes. The dataset is small and misses many listening styles, languages, and cultures.

---

## 5. Strengths

Where does your system seem to work well?

User types for which it gives reasonable results?
 Users with clear mood and danceability targets.

Any patterns you think your scoring captures correctly?
 It captures mood alignment and closeness in danceability and artist notoriety.

Cases where the recommendations matched your intuition?
 The sample profiles (high-energy pop, chill lofi, and deep intense rock) gave intuitive top songs.

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Features it does not consider?
 It does not use lyrics, context, time of day, or listening history.

Genres or moods that are underrepresented?
 The small dataset means some genres and mood styles are underrepresented.

Cases where the system overfits to one preference?
 The strong mood weight can over-prioritize mood and hide good songs.

Ways the scoring might unintentionally favor some users?
 Singer notoriety can favor popular artists and reduce discovery of less known artists.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Which user profiles you tested?
 High-energy pop, chill lofi, and deep intense rock.

What you looked for in the recommendations?
 I checked if top songs matched each profile mood and danceability.

What surprised you?
 Genre preference is stored but does not directly affect final score.

Any simple tests or comparisons you ran?
 I used the unit tests for ranking order and non-empty explanation output.

---

## 8. Future Work

Ideas for how you would improve the model next.

Additional features or preferences?
 Add genre and energy directly to scoring.

Better ways to explain recommendations?
 Add short natural-language reasons for each recommendation.

Improving diversity among the top results?
 Add a diversity step so top songs are not too similar.

Handling more complex user tastes?
 Support mixed tastes, like different moods for study and workout.

---

## 9. Personal Reflection

A few sentences about your experience.

What you learned about recommender systems?
Way more complex than I assumed, I had to spend more time planning than I did executing. 

Something unexpected or interesting you discovered?
Small scoring changes can quickly change top recommendations.

How this changed the way you think about music recommendation apps?
It made me think more critically about bias and why certain songs get promoted.
