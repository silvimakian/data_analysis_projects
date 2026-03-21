import string
import re
import math
from collections import Counter
import pandas as pd

def clean_data(text):
    clean_text = text.lower()
    translator = str.maketrans('', '', string.punctuation)
    clean_text = clean_text.translate(translator)
    new_text = re.sub(r'[^a-zA-Z0-9]', ' ', clean_text)
    final_text = re.sub(r'\s+', ' ', new_text)
    return final_text

def tokenize(text):
    clean_text = clean_data(text)
    return clean_text.split()

def load_stopwords(filepath="stopwords.txt"):
    with open(filepath, 'r') as f:
        stopwords = {line.strip() for line in f if line.strip()}
    return stopwords

def remove_stopwords(tokens, stopwords):
    return [t for t in tokens if t not in stopwords]

def calculate_tf(tokens):
    token_counts = Counter(tokens)
    length = len(tokens) if len(tokens) > 0 else 1
    return {word: count / length for word, count in token_counts.items()}

def calculate_idf(corpus_tokens):
    N = len(corpus_tokens)
    idf_scores = {}
    all_unique = set(word for doc in corpus_tokens for word in doc)

    for word in all_unique:
        doc_count = sum(1 for doc in corpus_tokens if word in doc)
        idf_scores[word] = math.log((N + 1) / (doc_count + 1)) + 1

    return idf_scores

def calculate_cosine_similarity(vec1, vec2):
    dot = 0
    for word, value in vec1.items():
        if word in vec2:
            dot += value * vec2[word]

    mag1 = math.sqrt(sum(v*v for v in vec1.values()))
    mag2 = math.sqrt(sum(v*v for v in vec2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return dot / (mag1 * mag2)

df=pd.read_csv("books.csv")
df.sample(n=1000).to_csv("small_data.csv", index=False)