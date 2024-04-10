Endpoints

1. Register User
   Endpoint
   POST /register
   Description
   Registers a new user in the system.

Request Body
{
"username": "example",
"password": "password123",
"email": "example@example.com",
"fullname": "John Doe"
}

Curl Example
curl -X POST -H "Content-Type: application/json" -d '{"username":"example","password":"password123","email":"example@example.com","fullname":"John Doe"}' http://localhost:8000/register

2. Login User
   Endpoint

POST /login
Description
Logs in an existing user and returns a JWT token for authentication.

Request Body
json

{
"username": "example",
"password": "password123"
}

Curl Example
curl -X POST -H "Content-Type: application/json" -d '{"username":"example","password":"password123"}' http://localhost:8000/login

3. Get All Restaurants
   Endpoint
   GET /restaurants
   Description
   Returns a list of all restaurants in the system.

Curl Example
curl http://localhost:8000/restaurants

4. Add Restaurant
   Endpoint
   POST /add_restaurant
   Description
   Adds a new restaurant to the system.
   Request Body
   json

{
"name": "Example Restaurant",
"address": "123 Main St, City",
"contact": "123-456-7890",
"opening_hours": "Mon-Sat: 10AM-8PM, Sun: 12PM-6PM",
"img": "example.jpg",
"desc": "A description of the restaurant.",
"menu_items": "Menu items in JSON format."
}

Curl Example
curl -X POST -H "Content-Type: application/json" -d '{"name":"Example Restaurant","address":"123 Main St, City","contact":"123-456-7890","opening_hours":"Mon-Sat: 10AM-8PM, Sun: 12PM-6PM","img":"example.jpg","desc":"A description of the restaurant.","menu_items":"Menu items in JSON format."}' http://localhost:8000/add_restaurant

5. Update Restaurant
   Endpoint
   PUT /update_restaurant/{restaurant_id}
   Description
   Updates an existing restaurant in the system.

Request Body
json
{
"name": "Updated Restaurant Name",
"address": "Updated Address",
"contact": "Updated Contact",
"opening_hours": "Updated Hours",
"img": "updated.jpg",
"desc": "Updated Description",
"menu_items": "Updated Menu Items"
}
Curl Example
curl -X PUT -H "Content-Type: application/json" -d '{"name":"Updated Restaurant Name","address":"Updated Address","contact":"Updated Contact","opening_hours":"Updated Hours","img":"updated.jpg","desc":"Updated Description","menu_items":"Updated Menu Items"}' http://localhost:8000/update_restaurant/1

6. Delete Restaurant
   Endpoint
   DELETE /delete_restaurant/{restaurant_id}
   Description
   Deletes an existing restaurant from the system.

Curl Example
curl -X DELETE http://localhost:8000/delete_restaurant/1

7. Get Reservation
   Endpoint
   GET /reservation/{reservation_id}
   Description
   Returns details of a specific reservation.

Curl Example
curl http://localhost:8000/reservation/1 8. Add Reservation
Endpoint

POST /add_reservation
Description
Adds a new reservation to the system.
Request Body
json

{
"user_id": 1,
"restaurant_id": 1,
"date": "2022-04-11",
"time": "20:00",
"party_size": 4,
"status": "confirmed",
"special_requests": "Special requests for the reservation."
}

Curl Example
curl -X POST -H "Content-Type: application/json" -d '{"user_id":1,"restaurant_id":1,"date":"2022-04-11","time":"20:00","party_size":4,"status":"confirmed","special_requests":"Special requests for the reservation."}' http://localhost:8000/add_reservation 9. Update Reservation
Endpoint

PUT /update_reservation/{reservation_id}
Description
Updates an existing reservation in the system.
Request Body
json

{
"user_id": 1,
"restaurant_id": 1,
"date": "2022-04-11",
"time": "20:00",
"party_size": 4,
"status": "confirmed",
"special_requests": "Special requests for the reservation."
}

Curl Example
curl -X PUT -H "Content-Type: application/json" -d '{"user_id":1,"restaurant_id":1,"date":"2022-04-11","time":"20:00","party_size":4,"status":"confirmed","special_requests":"Special requests for the reservation."}' http://localhost:8000/update_reservation/1 10. Delete Reservation
Endpoint

DELETE /delete_reservation/{reservation_id}
Description
Deletes an existing reservation from the system.

Curl Example
curl -X DELETE http://localhost:8000/delete_reservation/1
