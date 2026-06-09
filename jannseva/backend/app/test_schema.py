from app.schemas.user import UserRegister

user = UserRegister(
    name="Krishna",
    email="Krishna01@gmail.com",
    password="123456"
)

print(user)