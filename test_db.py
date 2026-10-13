from core.db import db

print("Database created successfully!")

user = db.create_user(
    "Ashwini",
    "ashwini@example.com",
    "password123"
)

print("User Created:", user)

result = db.get_user(
    "ashwini@example.com"
)

if result:

    print(dict(result))