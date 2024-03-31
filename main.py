import CreateTablesScript
import LoginScreen
import SignUp
import GetProfile
import PayPenalty
import ReturnBook
import Search
import Borrow
import sys
import sqlite3
from getpass import getpass

connection = None
cursor = None

db_name = sys.argv

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

def main():
    """
    main
    """
    global cursor, connection
    
    connect(db_name[1])
    CreateTablesScript.define_tables(cursor, connection)
    
    logged_in = False
    while True:
        while not logged_in:
            user_input = input("Type 'login' if you are a returning user, 'register' to make a new account, or 'exit' to exit the program: ")
            if user_input.lower() in {"login", "register"}:
                if user_input.lower() == "login":
                    user_name = LoginScreen.login_screen(cursor)
                elif user_input.lower() == "register":
                    user_name = SignUp.sign_up(cursor, connection)
                if user_name:
                    logged_in = True
            elif user_input.lower() == "exit":
                connection.close()
                return
            else:
                print("Incorrect input, try again")
        while logged_in:
            print(f"Logged in as {user_name}: ")
            print("Main menu: \n 1. Profile \n 2. Check borrowings \n 3. Search \n 4. Borrow \n 5. Penalties \n 6. Log out \n 7. Quit")
            user_input = input("Enter a number: ")
            if user_input.lower() == "1":
                GetProfile.get_profile(cursor, user_name)
            elif user_input.lower() == "2":
                ReturnBook.return_book(cursor, connection, user_name)
                
            elif user_input == "3":
                user_search_keyword = input("Search for title or author name: ")
                Search.search_books(user_search_keyword, cursor, connection, 1)

            elif user_input == "4":
                user_search_book = input("Search for book using book ID: ")
                Borrow.borrow_book(user_search_book, user_name, connection, cursor)

            elif user_input.lower() == "5":
                PayPenalty.pay_penalty(cursor, connection, user_name)

            elif user_input.lower() == "6":
                logged_in = False

            elif user_input.lower() == "7":
                connection.close()
                return
            else:
                print("Unknown command")
    connection.close()
    return

main()
