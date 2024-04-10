# routes/health_records.py
import json
from http.server import BaseHTTPRequestHandler
from app.services import auth_service
from app.services import reservation_service

class ReservationHandler:
    
    def handle_add_reservation(self):
        if not self.authenticate():
            return
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        # Assuming the data includes user_id, restaurant_id, date, time, party_size, status, special_requests
        reservation_id = reservation_service.add_reservation(data['user_id'], data['restaurant_id'], data['date'], data['time'], data['party_size'], data['status'], data['special_requests'])
        
        if reservation_id:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Reservation added successfully", "reservation_id": reservation_id}).encode('utf-8'))
        else:
            self.send_error(400, 'Failed to add reservation')




    def handle_update_reservation(self, reservation_id):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        reservation_service.update_reservation(reservation_id, data['user_id'], data['restaurant_id'], data['date'], data['time'], data['party_size'], data['status'], data['special_requests'])

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Reservation updated successfully"}).encode('utf-8'))

    # def handle_update_reservation(self, reservation_id):
    #     content_length = int(self.headers['Content-Length'])
    #     post_data = self.rfile.read(content_length)
    #     data = json.loads(post_data.decode('utf-8'))

    #     # Extract data from the request body and pass it to the update_reservation service
    #     success = reservation_service.update_reservation(reservation_id, data['user_id'], data['restaurant_id'], data['date'], data['time'], data['party_size'], data['status'], data['special_requests'])

    #     if success:
    #         self.send_response(200)
    #         self.send_header('Content-type', 'application/json')
    #         self.end_headers()
    #         self.wfile.write(json.dumps({"message": "Reservation updated successfully"}).encode('utf-8'))
    #     else:
    #         self.send_error(500, 'Failed to update reservation')


    def handle_delete_reservation(self):
        reservation_id = self.path.split('/')[-1]
        reservation_service.delete_reservation(reservation_id)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Reservation deleted successfully"}).encode('utf-8'))

    def handle_get_reservation(self):
        reservation_id = self.path.split('/')[-1]
        reservation = reservation_service.get_reservation_by_id(reservation_id)

        if reservation:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(reservation).encode('utf-8'))
        else:
            self.send_error(404, "Reservation not found")
        
    def handle_get_all_reservations(self):
        reservations = reservation_service.get_reservations()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(reservations).encode('utf-8'))


# class HealthRecordHandler:
#     def handle_add_health_record(self):
#         if not self.authenticate():
#             return
        
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length)
#         data = json.loads(post_data.decode('utf-8'))

#         # Assuming the data includes patient_id, record_type, summary, detailed_record_link
#         record_id = reservation_service.add_health_record(data['patient_id'], data['record_type'], data['summary'], data['detailed_record_link'], self.user_id)
        
#         if record_id:
#             self.send_response(200)
#             self.send_header('Content-type', 'application/json')
#             self.end_headers()
#             self.wfile.write(json.dumps({"message": "Health record added successfully", "record_id": record_id}).encode('utf-8'))
#         else:
#             self.send_error(400, 'Failed to add health record')
#         pass

#     def handle_update_health_record(self):
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length)
#         data = json.loads(post_data.decode('utf-8'))

#         reservation_service.update_health_record(data['record_id'], data['patient_id'], data['record_type'], data['summary'], data['detailed_record_link'], data['created_by_doctor_id'])

#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#         self.wfile.write(json.dumps({"message": "Health record updated successfully"}).encode('utf-8'))

#         pass

#     def handle_delete_health_record(self):
#         record_id = self.path.split('/')[-1]
#         reservation_service.delete_health_record(record_id)

#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#         self.wfile.write(json.dumps({"message": "Health record deleted successfully"}).encode('utf-8'))

#         pass

#     def handle_get_health_record(self):
#         record_id = self.path.split('/')[-1]
#         record = reservation_service.get_health_record_by_id(record_id)

#         if record:
#             self.send_response(200)
#             self.send_header('Content-type', 'application/json')
#             self.end_headers()
#             self.wfile.write(json.dumps(record).encode('utf-8'))
#         else:
#             self.send_error(404, "Health record not found")
        
#         pass

#     def handle_get_all_health_records(self):
#         records = reservation_service.get_health_records()

#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#         self.wfile.write(json.dumps(records).encode('utf-8'))
#         pass
