def get_profile(cursor, email):
    # Getting user information
    cursor.execute('''
                    SELECT name, email, byear
                    FROM members
                    WHERE members.email LIKE :email;
                    ''', {"email":email})
    user_data = cursor.fetchone()

    # Getting previous borrowings from the user
    cursor.execute('''
                    SELECT COUNT(*) AS previous_borrowings
                    FROM borrowings
                    WHERE member LIKE :email
                    AND end_date IS NOT NULL;
                    ''', {"email": email})
    previous_borrowings = cursor.fetchone()

    # Getting user's current borrowings
    cursor.execute('''
                    SELECT COUNT(*) AS current_borrowings
                    FROM borrowings
                    WHERE member LIKE :email
                    AND end_date IS NULL;
                    ''', {"email": email})
    current_borrowings = cursor.fetchone()

    # Getting user's overdue borrowings
    cursor.execute('''
                    SELECT COUNT(*) AS overdue_borrowings
                    FROM borrowings
                    WHERE member LIKE :email
                    AND end_date IS NULL
                    AND 20 > JULIANDAY(borrowings.start_date) - JULIANDAY(DATE());
                    ''', {"email": email})
    overdue_borrowings = cursor.fetchone()

    # Getting user's penalties
    cursor.execute('''
                    SELECT COUNT(*) AS penalties_count, IFNULL(SUM(amount), 0) AS penalties_sum
                    FROM penalties, borrowings
                    WHERE penalties.bid = borrowings.bid
                    AND borrowings.member LIKE :email
                    AND IFNULL(penalties.paid_amount, 0) < amount;
                    ''', {"email": email})
    penalties = cursor.fetchone()

    # Printing information about the user
    print(f"\nName: {user_data['name']}\nEmail: {user_data['email']}\nBirth year: {user_data['byear']}")
    print(f"Previous borrowings: {previous_borrowings['previous_borrowings']}")
    print(f"Current borrowings: {current_borrowings['current_borrowings']}")
    print(f"Overdue borrowings: {overdue_borrowings['overdue_borrowings']}")
    print(f"Penalties: {penalties['penalties_count']}")
    print(f"Penalties sum: {penalties['penalties_sum']}\n")
    return
