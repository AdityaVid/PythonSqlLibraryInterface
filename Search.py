def search_books(keyword, cursor, connection, page):
    offset = (page-1) * 5

    # Retrieve books with title matching the keyword
    cursor.execute("""
       SELECT 
            b.book_id, 
            b.title, 
            b.author, 
            b.pyear, 
            AVG(r.rating) AS avg_rating, 
            (COUNT(borrowings.bid) = 0 OR COUNT(borrowings.bid) IS NULL) AS available
        FROM 
            books b
        LEFT JOIN 
            reviews r ON b.book_id = r.book_id
        LEFT JOIN 
            borrowings ON b.book_id = borrowings.book_id AND borrowings.end_date > DATE('now')
        WHERE 
            b.title LIKE ? OR b.author LIKE ?
        GROUP BY 
            b.book_id
        LIMIT 5 OFFSET ?;
    """, ('%' + keyword + '%', '%' + keyword + '%', offset))

    results = cursor.fetchall()

    # Display the results
    for book in results:
        book_id, title, author, pyear, avg_rating, available = book
        avg_rating = round(avg_rating, 2) if avg_rating is not None else "N/A"
        print(f"Book ID: {book_id}, Title: {title}, Author: {author}, Publish Year: {pyear}, "
              f"Average Rating: {avg_rating}, Available: {available}")

    # Check if there are more results
    cursor.execute("""
        SELECT COUNT(*) 
        FROM (
            SELECT b.book_id
            FROM books b
            LEFT JOIN reviews r ON b.book_id = r.book_id
            WHERE b.title LIKE ? 
            GROUP BY b.book_id
            UNION
            SELECT b.book_id
            FROM books b
            LEFT JOIN reviews r ON b.book_id = r.book_id
            WHERE b.author LIKE ? 
            GROUP BY b.book_id
        ) AS total_results;
    """, ('%' + keyword + '%', '%' + keyword + '%'))

    total_results = cursor.fetchone()[0]
    
    if total_results > page * 5:
        print("There are more results. Type 'more' to see more results.")
        user_input = input("Type 'more' to see more results, or press any key to exit: ")
        if user_input.lower() == 'more':
            page += 1
            search_books(keyword, cursor, connection, page)
    
    return
