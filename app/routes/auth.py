
from http.server import BaseHTTPRequestHandler
from app.services import auth_service
import json


class AuthHandler:
    def handle_get_user_by_id(self, user_id):
        user_info = auth_service.get_user_info_by_id(user_id)
        if user_info:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'user_info': user_info}).encode())
        else:
            self.send_error(404, 'user_info not found')
