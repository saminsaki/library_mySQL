import mysql.connector
from mysql.connector import Error

# Database Connection
class Database:
    def __init__(self, host, user, password, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def create_database(self, name):
        try:
            sql = f"CREATE DATABASE IF NOT EXISTS {name}"
            self.cursor.execute(sql)
            self.connection.database = name
            self.database = name
            print("Database Created!")
        except Error as e:
            print(e)

    def create_table(self, table_sql):
        try:
            self.cursor.execute(table_sql)
            print("Table created")
        except Error as e:
            print(f"Error creating table: {e}")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
        except Error as e:
            print(f"Error executing query: {e}")

    def query_fetchall(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")

    def close(self):
        self.connection.close()

class User:
    def __init__(self, db):
        self.db = db
        self.logged_in_user = False

    def register(self, username, password, email):
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (username, password, email))
        print("User registered successfully.")

    def login(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        user = self.db.query_fetchall(query, (username, password))
        if user:
            self.logged_in_user = True
            print(f"{username} is logged in.")
        else:
            print("Login failed. Incorrect username or password.")

    def logout(self):
        if self.logged_in_user:
            print("Logged out.")
            self.logged_in_user = False
        else:
            print("No user is currently logged in.")

    def show_profile(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        user = self.db.query_fetchall(query, (username,))
        if user:
            print(f"User Details: {user}")
        else:
            print("User not found.")

class Employee:
    def __init__(self, db):
        self.db = db

    def add_employee(self, name, position):
        query = "INSERT INTO employees (name, position) VALUES (%s, %s)"
        self.db.execute_query(query, (name, position))
        print("Employee added successfully.")

    def show_employee_details(self, name):
        query = "SELECT * FROM employees WHERE name = %s"
        employee = self.db.query_fetchall(query, (name,))
        if employee:
            print(f"Employee Details: {employee}")
        else:
            print("Employee not found.")

class Book:
    def __init__(self, db):
        self.db = db

    def add_book(self, title, author, publication_year, genre):
        query = "INSERT INTO books (title, author, publication_year, genre) VALUES (%s, %s, %s, %s)"
        self.db.execute_query(query, (title, author, publication_year, genre))
        print("Book added successfully.")

    def update_book_info(self, book_id, author=None, publication_year=None, genre=None):
        query = "UPDATE books SET author = %s, publication_year = %s, genre = %s WHERE id = %s"
        update_data = (author, publication_year, genre, book_id)
        self.db.execute_query(query, update_data)
        print("Book information updated successfully.")

    def search_books(self, **kwargs):
        query_parts = []
        params = []

        for key, value in kwargs.items():
            if key in ['title', 'author', 'genre'] and value:
                query_parts.append(f"{key} LIKE %s")
                params.append(f"%{value}%")

        if not query_parts:
            print("No search criteria provided.")
            return

        query = "SELECT * FROM books WHERE " + " AND ".join(query_parts)
        books = self.db.query_fetchall(query, tuple(params))

        if books:
            print("Books found:")
            for book in books:
                print(book)
        else:
            print("No books found with the given search criteria.")


# Define tables
tables = {
    'users': """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100)
        )
    """,
    'employees': """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            position VARCHAR(100)
        )
    """,
    'books': """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(100),
            publication_year YEAR,
            genre VARCHAR(100)
        )
    """
}

# Database Initialization
db_info = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MohammadMohammad',
}

db = Database(**db_info)
db.create_database("library_db")

# Create tables
for table_name, table_sql in tables.items():
    db.create_table(table_sql)

# Main Function for Testing
def main():

    user_manager = User(db)
    employee_manager = Employee(db)

    # Test User Registration
    user_manager.register("john_doe", "john123", "john@example.com")

    # Test Login
    user_manager.login("john_doe", "john123")

    # Test Showing User Profile
    user_manager.show_profile("john_doe")

    # Test Logout
    user_manager.logout()

    # Test Employee Management
    employee_manager.add_employee("Jane Smith", "Librarian")
    employee_manager.show_employee_details("Jane Smith")
    

    # Test Book Management
    book_manager = Book(db)
    book_manager.add_book("Book1", "F. M", 1925, "Novel")
    book_manager.update_book_info(1, author="F. M", publication_year=1925, genre="Classic")
    book_manager.search_books(author="F. M")


    db.close()


if __name__ == "__main__":
    main()