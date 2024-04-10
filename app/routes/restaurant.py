# routes/doctors.py

import json
from http.server import BaseHTTPRequestHandler
from app.services import auth_service
from app.services import restaurant_service
from app.services import table_service

class RestaurantHandler:
    
    
    def handle_add_restaurant(self):
        if not self.authenticate():
            return
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        # required_fields = ['name', 'address', 'contact', 'opening_hours', 'img', 'desc', 'menu_items']
        # if not all(field in data for field in required_fields):
        #     self.send_error(400, 'Missing data for restaurant creation')
        #     return

        user_id = data.get('user_id')  # Assuming user_id is provided in the data
        # if not auth_service.is_admin(user_id):
        #     self.send_error(403, 'Only admins can add restaurants')
        #     return

        restaurant_data = restaurant_service.add_restaurant(user_id, data['name'], data['address'], data['contact'], data['opening_hours'], data['img'], data['description'], data['menu_items'])

        if restaurant_data:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "Restaurant added successfully", "restaurant_data": restaurant_data}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(500, 'Failed to add restaurant')


    # def handle_add_restaurant(self):
    #     if not self.authenticate():
    #         return
        
    #     content_length = int(self.headers['Content-Length'])
    #     post_data = self.rfile.read(content_length)
    #     data = json.loads(post_data.decode('utf-8'))

    #     # Proceed to add restaurant if data is present
    #     if data:
    #         user_id = data.get('user_id')  # Assuming user_id is provided in the data
    #         if not auth_service.is_admin(user_id):
    #             self.send_error(403, 'Only admins can add restaurants')
    #             return

    #         restaurant_id = restaurant_service.add_restaurant(data.get('name'), data.get('address'), data.get('contact'), data.get('opening_hours'), data.get('img'), data.get('desc'), data.get('menu_items'))

    #         if restaurant_id:
    #             self.send_response(200)
    #             self.send_header('Content-type', 'application/json')
    #             self.end_headers()
    #             response = {"message": "Restaurant added successfully", "restaurant_id": restaurant_id}
    #             self.wfile.write(json.dumps(response).encode('utf-8'))
    #         else:
    #             self.send_error(500, 'Failed to add restaurant')
    #     else:
    #         self.send_error(400, 'No data provided for restaurant creation')


    def handle_update_restaurant(self):
        if not self.authenticate():
            return
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        required_fields = ['restaurant_id', 'name', 'address', 'contact', 'opening_hours', 'img', 'desc', 'menu_items']
        if not all(field in data for field in required_fields):
            self.send_error(400, 'Missing data for restaurant update')
            return

        user_id = data.get('user_id')  # Assuming user_id is provided in the data
        if not auth_service.is_admin(user_id):
            self.send_error(403, 'Only admins can update restaurants')
            return

        success = restaurant_service.update_restaurant(data['restaurant_id'], data['name'], data['address'], data['contact'], data['opening_hours'], data['img'], data['desc'], data['menu_items'])

        if success:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Restaurant updated successfully"}).encode('utf-8'))
        else:
            self.send_error(500, 'Failed to update restaurant')

    def handle_delete_restaurant(self):
        if not self.authenticate():
            return

        restaurant_id = self.path.split('/')[-1]
        user_id = auth_service.is_admin(user_id) # Get user_id from authentication
        if not auth_service.is_admin(user_id):
            self.send_error(403, 'Only admins can delete restaurants')
            return

        success = restaurant_service.delete_restaurant(user_id, restaurant_id)

        if success:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Restaurant deleted successfully"}).encode('utf-8'))
        else:
            self.send_error(500, 'Failed to delete restaurant')

    def handle_get_restaurant(self):
        restaurant_id = self.path.split('/')[-1]
        restaurant = restaurant_service.get_restaurant(restaurant_id)

        if restaurant:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(restaurant).encode('utf-8'))
        else:
            self.send_error(404, "Restaurant not found")

    def handle_get_all_restaurants(self):
        restaurants = restaurant_service.get_all_restaurants()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(restaurants).encode('utf-8'))
        
        
        
        
        
        
    # Handler for assigning a doctor to a patient
    # def handle_assign_doctor(self):
    #     content_length = int(self.headers['Content-Length'])
    #     post_data = self.rfile.read(content_length)
    #     data = json.loads(post_data.decode('utf-8'))

    #     success = patient_service.assign_doctor(data['patient_id'], data['doctor_id'])
        
    #     if success:
    #         self.send_response(200)
    #         self.send_header('Content-type', 'application/json')
    #         self.end_headers()
    #         self.wfile.write(json.dumps({"message": "Doctor assigned successfully"}).encode('utf-8'))
    #     else:
    #         self.send_response(400)
    #         self.send_header('Content-type', 'application/json')
    #         self.end_headers()
    #         self.wfile.write(json.dumps({"message": "Failed to assign doctor"}).encode('utf-8'))
    #         pass