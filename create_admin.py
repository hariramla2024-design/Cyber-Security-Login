import mysql.connector
from werkzeug.security import generate_password_hash

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="cyber_login_system"
)

cursor = db.cursor()

username = "admin"
password = "Secure123"

password_hash = generate_password_hash(password)

cursor.execute(
    """
    INSERT INTO users (username, password_hash)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE password_hash = %s
    """,
    (username, password_hash, password_hash)
)

db.commit()

print("Admin account created successfully!")
print("Username: admin")
print("Password: Secure123")

cursor.close()
db.close()