from datetime import datetime

def return_book(cursor, connection, email):
    print("Your borrowings:")
    cursor.execute('''
                    SELECT bid, borrowings.book_id, title, start_date, start_date, end_date, IFNULL(end_date, DATE(JULIANDAY(start_date) + 20)) AS deadline
                    FROM borrowings, books
                    WHERE borrowings.book_id = books.book_id
                    AND borrowings.member LIKE :email
                    ''', {"email": email})
    borrowings = cursor.fetchall()

    print("\nYour borrowings:")
    for borrowing in borrowings:
        if borrowing['end_date'] == None:
            print(f"Borrow ID: {borrowing['bid']}, Title: {borrowing['title']}, Borrowing date: {borrowing['start_date']}, Deadline: {borrowing['deadline']}")
            end_date = datetime.strptime(borrowing['deadline'], "%Y-%m-%d")
        else:
            print(f"Borrow ID: {borrowing['bid']}, Title: {borrowing['title']}, Borrowing date: {borrowing['start_date']}")

    user_input = ""
    while borrowings and user_input.lower() != "no":
        user_input = input("Would you like to return a book? ")
        if user_input.lower() == "yes":
            valid_input = False
            while not valid_input:
                try:
                    borrow_id = input("Select the borrowing you would like to return: ")
                    if borrow_id == "quit":
                        valid_input = True
                    else:
                        borrow_id = int(borrow_id)
                        valid_input = True
                except:
                    print("Invalid input")

            borrow_index = None
            for i in range(len(borrowings)):
                if borrow_id == borrowings[i]['bid']:
                    borrow_index = i
                
            if borrow_index != None:
                if borrowings[borrow_index]['end_date'] == None:
                    cursor.execute('''
                                UPDATE borrowings
                                SET end_date = DATE()
                                WHERE bid = :borrow_id;
                                ''', {"borrow_id": borrow_id})
                    print("Book returned.")
                    connection.commit()
                    end_date = datetime.today()
                    start_date = datetime.strptime(borrowing['start_Date'], "%Y-%m-%d")
                    date_diff = abs((end_date - start_date).days)

                    if date_diff > 20:
                        print("You have returned this book", date_diff - 20, "days late, so you have been penalized", "$" + str(date_diff - 20))
                        cursor.execute('''
                                         SELECT IFNULL(MAX(pid), 0) + 1 AS pid
                                         FROM penalties''')
                        pid = cursor.fetchone()['pid']
                        cursor.execute('''
                                        INSERT INTO penalties VALUES
                                        (:pid, :borrow_id, :amount, NULL);
                                        ''', {"pid": pid, "borrow_id": borrowings[borrow_index]['bid'], "amount": date_diff - 20})
                        connection.commit()

                    review = input("Would you like to write a review for this book? ")
                    while review.lower() != "no" and review.lower() != "yes":
                        print("Invalid input")
                        review = input("Would you like to write a review for this book? ")

                    if review == "yes":
                        review = input("Enter your review: ")
                        stars = 0
                        while stars < 1 or stars > 5:
                            try:
                                stars = int(input("Enter number of stars: "))
                                if stars < 1 or stars > 5:
                                    print("Invalid number of stars")
                            except:
                                print("Invalid input")

                        cursor.execute('''
                                        SELECT IFNULL(MAX(rid), 0) + 1 AS rid
                                        FROM reviews''')
                        rid = cursor.fetchone()['rid']

                        cursor.execute('''
                                        INSERT INTO reviews VALUES
                                        (:rid, :book_id, :email, :stars, :review, DATE())
                                        ''', {"rid": rid, "book_id": borrowings[borrow_index]['book_id'], "email": email, "stars": stars, "review": review})
                        connection.commit()
                    else:
                        print("Borrowing was already returned")
                else:
                    print("Borrowing not found")

        print("Your borrowings:")
        cursor.execute('''
                        SELECT bid, borrowings.book_id, title, start_date, start_date, end_date, IFNULL(end_date, DATE(JULIANDAY(start_date) + 20)) AS deadline
                        FROM borrowings, books
                        WHERE borrowings.book_id = books.book_id
                        AND borrowings.member = :email
                        ''', {"email": email})
        borrowings = cursor.fetchall()

        for borrowing in borrowings:
            if borrowing['end_date'] == None:
                print(f"Borrow ID: {borrowing['bid']}, Title: {borrowing['title']}, Borrowing date: {borrowing['start_date']}, Deadline: {borrowing['deadline']}")
            else:
                print(f"Borrow ID: {borrowing['bid']}, Title: {borrowing['title']}, Borrowing date: {borrowing['start_date']}")

    if not borrowings:
        print("You have no borrowings")
    print("")
