from core.auth import auth

print("=" * 50)

print("Testing Registration")

status, message = auth.register(
    username="Ashwini",
    email="ashwini@example.com",
    password="Password123"
)

print(status)
print(message)

print("=" * 50)

print("Testing Login")

status, user = auth.login(
    "ashwini@example.com",
    "Password123"
)

print(status)

print(user)