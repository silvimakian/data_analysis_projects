from func import(
    create_books,
    add_words,
    load_books,
    practice_session,
    train_model
)

from analysis import (
    analyze_sessions,
    book_analysis
                      )

while True:
    print("------Menu------")
    print("1. Practice")
    print("2. Create new book")
    print("3. View the books")
    print("4. Add words")
    print("5. Session analysis")
    print("6. Exit")
    model = train_model()
    choice = 0
    while choice < 1 or choice > 6:
        try:
            choice = int(input("Enter the number of what you want to do (1-6): "))
            if choice < 1 or choice > 6:
                print("Please pick a number between 1 and 5.")
        except ValueError:
            print("That's not a number! Try again.")
    if choice==1:
        practice_session(model)
    elif choice==2:
        print(create_books())
    elif choice==3:
        print(load_books())
    elif choice==4:
        print(add_words())
    elif choice==5:
        while True:
            print("------Sub-menu------")
            print("1. Session Stats ")
            print("2. Book Stats")
            print("3. Exit")
            sub_choice = 0
            while sub_choice < 1 or sub_choice > 3:
                try:
                    sub_choice = int(input("Enter the number of what you want to do (1-3): "))
                    if sub_choice < 1 or sub_choice > 3:
                        print("Please pick a number between 1 and 3.")
                except ValueError:
                    print("That's not a number! Try again.")
            if sub_choice==1:
                print(analyze_sessions())
            if sub_choice==2:
                print(book_analysis())
            if sub_choice==3:
                break

    elif choice==6:
       break



