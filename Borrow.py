def borrow_book(book_id, member_email, connection, cursor):

    # Check if the book is available for borrowing
    cursor.execute("SELECT COUNT(*) FROM borrowings WHERE book_id = ? AND end_date IS NOT NULL", (book_id,))
    connection.commit()
    if cursor.fetchone()[0] > 0:
        print("Sorry, this book is already borrowed.\n")
        return

    # Assign a unique borrowing ID (bid)
    cursor.execute("SELECT MAX(bid) FROM borrowings")
    last_bid = cursor.fetchone()[0]
    if last_bid is None:
        bid = 1
    else:
        bid = last_bid + 1

    # Insert the borrowing record into the database
    cursor.execute("INSERT INTO borrowings (bid, member, book_id, start_date, end_date) VALUES (?, ?, ?, DATE(), NULL)",
                   (bid, member_email, book_id))
    connection.commit()
    print("You are now borrowing this book.\n")

    return
