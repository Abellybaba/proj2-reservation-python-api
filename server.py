# File: server.py

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging
from urllib.parse import parse_qs, urlparse
from app.services import auth_service
from app.services import table_service
from app.services import restaurant_service
from app.services import reservation_service
from app.db import models
from app.routes import reservation, restaurant, table

# Initialize logging
logging.basicConfig(level=logging.INFO)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler, restaurant.RestaurantHandler, table.TableHandler, reservation.ReservationHandler):
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000, *')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-type, Authorization')
        BaseHTTPRequestHandler.end_headers(self)
    
    
    def do_GET(self):
        if self.path.startswith('/restaurant/'):
            self.handle_get_restaurant()
        elif self.path == '/reservations':
            self.handle_get_all_reservations()
        elif self.path.startswith('/reservation/'):
            self.handle_get_reservation()
        elif self.path == '/tables':
            if not self.authenticate():
                return
            self.handle_get_all_tables()
        elif self.path == '/restaurants':
            if not self.authenticate():
                return
            self.handle_get_all_restaurants()
        elif self.path.startswith('/table/'):
            table_id = self.path.split('/')[-1]
            if table_id.isdigit():
                self.handle_get_table_by_id(table_id)
            else:
                self.send_error(400, 'Invalid table ID')
        
            
    def authenticate(self):
        """Check if the request contains a valid token."""
        if 'Authorization' not in self.headers:
            self.send_error(401, 'Authorization token is missing')
            return False

        token = self.headers['Authorization'].split()[-1]
        user_id = auth_service.verify_token(token)
        if not user_id:
            self.send_error(403, 'Token is invalid')
            return False
        
        # User ID from the token can be used to further verify user's permissions if necessary
        self.user_id = user_id
        return True

    def is_user_admin(self):
    # Make sure the user is authenticated
        if not self.authenticate():
            return False
    # Check if the authenticated user is an admin
            return auth_service.is_admin(self.user_id)



    def do_POST(self):
        if self.path == '/register':
            self.handle_register()
        elif self.path == '/login':
            self.handle_login()
        elif self.path == '/add_restaurant':
            if not self.authenticate():
                return
            self.handle_add_restaurant()
        elif self.path == '/add_table':
            if not self.authenticate():
                return
            self.handle_add_table()
        elif self.path == '/add_reservation':
            if not self.authenticate():
                return
            self.handle_add_reservation()
    
    
    def do_PUT(self):
        if self.path.startswith('/update_restaurant/'):
            if not self.authenticate():
                return
            restaurant_id = self.path.split('/')[-1]
            if restaurant_id.isdigit():
                self.handle_update_restaurant(restaurant_id)
            else:
                self.send_error(400, 'Invalid restaurant ID')
        elif self.path.startswith('/update_table/'):
            if not self.authenticate():
                return
            table_id = self.path.split('/')[-1]
            if table_id.isdigit():
                self.handle_update_table(table_id)
            else:
                self.send_error(400, 'Invalid table ID')
        elif self.path.startswith('/update_reservation/'):
            # if not self.is_user_admin():
            #     self.send_error(403, "Only admins can perform this action.")
            #     return
            reservation_id = self.path.split('/')[-1]
            if reservation_id.isdigit():
                self.handle_update_reservation(reservation_id)
            # else:
            #     self.send_error(400, 'Invalid reservation ID')

    def do_DELETE(self):
        if self.path.startswith('/delete_restaurant/'):
            if not self.authenticate():
                return
            restaurant_id = self.path.split('/')[-1]
            if restaurant_id.isdigit():
                self.handle_delete_restaurant(restaurant_id)
            else:
                self.send_error(400, 'Invalid restaurant ID')
        elif self.path.startswith('/delete_table/'):
            if not self.authenticate():
                return
            table_id = self.path.split('/')[-1]
            if table_id.isdigit():
                self.handle_delete_table(table_id)
            else:
                self.send_error(400, 'Invalid table ID')
        elif self.path.startswith('/delete_reservation/'):
            if not self.is_user_admin():
                self.send_error(403, "Only admins can perform this action.")
                return
            reservation_id = self.path.split('/')[-1]
            if reservation_id.isdigit():
                self.handle_delete_reservation(reservation_id)
            else:
                self.send_error(400, 'Invalid reservation ID')
                
    def handle_register(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            if not all(key in data for key in ['username', 'password', 'email', 'fullname']):
                self.send_error(400, 'Missing registration information')
                return
            
            # Hash the password before registration
            # hashed_password = auth_service.hash_password(password)

            user_id = auth_service.register_user(data['username'], data['password'], data['email'], data['fullname'])

            if user_id:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"message": "User registered successfully", "user_id": user_id}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self.send_error(400, 'Registration failed')


    # def handle_register(self):
    #     content_length = int(self.headers['Content-Length'])
    #     post_data = self.rfile.read(content_length)
    #     data = json.loads(post_data.decode('utf-8'))

    #     if not all(key in data for key in ['username', 'password', 'email', 'fullname']):
    #         self.send_error(400, 'Missing registration information')
    #         return

    #     username = data['username']
    #     password = data['password']
    #     email = data['email']
    #     fullname = data['fullname']

    #     # Hash the password before registration
    #     hashed_password = auth_service.hash_password(password)

    #     user_id = auth_service.register_user(username, hashed_password, email, fullname)

    #     if user_id:
    #         self.send_response(200)
    #         self.send_header('Content-type', 'application/json')
    #         self.end_headers()
    #         response = {"message": "User registered successfully", "user_id": user_id}
    #         self.wfile.write(json.dumps(response).encode('utf-8'))
    #     else:
    #         self.send_error(400, 'Registration failed')



    def log_message(self, format, *args):
        # Override to direct http.server logs to standard logging
        logging.info("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))

    def send_error(self, code, message=None):
        # Customize error handling
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if message:
            self.wfile.write(json.dumps({'error': message}).encode('utf-8'))
        else:
            self.wfile.write(json.dumps({'error': 'An error occurred'}).encode('utf-8'))



    def handle_login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if 'username' not in data or 'password' not in data:
            self.send_error(400, 'Username and password are required')
            return

        user_id = auth_service.login_user(data['username'], data['password'])

        if user_id:
            token = auth_service.generate_token(user_id)
            user_info = auth_service.get_user_info_by_id(user_id)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "Login successful", "token": token, "user": user_info}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(401, 'Invalid username or password')
        


    # def handle_register(self):
    #     content_length = int(self.headers['Content-Length'])
    #     post_data = self.rfile.read(content_length)
    #     data = json.loads(post_data.decode('utf-8'))

    #     if not all(key in data for key in ['username', 'password', 'role', 'email', 'fullname']):
    #         self.send_error(400, 'Missing registration information')
    #         return

    #     user_id = auth_service.register_user(data['username'], data['password'], data['role'], data['email'], data['fullname'])

    #     if user_id:
    #         self.send_response(200)
    #         self.send_header('Content-type', 'application/json')
    #         self.end_headers()
    #         response = {"message": "User registered successfully", "user_id": user_id}
    #         self.wfile.write(json.dumps(response).encode('utf-8'))
    #     else:
    #         self.send_error(400, 'Registration failed')


    # def handle_login(self):
    #     content_length = int(self.headers['Content-Length'])
    #     post_data = self.rfile.read(content_length)
    #     data = json.loads(post_data.decode('utf-8'))

    #     if 'username' not in data or 'password' not in data:
    #         self.send_error(400, 'Username and password are required')
    #         return

    #     user_id = auth_service.login_user(data['username'], data['password'])
    #     if user_id:
    #         token = auth_service.generate_token(user_id)
    #         self.send_response(200)
    #         self.send_header('Content-type', 'application/json')
    #         self.end_headers()
    #         self.wfile.write(json.dumps({"message": "Login successful", "token": token}).encode('utf-8'))
    #     else:
    #         self.send_error(401, 'Invalid username or password')


if __name__ == '__main__':
    models.setup_database()
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    logging.info("Server started on localhost:8000")
    httpd.serve_forever()