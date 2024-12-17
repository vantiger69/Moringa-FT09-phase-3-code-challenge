from connection import get_db_connection

def create_tables():
    print("Starting table creation...")  # Debug start
    try:
        conn = get_db_connection()
        print("Database connection successful!")  # Debug connection
        cursor = conn.cursor()

        print("Creating 'authors' table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        print("Creating 'magazines' table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            )
        ''')

        print("Creating 'articles' table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER,
                magazine_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors (id),
                FOREIGN KEY (magazine_id) REFERENCES magazines (id)
            )
        ''')

        conn.commit()
        print("All tables created successfully!")  # Success
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        print("Database connection closed.")  # Closing message

create_tables()
