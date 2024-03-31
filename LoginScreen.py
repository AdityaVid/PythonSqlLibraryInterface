import getpass

def login_screen(cursor):
    """
    Provide a login interface for users.

    Args:
    - cursor (sqlite3.Cursor): Cursor object to interact with the database.
    """
    while True:
        user_email = input("Enter Email address: ")
        if user_email == "quit":
            user_email = False
            break
        user_password = getpass.getpass("Enter Password: ")
        cursor.execute('SELECT * FROM members WHERE email LIKE ? AND passwd = ?;', (user_email, user_password))
        if cursor.fetchone():
            print("Login Successful")
            break
        else:
            print("Incorrect username or password, please try again or type 'quit' to cancel login")

    return user_email
