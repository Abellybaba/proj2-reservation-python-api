import sqlite3

def add_reservation(user_id, restaurant_id, date, time, party_size, special_requests, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO reservations (user_id, restaurant_id, date, time, party_size, special_requests) VALUES (?, ?, ?, ?, ?, ?)", 
                   (user_id, restaurant_id, date, time, party_size, special_requests))
    conn.commit()
    reservation_id = cursor.lastrowid
    conn.close()
    
    return reservation_id

def get_reservations(db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""SELECT r.*, u.username AS user_username, u.email AS user_email, u.first_name AS user_first_name, u.last_name AS user_last_name,
                      rest.name AS restaurant_name, rest.address AS restaurant_address, rest.contact AS restaurant_contact
                      FROM reservations r
                      JOIN users u ON r.user_id = u.id
                      JOIN restaurants rest ON r.restaurant_id = rest.restaurant_id""")
    records = cursor.fetchall()
    conn.close()
    
    return [{
        'reservation_id': row[0],
        'user_id': row[1],
        'restaurant_id': row[2],
        'date': row[3],
        'time': row[4],
        'party_size': row[5],
        'status': row[6],
        'special_requests': row[7],
        'user_username': row[8],
        'user_email': row[9],
        'user_first_name': row[10],
        'user_last_name': row[11],
        'restaurant_name': row[12],
        'restaurant_address': row[13],
        'restaurant_contact': row[14]
    } for row in records]

# def update_reservation(reservation_id, user_id, restaurant_id, date, time, party_size, status, special_requests, db_file="restaurant_reservation.db"):
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
#     cursor.execute("UPDATE reservations SET user_id = ?, restaurant_id = ?, date = ?, time = ?, party_size = ?, status = ?, special_requests = ? WHERE reservation_id = ?",
#                    (user_id, restaurant_id, date, time, party_size, status, special_requests, reservation_id))
#     conn.commit()
#     conn.close()

import sqlite3

def update_reservation(reservation_id, user_id, restaurant_id, date, time, party_size, status, special_requests, db_file="restaurant_reservation.db"):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Update the reservation in the database
        cursor.execute("""
            UPDATE reservations 
            SET user_id = ?, 
                restaurant_id = ?, 
                date = ?, 
                time = ?, 
                party_size = ?, 
                status = ?, 
                special_requests = ? 
            WHERE reservation_id = ?""",
            (user_id, restaurant_id, date, time, party_size, status, special_requests, reservation_id))
        
        # Commit the transaction
        conn.commit()

        # Close the database connection
        conn.close()
        
        return True  # Return True to indicate success
    except sqlite3.Error as e:
        # Handle any errors that occur during the update process
        print("Error updating reservation:", e)
        return False  # Return False to indicate failure



def delete_reservation(reservation_id, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservations WHERE reservation_id = ?", (reservation_id,))
    conn.commit()
    conn.close()

# def get_reservation_by_id(reservation_id, db_file="restaurant_reservation.db"):
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
#     cursor.execute("""SELECT r.*, u.username AS user_username, u.email AS user_email, u.first_name AS user_first_name, u.last_name AS user_last_name,
#                             rest.name AS restaurant_name, rest.address AS restaurant_address, rest.contact AS restaurant_contact
#                             FROM reservations r
#                             JOIN users u ON r.user_id = u.id
#                             JOIN restaurants rest ON r.restaurant_id = rest.restaurant_id
#                             WHERE reservation_id = ?
#                             """, (reservation_id,))
#     record = cursor.fetchone()
#     conn.close()
#     return record


def get_reservation_by_id(reservation_id, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""SELECT r.*, u.username AS user_username, u.email AS user_email, u.first_name AS user_first_name, u.last_name AS user_last_name,
                      rest.name AS restaurant_name, rest.address AS restaurant_address, rest.contact AS restaurant_contact
                      FROM reservations r
                      JOIN users u ON r.user_id = u.id
                      JOIN restaurants rest ON r.restaurant_id = rest.restaurant_id
                      WHERE reservation_id = ?""", (reservation_id,))
    
    records = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    conn.close()

    reservations = []
    for row in records:
        reservation = dict(zip(columns, row))
        reservations.append(reservation)

    return reservations

