DEFAULT_TEST_DATA = {
    "id": list(range(1, 101)),
    "name": ["User" + str(i) for i in range(1, 101)],
    "email": ["user" + str(i) + "@example.com" for i in range(1, 101)],
    "telephone_number": ["+12345678" + str(i).zfill(2) for i in range(1, 101)],
    "surname": ["Surname" + str(i) for i in range(1, 101)],
    "patronymic": ["Patronymic" + str(i) for i in range(1, 101)],
    "location": ["City" + str(i) for i in range(1, 101)],
    "sex": ["Male" if i % 2 == 0 else "Female" for i in range(1, 101)],
    "hashed_password": ["hashed_password_" + str(i) for i in range(1, 101)],
    "birth": ["1990-01-" + str((i % 28) + 1).zfill(2) for i in range(1, 101)],
    "is_active": [i % 2 == 0 for i in range(1, 101)],
    "last_active_time": ["2025-03-01 12:00:00" for _ in range(100)],
    "status": ["active" if i % 2 == 0 else "inactive" for i in range(1, 101)],
    "refresh_token_update_time": ["2025-03-01 12:00:00" for _ in range(100)],
    "created_at": ["2025-01-01 12:00:00" for _ in range(100)],
    "updated_at": ["2025-02-01 12:00:00" for _ in range(100)],

# ROUTE_TEST_DATA
    "user_id": list(range(1, 101)),
    "distance": [i * 1.5 for i in range(1, 101)],
    "users_travel_time": [i * 10 for i in range(1, 101)],
    "users_travel_speed": [i * 2 for i in range(1, 101)],
    "users_transport": ["Car" if i % 3 == 0 else "Bike" if i % 3 == 1 else "Walk" for i in range(1, 101)],
    "comment": ["Comment " + str(i) for i in range(1, 101)],
    "locname_start": ["Start" + str(i) for i in range(1, 101)],
    "locname_finish": ["Finish" + str(i) for i in range(1, 101)],


# COORDINATE_TEST_DATA
    "order": list(range(1, 101)),
    "route_id": list(range(1, 101)),
    "latitude": [50.0 + (i * 0.01) for i in range(1, 101)],
    "longitude": [30.0 + (i * 0.01) for i in range(1, 101)],


# RATING_TEST_DATA
    "value": [(i % 5) + 1 for i in range(1, 101)],
}
