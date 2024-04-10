from app.db import database

database_file = "restaurant_reservation.db"


sql_create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role DEFAULT 'customer',  
    email TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    phone_number TEXT,
    address TEXT,
    img TEXT
);
"""

sql_create_tokens_table = """
CREATE TABLE IF NOT EXISTS tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    expiry TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

# restaurant table 
sql_create_reservations_table = """
CREATE TABLE IF NOT EXISTS reservations (
            reservation_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            restaurant_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            party_size INTEGER NOT NULL,
            status DEFAULT 'pending',
            special_requests TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (restaurant_id)
);
"""

# health_records table
sql_create_tables_table = """
CREATE TABLE IF NOT EXISTS tables (
            table_id INTEGER PRIMARY KEY,
            restaurant_id INTEGER NOT NULL,
            table_number INTEGER NOT NULL,
            capacity INTEGER NOT NULL,
            is_available INTEGER NOT NULL,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (restaurant_id)
);
"""


sql_create_restaurants_table = """
CREATE TABLE IF NOT EXISTS restaurants (
            restaurant_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT NOT NULL,
            address TEXT,
            contact TEXT,
            opening_hours TEXT,
            img TEXT,
            description TEXT,
            menu_items TEXT
);
"""

# Function to create tables
def setup_database():
    conn = database.create_connection(database_file)
    if conn is not None:
        database.create_table(conn, sql_create_users_table)
        database.create_table(conn, sql_create_restaurants_table)
        database.create_table(conn, sql_create_reservations_table)
        database.create_table(conn, sql_create_tables_table)
        database.create_table(conn, sql_create_tokens_table)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == "__main__":
    setup_database()
