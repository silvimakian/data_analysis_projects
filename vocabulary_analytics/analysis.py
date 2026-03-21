from func import(
    create_books,
    add_words,
    load_books,
    practice_session,
    choose_books
)
import json
import time
import os
import matplotlib.pyplot as plt

#analyze books
#hardest work

def analyze_sessions():
    with open("data/sessions.json", "r", encoding="utf-8") as f:
        sessions = json.load(f)
    session_count=0
    total_accuracy=0
    total_words=0
    total_time=0
    best_streak=0
    worst_streak = float('inf')
    total_streak=0
    total_speed = 0
    for session in sessions:
        session_count+=1
        total_accuracy+=session["accuracy"]
        total_words+=session["session_size"]
        total_time+=session["duration_seconds"]/60
        speed = session["session_size"] / (session["duration_seconds"] / 60)
        total_speed += speed
        total_streak+=session["longest_correct_streak"]
        if session["longest_correct_streak"]>best_streak:
            worst_streak=best_streak
            best_streak=session["longest_correct_streak"]
        elif session["longest_correct_streak"]<worst_streak:
            worst_streak=session["longest_correct_streak"]
        
    avg_speed = total_speed / session_count
    avg_streak=total_streak/session_count
    avg_accuracy=total_accuracy/session_count
    print("____________________________")
    print("General stats: ")
    print(f"Total sessions: {session_count}")
    print(f"Average accuracy: {avg_accuracy}")
    print(f"Total words practiced: {total_words}")
    print(f"Total study time: {round(total_time, 2)} minutes")
    print(f"Learning speed: {round(avg_speed), 2} words per minute")
    print("\n____________________________")
    print("Streak analysis: ")
    print(f"Best correct answer streak: {best_streak}")
    print(f"Worst correct answer streak: {worst_streak}")
    print(f"Average correct answer streak: {avg_streak}")
    print("\n____________________________")
    print("Learning progress: ")
    xpoints=[]
    ypoints=[]
    for index, session in enumerate(sessions, start=1):
        xpoints.append(index)
        ypoints.append(session["accuracy"])
        print(f"Session number {index}: {session['accuracy']}")
        
    plt.plot(xpoints, ypoints)
    plt.xlabel("Session number")
    plt.ylabel("Accuracy")
    plt.title("Learning progress")
    plt.grid(True)
    plt.show()

def hardest_words(path, data):
    
    hardest=sorted(data, key=lambda w: w["mistakes"], reverse=True)
    easiest=sorted(data, key=lambda w: w["mistakes"], reverse=False)
    print(f"\nTop three hardest words in {os.path.basename(path)}:\n ")
    for word in hardest[:3]:
        print(f"{word['word']} -- mistakes: {word['mistakes']}")

    print(f"\nTop three easiest words in {os.path.basename(path)}:\n ")
    for word in easiest[:3]:
        print(f"{word['word']} -- mistakes: {word['mistakes']}")
    
def recommend_words(words, n=5):

    hardest = sorted(words, key=lambda w: w["weight"], reverse=True)

    print("\nRecommended words to review:\n")

    for word in hardest[:n]:
        print(f"{word['word']} (weight: {word['weight']}, mistakes: {word['mistakes']})")

def book_analysis():
    path=choose_books()
    if path is None:
        return
    with open(path, "r", encoding="utf-8") as file:
        words=json.load(file)
        
    if not words:
        print("No words in this book")
        return
    mistakes=0
    correct=0
    mastered_words=0
    not_practice=0
    total_weight=0
    
    for word in words:
        total_weight+=word["weight"]
        mistakes+=word["mistakes"]
        correct+=word["correct"]
        if word["correct"]>=5 and word["mistakes"]<=2:
            mastered_words+=1
        elif word["correct"]==0 and word["mistakes"]==0:
            not_practice+=1
    
    if correct+mistakes==0:
        accuracy=0
    else:
        accuracy=correct/(correct+mistakes)
    progress = (mastered_words / len(words)) * 100
    print("__________________\n")
    print(f"Book analysis: {os.path.basename(path)}")
    print("__________________\n")
    print(f"Total words: {len(words)}")
    print(f"Total correct answers: {correct}")
    print(f"Total mistakes: {mistakes}")
    print(f"Book accuracy: {round(accuracy, 2)}")
    print(f"Mastered words: {mastered_words}/ {len(words)}")
    print(f"Learning progress: {round(progress, 2)} %")
    print(f"Words never practiced:{not_practice}")
    print(f"Average difficulty weight: {round(total_weight/(len(words)), 2)}")
    hardest_words(path, words)
    recommend_words(words)



