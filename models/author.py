from database.connection import get_db_connection

class Author:
    def __init__(self,name):

        #validate name length
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        
        #set name(private attribute)
        self._name = name

        #Insert new author into database and set the ID

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
             INSERT INTO authors(name)
             VALUES(?)
        ''',(self._name,))

    
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()


        #getter for id (property)
    @property
    def id(self):
        return self._id
        
    @property
    def name(self):
        return self._name
        

    #there should be no setter for name since it should not be changeable after instantiation
    @name.setter
    def name(self, value):
        raise AttributeError("Name cannot be changed after instantiation")
    
    #__repr__ method for a nice string representation of the object
    def __repr__(self):
        print(f"Debugging __repr__: {self.name}")
        return f'<Author {self.name}>'
    
    #fetching an Author by Id IF needed

    @classmethod
    def get_by_id(cls, author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
             SELECT * FROM authors WHERE id = ?
        ''',(author_id,))
        row = cursor.fetchone()
        print("Fetched row:",row)
        conn.close()
        if row:
            print(f"Debugging Author creation with name: {row[1]}")
            return cls(row[1] )
        else:
           return None

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT articles.title,articles.content
            FROM articles
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''',(self.id,))
        rows = cursor.fetchall()
        conn.close()

        articles = []
        for row in rows:
            articles.append({'title':row[0], 'content': row[1]})

        return articles
        

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT magazine.title,magazines.published_date
            FROM magazines
            JOIN authors ON magazines.author_id = authors.id
            WHERE authors.id = ?          
        ''',(self.id,))

        rows = cursor.fetchall()
        conn.close()

        magazines = []
        for row in rows:
            magazines.append({'title':row[0],'published_date':row[1]})
        return magazines
        
        
    

new_author = Author("Jane Doe")
print(f"New author created: {new_author}")


author = Author.get_by_id(1)
if author:
    print(f"Fetched Author by ID 1: {author}")

else:
    print("No author found with ID 1")

name = input("Enter author's name:")
new_author = Author(name)
print(f"New Author Created:{new_author}") 