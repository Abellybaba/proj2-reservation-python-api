
import sqlite3


def add_table(restaurant_id, table_number, capacity, is_available, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tables (restaurant_id, table_number, capacity, is_available) 
        VALUES (?, ?, ?, ?)""", (restaurant_id, table_number, capacity, is_available))
    conn.commit()
    table_id = cursor.lastrowid
    conn.close()
    return table_id

def update_table(table_id, restaurant_id, table_number, capacity, is_available, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tables 
        SET restaurant_id = ?, table_number = ?, capacity = ?, is_available = ? 
        WHERE table_id = ?""", (restaurant_id, table_number, capacity, is_available, table_id))
    conn.commit()
    conn.close()

def get_all_tables(db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tables")
    tables = cursor.fetchall()
    conn.close()
    return [{'table_id': row[0], 'restaurant_id': row[1], 'table_number': row[2], 'capacity': row[3], 'is_available': row[4]} for row in tables]

def get_table_by_id(table_id, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tables WHERE table_id = ?", (table_id,))
    table = cursor.fetchone()
    conn.close()
    if table:
        return {'table_id': table[0], 'restaurant_id': table[1], 'table_number': table[2], 'capacity': table[3], 'is_available': table[4]}
    return None

def delete_table(table_id, db_file="restaurant_reservation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tables WHERE table_id = ?", (table_id,))
    conn.commit()
    conn.close()
