

from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, title, content, author, magazine):
        
        if not isinstance(title, str) or len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be a string between 5 and 50 characters")
        
        if not isinstance(content, str) or len(content) == 0:
            raise ValueError("Content must be a non-empty string")

        
        self._title = title
        self._content = content
        
        
        if not isinstance(author, Author):
            raise ValueError("Author must be an instance of Author")
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be an instance of Magazine")
        
        
        self._author_id = author.id
        self._magazine_id = magazine.id
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
        ''', (self._title, self._content, self._author_id, self._magazine_id))
        
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    
    @property
    def title(self):
        return self._title
    
    
    @property
    def content(self):
        return self._content
    
    
    @property
    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.name FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.id = ?
        ''', (self._id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    
    @property
    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT magazines.name FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.id = ?
        ''', (self._id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
    
    
    @property
    def id(self):
        return self._id

    
    def __repr__(self):
        return f'<Article {self.title}>'

    
    @classmethod
    def get_by_id(cls, article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles WHERE id = ?
        ''', (article_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
        
            author = Author.get_by_id(row[3])
            magazine = Magazine.get_by_id(row[4])
            return cls(row[1], row[2], author, magazine)
        else:
            return None


author = Author("Jane Doe")
magazine = Magazine("Tech Weekly", "Technology")


article = Article("How to Learn Python", "Content of the article goes here.", author, magazine)


print(f"Article created: {article}")
print(f"Article title: {article.title}")
print(f"Article author: {article.author}")
print(f"Article magazine: {article.magazine}")