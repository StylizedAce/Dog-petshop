import requests
import subprocess
import time
import sys # So the exit function can actually close the app

BASE_URL = "http://localhost:5000"
session = requests.Session()  # session object to funnel REST operations through


# ------ app.py launch --- 

    # This is here so you wont have to run two different terminals and instead just run client.py

def startApp():
    return subprocess.Popen(["python", "app.py"])

def stopApp(process):
    process.terminate()

#---------



def register_user():
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    response = session.post(f"{BASE_URL}/register", json={'username': username, 'password': password})
    if response.status_code == 201:
        print("User registered successfully.")
    else:
        print("Error:", response.json().get('error', 'Unknown error')) # Should throw errorcode in realscale application

def login_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    response = session.post(f"{BASE_URL}/login", json={'username': username, 'password': password})
    if response.status_code == 200:
        print("Login successful.")
        print(f"Welcome {username} !")
        return username
    else:
        print("Error:", response.json().get('error', 'Invalid credentials'))
        return None

def logout_user():
    response = session.post(f"{BASE_URL}/logout")
    if response.status_code == 200:
        print("Logout successful.")
    else:
        print("Error:", response.json().get('error', 'Unknown error')) # Should throw errorcode in realscale application

def show_dogs():
    response = session.get(BASE_URL)
    if response.status_code == 200:
        data = response.json()
        print("\nDogs available:")
        for dog in data['dogs']:
            if dog['status'] == 'AVAILABLE':
                print(f"{dog['id']}. {dog['breed']} - {dog['name']} - {dog['price']} gems")
        print(f"\nYour gem-balance: ${data['gems']}")
    else:
        print("Error:", response.json().get('error', 'Unauthorized'))

def buy_dog():
    while True:
        try:
            dog_id = (input("Enter the ID of the dog you want to buy, or write exit to leave: "))
            if isinstance(dog_id, str):
                if dog_id == "exit":
                    break
            dog_id = int(dog_id)
            response = session.post(f"{BASE_URL}/buy/{dog_id}")
            if response.status_code == 200:
                print(response.json()['message'])
                break  # Exit the loop after a successful purchase
            else:
                print("Error:", response.json().get('error', 'Unknown error or insufficient balance'))
                break  # Exit the loop if there's an error in the response
        except ValueError:
            print("Invalid input. Please enter a valid dog ID.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break  # Exit the loop in case of unexpected errors


def reset_shop():
    response = session.post(f"{BASE_URL}/reset")


def main():

    print("Starting server...")

    # Start the Flask app
    flask_process = startApp()

    # Give the server some time to start up
    time.sleep(2)

    if flask_process:
        print("\nServer started \nBeginning application...\n")
    else:
        print("Error starting server!")


    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            register_user()
        elif choice == '2':
            username = login_user()
            if username:
                while True:
                    print("\n1. View Dogs")
                    print("2. Buy Dog")
                    print("3. Logout")
                    print("4. Reset shop (Dev)")
                    choice = input("Choose an option: ")
                    
                    if choice == '1':
                        show_dogs()
                    elif choice == '2':
                        buy_dog()
                    elif choice == '3':
                        logout_user()
                        break
                    elif choice == '4':
                        reset_shop()
                        break
                    else:
                        print("Invalid choice, please try again.")
        elif choice == '3':
            stopApp(flask_process)
            sys.exit()
        else:
            print("Invalid choice, please choose one of the given options")

if __name__ == '__main__':
    main()
