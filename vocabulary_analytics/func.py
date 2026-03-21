
import json
import os
import random
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def choose_books():
    folder_path="data/books"
    files=[f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print("Select a book: ")
    for index, filename in enumerate(files, start=1):
        print(f"{index}. {filename}")
    choice=int(input("Enter the number of book: "))
    if choice < 1 or choice > len(files):
        print("Invalid choice")
        return
    selected_book=files[choice-1]
    path=os.path.join(folder_path, selected_book)
    return path

def create_books():
    book_name=input("Name your vocabulary book: ").lower()
    path=f"data/books/{book_name}.json"

    if os.path.exists(path):
        print("This book already exists")
        return
    
    with open(path, "w") as file:
        json.dump([], file)
    print("The book was added to yor collection successfully")


def add_words():
    path=choose_books()
    if path is None:
        return
    
    ask='yes'

    while ask == 'yes':
        new_word=input("Input the new word: ")
        translation=input("Input the new words translation or defintion: ")
    
        with open(path, "r") as file:
            words = json.load(file)
        word_data = {
            "word": new_word,
             "translation": translation,
            "correct": 0,
            "mistakes": 0,
            "weight":1
        }
        words.append(word_data)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(words, file, indent=4, ensure_ascii=False)
        print(f"new word successfully appended to {path}")
        ask=input("Want to add a new word?(yes/no): ").lower()
        if ask=='no':
            break


def load_books():
    path=choose_books()
    if path is None:
        return
    with open(path, "r", encoding="utf-8") as file:
        data=json.load(file)
    for item in data:
        print(f"{item['word']}:{item['translation']} ")




def build_ml_dataset():
    sessions_path = "data/sessions.json"
    if not os.path.exists(sessions_path):
        print("No sessions found!")
        return None, None, None, None

    with open(sessions_path, "r", encoding="utf-8") as f:
        sessions = json.load(f)

    data = []
    labels = []

    for session in sessions:
        features = {
            "session_size": session["session_size"],
            "accuracy": session["accuracy"],
            "longest_correct_streak": session["longest_correct_streak"],
            "longest_mistake_streak": session["longest_mistake_streak"],
            "time_seconds": session.get("time_seconds", 0)
        }
        data.append(features)
        labels.append(1 if session["accuracy"] >= 0.8 else 0)

    if not data:
        print("Dataset empty!")
        return None, None, None, None

    df = pd.DataFrame(data)
    X_train, X_test, y_train, y_test = train_test_split(df, labels, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


def train_model():
    X_train, X_test, y_train, y_test = build_ml_dataset()
    if X_train is None:
        return None
    model = LogisticRegression()
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    print(f"ML model trained! Test accuracy: {acc}")
    return model

def practice_session(model=None):
    path = choose_books() 
    if path is None:
        return

    with open(path, "r", encoding="utf-8") as f:
        words = json.load(f)
    if not words:
        print("No words in this book")
        return

    
    planned_size = int(input("How many words for this session? "))
    avg_correct_streak = sum(w.get("correct",0) for w in words) / len(words)
    avg_mistake_streak = sum(w.get("mistakes",0) for w in words) / len(words)
    avg_accuracy = sum(w.get("correct",0) for w in words) / max(1, sum(w.get("correct",0)+w.get("mistakes",0) for w in words))
    features = pd.DataFrame([{
        "session_size": planned_size,
        "accuracy": avg_accuracy,
        "longest_correct_streak": avg_correct_streak,
        "longest_mistake_streak": avg_mistake_streak,
        "time_seconds": planned_size * 5  
    }])

    if model:
        predicted_success = model.predict(features)[0]
        if predicted_success == 0:
            print("ML suggests this session might be hard, reducing size by half...")
            planned_size = max(3, planned_size // 2)
        else:
            print("ML predicts session will be fine!")

    mistakes = 0
    correct = 0
    while mistakes < 3 and correct + mistakes < planned_size:
        word = random.choice(words)
        if random.choice([True, False]):
            question = word["word"]
            answer = word["translation"]
        else:
            question = word["translation"]
            answer = word["word"]

        user_answer = input(f"Translate/Match: {question} ---> ").strip().lower()
        if user_answer == answer.lower():
            print("Correct!")
            word["correct"] = word.get("correct",0) + 1
            correct += 1
        else:
            print(f"Wrong! Correct: {answer}")
            word["mistakes"] = word.get("mistakes",0) + 1
            mistakes += 1

    print(f"Session ended. Correct: {correct}, Mistakes: {mistakes}")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=4, ensure_ascii=False)

    session_data = {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "book": os.path.basename(path),
        "accuracy": round(correct/(correct+mistakes) if (correct+mistakes)>0 else 0,2),
        "mistakes": mistakes,
        "correct": correct,
        "longest_correct_streak": correct,
        "longest_mistake_streak": mistakes,
        "session_size": correct + mistakes,
        "time_seconds": planned_size*5 
    }

    sessions_path = "data/sessions.json"
    if os.path.exists(sessions_path):
        with open(sessions_path, "r", encoding="utf-8") as f:
            sessions = json.load(f)
    else:
        sessions = []

    sessions.append(session_data)
    with open(sessions_path, "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=4, ensure_ascii=False)