from auth.password import hash_password
from auth.password import verify_password

password = "123456"

hashed = hash_password(password)

print("Original:", password)

print("Hashed:", hashed)

result = verify_password(
    password,
    hashed
)

print("Verified:", result)