import sqlite3
from app.services import auth_service

# def add_restaurant(user_id, name, address, contact, opening_hours, img, description, menu_items, db_file="restaurant_reservation.db"):
#     # Check if the user has admin privileges
#     if not auth_service.is_admin(user_id):
#         return None  # Or raise an exception

#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()

#     # Proceed with adding the restaurant if the user is an admin
#     cursor.execute("INSERT INTO restaurants (user_id, name, address, contact, opening_hours, img, description, menu_items) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#                    (user_id, name, address, contact, opening_hours, img, description, menu_items))
#     conn.commit()
#     restaurant_info = cursor.lastrowid
#     conn.close()

#     return restaurant_info


def add_restaurant(user_id, name, address, contact, opening_hours, img, description, menu_items, db_file="restaurant_reservation.db"):
    # Check if the user has admin privileges
    if not auth_service.is_admin(user_id):
        return None  # Or raise an exception

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Proceed with adding the restaurant if the user is an admin
    cursor.execute("INSERT INTO restaurants (user_id, name, address, contact, opening_hours, img, description, menu_items) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (user_id, name, address, contact, opening_hours, img, description, menu_items))
    conn.commit()
    restaurant_info = cursor.lastrowid
    conn.close()

    return restaurant_info

def update_restaurant(user_id, restaurant_id, name, address, contact, opening_hours, img, description, menu_items, db_file="restaurant_reservation.db"):
    if not auth_service.is_admin(user_id):
        return False  # Or raise an exception

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("UPDATE restaurants SET name = ?, address = ?, contact = ?, opening_hours = ?, img = ?, description = ?, menu_items = ? WHERE restaurant_id = ?",
                   (name, address, contact, opening_hours, img, description, menu_items, restaurant_id))
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()

    return updated_rows > 0

def delete_restaurant(user_id, restaurant_id, db_file="restaurant_reservation.db"):
    if not auth_service.is_admin(user_id):
        return False  # Or raise an exception

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM restaurants WHERE restaurant_id = ?", (restaurant_id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()

    return deleted_rows > 0

# def get_restaurant(restaurant_id, db_file="restaurant_reservation.db"):
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM restaurants WHERE restaurant_id = ?", (restaurant_id,))
#     restaurant = cursor.fetchone()
#     conn.close()

#     return restaurant

def get_restaurant(restaurant_id, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM restaurants WHERE restaurant_id = ?", (restaurant_id,))
    restaurants = cursor.fetchall()
    
    if restaurants:
        columns = [column[0] for column in cursor.description]  # Get column names
        restaurant_list = []
        for row in restaurants:
            restaurant_dict = dict(zip(columns, row))  # Create dictionary for each row
            restaurant_list.append(restaurant_dict)
        return restaurant_list
    else:
        return None
    
    conn.close()



# def get_all_restaurants(db_file="restaurant_reservation.db"):
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM restaurants")
#     restaurants = cursor.fetchall()
#     conn.close()

#     return restaurants


def get_all_restaurants(db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM restaurants")
    rows = cursor.fetchall()
    
    restaurants = []
    if rows:
        columns = [col[0] for col in cursor.description]
        for row in rows:
            restaurant = dict(zip(columns, row))
            restaurants.append(restaurant)

    conn.close()

    return restaurants











