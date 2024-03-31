import sqlite3
import time
import hashlib

def drop_all_tables(cursor, connection):

    drop_all=    '''drop table if exists reviews;
                    drop table if exists penalties;
                    drop table if exists borrowings;
                    drop table if exists books;
                    drop table if exists members;
                    '''
    cursor.executescript(drop_all)

    connection.commit()

    return

def define_tables(cursor, connection):

    members_query=   '''
                        CREATE TABLE IF NOT EXISTS members (
                                email CHAR(100),
                                passwd CHAR(100),
                                name CHAR(255) NOT NULL,
                                byear INTEGER,
                                faculty CHAR(100),
                                PRIMARY KEY (email)
                                );
                    '''

    books_query=  '''
                        CREATE TABLE IF NOT EXISTS books (
                                book_id INTEGER,
                                title CHAR(255),
                                author CHAR(150),
                                pyear INTEGER,
                                PRIMARY KEY (book_id)
                                );
                    '''

    borrowings_query= '''
                    CREATE TABLE IF NOT EXISTS borrowings(
                            bid INTEGER,
                            member CHAR(100) NOT NULL,
                            book_id INTEGER NOT NULL,
                            start_date DATE NOT NULL,
                            end_date DATE,
                            PRIMARY KEY (bid),
                            FOREIGN KEY (member) REFERENCES members(email),
                            FOREIGN KEY (book_id) REFERENCES books(book_id)
                            );
                '''
    
    penalties_query='''
                    CREATE TABLE IF NOT EXISTS penalties(
                            pid INTEGER,
                            bid INTEGER NOT NULL,
                            amount INTEGER NOT NULL,
                            paid_amount INTEGER,
                            PRIMARY KEY (pid),
                            FOREIGN KEY (bid) REFERENCES borrowings(bid)
                            );
                '''
    
    reviews_query= '''
                    CREATE TABLE IF NOT EXISTS reviews(
                            rid INTEGER,
                            book_id INTEGER NOT NULL,
                            member CHAR(100) NOT NULL,
                            rating INTEGER NOT NULL,
                            rtext CHAR(255),
                            rdate DATE,
                            PRIMARY KEY (rid),
                            FOREIGN KEY (member) REFERENCES members(email),
                            FOREIGN KEY (book_id) REFERENCES books(book_id)
                            );
                '''

    cursor.execute(members_query)
    cursor.execute(books_query)
    cursor.execute(borrowings_query)
    cursor.execute(penalties_query)
    cursor.execute(reviews_query)
    connection.commit()

    return

def add_data(cursor, connection):
    cursor.executescript('''
                        INSERT OR IGNORE INTO members VALUES
                        ('dave@ualberta.ca', 'a', 'Dave', 1980, 'CS'),
                        ('john@ualberta.ca', 'b', 'John', 1990, 'CS'),
                        ('marry@ualberta.ca', 'c', 'Marry', 1995, 'CS'),
                        ('mike@ualberta.ca', 'd', 'John', 1990, 'Math'),
                        ('sarah@ualberta.ca', 'e', 'Sarah', 1990, 'Math');
                        ''')
    connection.commit()


    cursor.executescript('''
                        INSERT OR IGNORE INTO books VALUES
                        (1, 'John 1', 'Joe', 2002),
                        (2, 'John 2', 'Joe', 2022),
                        (3, 'Book 3', 'John', 2024),
                        (4, 'Book 4', 'John', 2020),
                        (5, 'John 5', 'Rejwana', 2017),
                        (6, 'Book 6', 'Marry', 2017);
                        ''')
    connection.commit()

    """
    cursor.executescript('''
                        INSERT OR IGNORE INTO borrowings VALUES
                        (1, 'dave@ualberta.ca', 1, '2023-11-15', NULL),
                        (2, 'dave@ualberta.ca', 1, '2023-11-15', NULL),
                        (3, 'dave@ualberta.ca', 2, '2023-11-15', NULL),
                        (4, 'dave@ualberta.ca', 2, '2023-10-15', '2023-10-25'),
                        (5, 'john@ualberta.ca', 3, '2023-10-15', '2023-10-25'),
                        (6, 'john@ualberta.ca', 3, '2023-10-15', '2023-11-25'),
                        (7, 'john@ualberta.ca', 3, '2023-10-15', '2023-11-25'),
                        (8, 'john@ualberta.ca', 3, '2023-10-15', '2023-10-25'),
                        (9, 'mike@ualberta.ca', 4, '2023-11-15', NULL),
                        (10, 'marry@ualberta.ca', 4, '2023-11-15', NULL),
                        (11, 'marry@ualberta.ca', 4, '2023-11-15', NULL),
                        (12, 'sarah@ualberta.ca', 5, '2023-11-15', NULL);
                        ''')
    connection.commit()
    """
    """
    cursor.executescript('''
                        INSERT OR IGNORE INTO penalties VALUES
                        (1, 1, 50, NULL),
                        (2, 2, 50, 20),
                        (3, 1, 50, 50),
                        (4, 3, 60, 60),
                        (5, 5, 90, 90),
                        (6, 10, 50, NULL),
                        (7, 12, 70, 70);
                        ''')
    connection.commit()
    """
    """
    cursor.executescript('''
                        INSERT OR IGNORE INTO reviews VALUES
                        (1, 2, 'dave@ualberta.ca', 4, '','2023-12-15'),
                        (2, 2, 'marry@ualberta.ca', 3, '','2022-12-15'),
                        (3, 3, 'dave@ualberta.ca', 4, '','2023-08-15');
                        ''')
    connection.commit()
    """
def main():
    global connection, cursor

    # Connect to the database
    path="./library.db"
    connect(path)

    #drop all tables if necessary
    #drop_all_tables()

    # Create tables if they don't exist
    define_tables()

    # Commit changes and close connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
