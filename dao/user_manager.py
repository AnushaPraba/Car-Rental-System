import bcrypt
from util.validation import validate_email, validate_phone, validate_password, hash_password, is_username_unique
from util.db_conn_util import DBConnUtil
from getpass import getpass

class UserManager:
    def __init__(self):
        self.conn = DBConnUtil.get_connection(r'E:/nila_hexa/Car-Rental-System/util/db.properties')

    def signup_customer(self):
        cursor = self.conn.cursor()

        firstName = input("Enter First Name: ")
        lastName = input("Enter Last Name: ")

        while True:
            email = input("Enter Email: ")
            try:
                if validate_email(email):
                    break
            except Exception as e:
                print(e)

        while True:
            phone = input("Enter Phone Number: ")
            try:
                if validate_phone(phone):
                    break
            except Exception as e:
                print(e)

        while True:
            username = input("Choose a Username: ")
            try:
                if is_username_unique(self.conn, username):
                    break
            except Exception as e:
                print(e)

        while True:
            password = input("Choose a Password: ")
            try:
                if validate_password(password):
                    hashed_password = hash_password(password)
                    break
            except Exception as e:
                print(e)

        cursor.execute(""" 
            INSERT INTO customer (firstName, lastName, email, phoneNumber)
            VALUES (%s, %s, %s, %s)
        """, (firstName, lastName, email, phone))
        self.conn.commit()
        customer_id = cursor.lastrowid

        cursor.execute(""" 
            INSERT INTO users (username, password, role, customerID)
            VALUES (%s, %s, 'customer', %s)
        """, (username, hashed_password, customer_id))
        self.conn.commit()

        print("Signup successful! You can now login.")

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            role = user[3]
            customerID = user[4]
            print(f"Login successful! Logged in as {role}.")
            return role,customerID # Pass customerID
        else:
            print("Invalid credentials.\n")
            return None,None

