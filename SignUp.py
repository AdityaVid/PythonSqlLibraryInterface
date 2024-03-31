import getpass

def sign_up(cursor, connection):
    cursor.execute('''
                SELECT *
                FROM members;
                ''')
    users = cursor.fetchall()

    unique_email = False
    while not unique_email:
        unique_email = True
        email = input("Enter your email: ")
        for user in users:
            if email == user["email"]:
                print("Email is already in use, please use another email.")
                unique_email = False

    uname = input("Enter your name: ")
    byear = input("Enter your birth year: ")
    fname = input("Enter your faculty: ")
    pword = getpass.getpass("Enter your password: ")

    cursor.execute('''
        INSERT INTO members(email, passwd, name, byear, faculty) VALUES
        (:email, :pword, :uname, :byear, :fname)
        ''', {"email": email, "pword":pword, "uname":uname, "byear":byear, "fname":fname})

    connection.commit()
    return email
