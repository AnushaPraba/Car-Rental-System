import re
from exception.invalid_customer_detail_exception import InvalidEmailException, InvalidPasswordException, \
    DuplicateUserNameException
from exception.invalid_customer_detail_exception import InvalidPhoneNumberException
import bcrypt

def validate_email(email):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        raise InvalidEmailException("Invalid email format.")
    else:
        return True

def validate_phone(phone):
    if not re.match(r"^[6-9]\d{9}$", phone):
        raise InvalidPhoneNumberException("Invalid phone number format.Must be 10 digits starting with 6-9.")
    else:
        return True

def validate_password(password):
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", password):
        raise InvalidPasswordException("Password must be at least 8 characters, with one uppercase, one lowercase, and one digit.")
    else:
        return True

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return hashed

def is_username_unique(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone() is None:
        return True
    else:
        raise DuplicateUserNameException("Username already exists. Choose another.")