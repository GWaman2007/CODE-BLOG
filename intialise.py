import mysql.connector
from mysql.connector import errorcode

# Database configuration
config = {
    'user': 'root',
    'password': 'tiger',
    'host': 'localhost',
}

def drop_database_if_exists(cursor):
    try:
        cursor.execute("DROP DATABASE IF EXISTS code_blog")
        print("Database dropped (if it existed).")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE code_blog")
        cursor.execute("USE code_blog")
        print("Database created and selected.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)

def create_tables(cursor):
    tables = {
        'users': (
            "CREATE TABLE users ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "username VARCHAR(50) NOT NULL UNIQUE, "
            "email VARCHAR(100) NOT NULL UNIQUE, "
            "password_hash VARCHAR(255) NOT NULL, "
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
            ")"
        ),
        'posts': (
            "CREATE TABLE posts ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "title VARCHAR(255) NOT NULL, "
            "content TEXT NOT NULL, "
            "author_id INT, "
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
            "FOREIGN KEY (author_id) REFERENCES users(id)"
            ")"
        ),
        'comments': (
            "CREATE TABLE comments ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "post_id INT, "
            "author_id INT, "
            "content TEXT NOT NULL, "
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
            "FOREIGN KEY (post_id) REFERENCES posts(id), "
            "FOREIGN KEY (author_id) REFERENCES users(id)"
            ")"
        ),
        'likes': (
            "CREATE TABLE likes ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "post_id INT, "
            "user_id INT, "
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
            "FOREIGN KEY (post_id) REFERENCES posts(id), "
            "FOREIGN KEY (user_id) REFERENCES users(id)"
            ")"
        )
    }

    for table_name in tables:
        table_creation_query = tables[table_name]
        try:
            cursor.execute(table_creation_query)
            print(f"Table '{table_name}' created.")
        except mysql.connector.Error as err:
            print(f"Error creating table '{table_name}': {err}")
            exit(1)

def main():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        drop_database_if_exists(cursor)
        create_database(cursor)
        create_tables(cursor)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
