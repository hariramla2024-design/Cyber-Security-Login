# Login Security Monitoring System

USERNAME = "admin"
PASSWORD = "Secure123"

attempts = 0
MAX_ATTEMPTS = 3

print("================================")
print("   LOGIN SECURITY SYSTEM")
print("================================")

while attempts < MAX_ATTEMPTS:

    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == USERNAME and password == PASSWORD:
        print("\nLogin Successful!")
        print("Welcome,", username)
        break

    else:
        attempts += 1

        print("Invalid username or password!")
        print("Attempts remaining:", MAX_ATTEMPTS - attempts)

if attempts == MAX_ATTEMPTS:
    print("\nAccount temporarily blocked!")
    print("Security Alert: Too many failed attempts.")