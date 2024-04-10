# File: auth_service.py in the services/ directory

import sqlite3
import secrets
import hashlib

# def register_user(username, password, role, email, first_name, last_name, phone_number, address, img, db_file="restaurant_reservation.db"):
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()

#     # Insert a new user
#     cursor.execute("INSERT INTO users (username, password, role, email, first_name, last_name, phone_number, address, img) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
#                    (username, password, role, email, first_name, last_name, phone_number, address, img))
#     conn.commit()
#     user_id = cursor.lastrowid
#     conn.close()
    
#     return user_id

def register_user(username, password, email, fullname, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Insert a new user
    cursor.execute("INSERT INTO users (username, password, email, first_name, last_name) VALUES (?, ?, ?, ?, ?)", 
                   (username, password, email, *fullname.split(' ', 1)))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    return user_id



def login_user(username, password, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Verify user credentials
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    # Validate password and return user ID if successful
    if user and user[1] == password:
        return user[0]
    return None



def get_user_info_by_id(user_id, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Retrieve user information based on user_id
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user_info = cursor.fetchone()  # Fetch one row as a tuple
    conn.close()

    # Convert the user_info tuple to a dictionary for easier handling
    if user_info:
        user_info_dict = {
            "id": user_info[0],
            "username": user_info[1],
            "password": user_info[2],
            "role": user_info[3],
            "email": user_info[4],
            "first_name": user_info[5],
            "last_name": user_info[6],
            "phone_number": user_info[7],
            "address": user_info[8],
            "img": user_info[9]
        }
        return user_info_dict
    else:
        return None


def generate_token(user_id, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Generate a new token
    token = secrets.token_urlsafe(32)
    cursor.execute("INSERT INTO tokens (token, user_id) VALUES (?, ?)", (token, user_id))
    conn.commit()
    conn.close()
    
    return token

def is_admin(user_id, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] == 'admin' if result else False
    
    # if result and result[0] == 'admin':
    #     return True
    # return False


def verify_token(token, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if the token exists and is valid
    cursor.execute("SELECT user_id FROM tokens WHERE token = ?", (token,))
    user_id = cursor.fetchone()
    conn.close()
    
    return user_id[0] if user_id else None


def hash_password(password):
    # Create a sha256 hash object
    hasher = hashlib.sha256()
    # Update the hasher with the password
    hasher.update(password.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    hashed_password = hasher.hexdigest()
    return hashed_password