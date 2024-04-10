# routes/patients.py

from http.server import BaseHTTPRequestHandler
from app.services import auth_service
from app.services import table_service
import json

class TableHandler:
    def handle_add_table(self):
        content_length = int(self.headers.get('Content-Length'))
        post_data = json.loads(self.rfile.read(content_length))
        table_id = table_service.add_table(post_data['restaurant_id'], post_data['table_number'], post_data['capacity'], post_data['is_available'])
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {'message': 'Table added', 'table_id': table_id}
        self.wfile.write(json.dumps(response).encode())

    def handle_update_table(self, table_id):
        content_length = int(self.headers.get('Content-Length'))
        post_data = json.loads(self.rfile.read(content_length))
        table_service.update_table(table_id, post_data['restaurant_id'], post_data['table_number'], post_data['capacity'], post_data['is_available'])
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {'message': 'Table updated'}
        self.wfile.write(json.dumps(response).encode())

    def handle_delete_table(self):
        # Implementation of deleting a table
        pass

    def handle_get_table(self):
        # Implementation of retrieving table details
        # Extract table ID from the URL
        table_id = int(self.path.split('/')[-1])
        table = table_service.get_table_by_id(table_id)
        if table:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(table).encode('utf-8'))
        else:
            self.send_error(404, 'Table not found')

    def handle_get_all_tables(self):
        tables = table_service.get_all_tables()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'tables': tables}).encode())

    def handle_get_table_by_id(self, table_id):
        table = table_service.get_table_by_id(table_id)
        if table:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'table': table}).encode())
        else:
            self.send_error(404, 'Table not found')















# class PatientHandler:
#     def handle_add_patient(self):
#         length = int(self.headers.get('Content-Length'))
#         post_data = json.loads(self.rfile.read(length))
#         patient_id = patient_service.add_patient(post_data['user_id'], post_data['assigned_doctor_id'], post_data['date_of_birth'], post_data['gender'], post_data['phone_number'], post_data['emergency_contact'])
#         self.send_response(200)
#         self.send_header('Content-Type', 'application/json')
#         self.end_headers()
#         response = {'message': 'Patient added', 'patient_id': patient_id}
#         self.wfile.write(json.dumps(response).encode())
#         pass

#     def handle_update_patient(self, patient_id):
#         length = int(self.headers.get('Content-Length'))
#         post_data = json.loads(self.rfile.read(length))
#         patient_service.update_patient(patient_id, post_data['assigned_doctor_id'], post_data['date_of_birth'], post_data['gender'], post_data['phone_number'], post_data['emergency_contact'])
#         self.send_response(200)
#         self.send_header('Content-Type', 'application/json')
#         self.end_headers()
#         response = {'message': 'Patient updated'}
#         self.wfile.write(json.dumps(response).encode())
#         pass

#     def handle_delete_patient(self):
#         # Implementation of deleting a patient
#         pass

#     def handle_get_patient(self):
#         # Implementation of retrieving patient details
#         # Extract patient ID from the URL
#         patient_id = int(self.path.split('/')[-1])
#         patient = patient_service.get_patient(patient_id)
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#         self.wfile.write(json.dumps(patient).encode('utf-8'))
#         pass
    
#     def handle_get_all_patients(self):
#         patients = patient_service.get_all_patients()
#         self.send_response(200)
#         self.send_header('Content-Type', 'application/json')
#         self.end_headers()
#         self.wfile.write(json.dumps({'patients': patients}).encode())

#     def handle_get_patient_by_id(self, patient_id):
#         patient = patient_service.get_patient_by_id(patient_id)
#         if patient:
#             self.send_response(200)
#             self.send_header('Content-Type', 'application/json')
#             self.end_headers()
#             self.wfile.write(json.dumps({'patient': patient}).encode())
#         else:
#             self.send_error(404, 'Patient not found')
            
            
            
            