

from jose import jwt

SECRET_KEY = "Yx7JgK4nB9vM8wTqZ2LkR6dP1XyCfV5sA0mN3oU8JdT7GzWQvFbYpH2RxM6K"
ALGORITHM = "HS256"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMiIsInRlbmFudF9pZCI6MzIsImV4cCI6MTc0MjM5Mzc2Nn0.E0VnN29oaWXN6frS4-l2gSiqfnt137QZCV-FnD62TNs"
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(decoded)  # Should contain "sub" (user_id) and "tenant_id"
except Exception as e:
    print("Token decode error:", e)