from preprocessing import (
    tokenize, load_stopwords, calculate_tf,
    calculate_idf, calculate_cosine_similarity
)
import pandas as pd

data = pd.read_csv("books.csv")

corpus_tokens = []
stopwords = load_stopwords()

for idx, row in data.iterrows():
    text = f"{row['Title']} {row['Author']} {row['genres']}"
    tokens = tokenize(text)
    tokens = [t for t in tokens if t not in stopwords]
    corpus_tokens.append(tokens)

idf_scores = calculate_idf(corpus_tokens)
tfidf_vectors = []

for tokens in corpus_tokens:
    tf = calculate_tf(tokens)
    tfidf = {word: tf_val * idf_scores.get(word, 0) for word, tf_val in tf.items()}
    tfidf_vectors.append(tfidf)

def recommend_books(book_title, top_n=5):
    book_title = book_title.lower()

    matches = data[data["Title"].str.lower() == book_title]

    if matches.empty:
        print("\n Book not found in dataset!")
        return

    book_index = matches.index[0]
    target_vector = tfidf_vectors[book_index]

    print(f"\n Finding books similar to: {matches.iloc[0]['Title']}")

    similarities = []

    for i, other_vector in enumerate(tfidf_vectors):
        if i == book_index:
            continue
        score = calculate_cosine_similarity(target_vector, other_vector)
        similarities.append((i, score))

    similarities.sort(key=lambda x: x[1], reverse=True)

    print(f" Top {top_n} recommendations:\n")
    for idx, score in similarities[:top_n]:
        print(f"- {data.iloc[idx]['Title']} (score: {round(score, 4)})")

while True:
    print("\n--- MENU ---")
    print("1. Get book recommendations")
    print("0. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        title = input("Enter a book title: ")
        recommend_books(title)

    elif choice == "0":
        print("Goodbye!")
        break

    else:
        print("Invalid choice, try again.")