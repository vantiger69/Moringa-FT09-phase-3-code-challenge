from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category):
        self._id = None
        self.name = name
        self.category = category

        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()


        self.insert_magazine_into_db(name,category)

        self._id = self.get_magazine_id_from_db(name)

    def insert_magazine_into_db(self,name,category):
        print(f"Magazine '{name}' with category '{category}' inserted into DB.")

        query = "INSERT INTO magazine (name,category) VALUES (%s,%s) RETURNING id;"
        try:
         self.cursor.execute(query ,(name, category))
         self.conn.commit()
         self._id = self.cursor.fetchone()[0]
    
        except Exception as e:
            print(f"Error fetching magazine ID: {e}") 
            return None


    def get_magazine_id_from_db(self,name):
          query = "SELECT id FROM magazine WHERE name LIKE ?;"
          try:
            self.cursor.execute(query, (f"%{name}%",))
            result = self.cursor.fetchone()
            return result[0] if result else None
          except Exception as e:
              print(f"Error fetching magazine ID: {e}")
              return None
        

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,value):
        if len(value) < 2 or len(value) > 16 :
            raise ValueError("Name must be between 2 and 16 characters.")
        self._name = value
        self.update_name_in_db(value)


    def update_name_in_db(self, value):
        query = "UPDATE magazine SET name = %s WHERE id = %s;"
        try:
            self.cursor.execute(query, (value,self.id))
            self.conn.commit()
        except Exception as e:
            print(f"Error updating name: {e}")

    @property
    def category(self):
        return self._category
    

    @category.setter
    def category(self, value):

        if len(value) == 0:
            raise ValueError("Category must not be empty.")
        
        self._category = value
        self.update_category_in_db(value)


    def update_category_in_db(self,value):
        query = ("UPDATE magazine SET category = %s WHERE id = %s;")
        try:
            self.cursor.execute(query, (value,self.id))
            self.conn.commit()
        except Exception as e:
            print(f"Error updating category: {e}")        


    def articles(self):
        pass
    def contributions(self):
        pass

    def article_titles(self):

        pass 

    def contributing_authors(self):

        pass      


magazine = Magazine("Tech Monthly","Technology")

print(f"Mgazine ID: {magazine.id}")
print(f"Mgazine Name: {magazine.name}")
print(f"Mgazine Category: {magazine.category}")
 
magazine.name = "Science Weekly"
magazine.category = "Science"

print(f"Updated Name: {magazine.name}")
print(f"Updated Category: {magazine.name}")


