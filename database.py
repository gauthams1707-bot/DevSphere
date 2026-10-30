
import sqlite3
from pathlib import Path
from datetime import datetime

# Database file location
BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "blog.db"


# Connect to database
def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# Create database and table
def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            excerpt TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT DEFAULT 'Admin',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Add a new blog article
def create_post(title, category, excerpt, content, author="Admin"):
    connection = get_connection()
    cursor = connection.cursor()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO posts
        (title, category, excerpt, content, author, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title, category, excerpt, content,
        author, current_time, current_time
    ))

    post_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return post_id


# Get all blog articles
def get_all_posts():
    connection = get_connection()

    posts = connection.execute("""
        SELECT * FROM posts
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return posts


# Get a single article using its ID
def get_post_by_id(post_id):
    connection = get_connection()

    post = connection.execute("""
        SELECT * FROM posts WHERE id = ?
    """, (post_id,)).fetchone()

    connection.close()

    return post


# Update an existing article
def update_post(post_id, title, category, excerpt, content):
    connection = get_connection()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection.execute("""
        UPDATE posts
        SET title = ?,
            category = ?,
            excerpt = ?,
            content = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        title, category, excerpt,
        content, current_time, post_id
    ))

    connection.commit()
    connection.close()


# Delete an article
def delete_post(post_id):
    connection = get_connection()

    connection.execute("""
        DELETE FROM posts WHERE id = ?
    """, (post_id,))

    connection.commit()
    connection.close()


# Search articles by title, category or content
def search_posts(keyword):
    connection = get_connection()

    search_term = f"%{keyword}%"

    posts = connection.execute("""
        SELECT * FROM posts
        WHERE title LIKE ?
           OR category LIKE ?
           OR content LIKE ?
           OR excerpt LIKE ?
        ORDER BY id DESC
    """, (
        search_term,
        search_term,
        search_term,
        search_term
    )).fetchall()

    connection.close()

    return posts


# Get articles by category
def get_posts_by_category(category):
    connection = get_connection()

    posts = connection.execute("""
        SELECT * FROM posts
        WHERE category = ?
        ORDER BY id DESC
    """, (category,)).fetchall()

    connection.close()

    return posts


# Get total number of articles
def get_post_count():
    connection = get_connection()

    count = connection.execute("""
        SELECT COUNT(*) FROM posts
    """).fetchone()[0]

    connection.close()

    return count


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")
