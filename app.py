from flask import Flask, jsonify, request, session
import os

app = Flask(__name__)
app.secret_key = 'mySecretKey'  # This key is necessary because i like using the session to manage the user data

def load_dogs_from_file(filename):
    dogs = []
    with open(filename, 'r') as file:
        for line in file:
            id, breed, name, price, status = line.strip().split(',')
            dogs.append({
                'id': int(id),
                'breed': breed,
                'name': name,
                'price': int(price),
                'status': status
            })
    return dogs

def load_users_from_file(filename): # DB.txt
    users = {}
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                username, password, gems = line.strip().split(',')
                users[username] = {'password': password, 'gems': int(gems)}
    return users

def save_users_to_file(filename, users): # users.txt
    with open(filename, 'w') as file:
        for username, details in users.items():
            file.write(f"{username},{details['password']},{details['gems']}\n")

def save_dog_info(dog_id, dogs_filename='DB.txt'):
    dogs = load_dogs_from_file(dogs_filename)
    with open(dogs_filename, 'w') as file:
        for dog in dogs:
            if dog['id'] == dog_id:
                file.write(f"{dog['id']},{dog['breed']},{dog['name']},{dog['price']},SOLD to {session['username']}\n")
            else: # The above and below are there because otherwise the write mode of the open() method would truncate the file thus removing existing info
                file.write(f"{dog['id']},{dog['breed']},{dog['name']},{dog['price']},{dog['status']}\n")

def update_dog_data(dogs_filename='DB.txt'):
    global dogs
    dogs = load_dogs_from_file(dogs_filename)

@app.route('/') # Base endpoint simply returns a list of dogs and the user in session's gem-balance
def home():
    if 'username' in session:
        username = session['username']
        user_balance = users[username]['gems']
        return jsonify({
            'gems': user_balance,
            'dogs': dogs
        })
    return jsonify({'header': 'Welcome to the Dog Shop API'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400
    users[username] = {'password': password, 'gems': 1000}  # Starting balance
    save_users_to_file('users.txt', users)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    user = users.get(username)
    if user and user['password'] == password:
        session['username'] = username # Saving the user to session so its easy to extract their name. I could save the whole user object but its not yet necessary
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None) # Removes user from session thus taking you back to startscreen
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/buy/<int:dog_id>', methods=['POST'])
def buy_dog(dog_id):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    username = session['username']
    user_balance = users[username]['gems']
    
    dog = next((d for d in dogs if d['id'] == dog_id and d['status'] == 'AVAILABLE'), None)
    if dog:
        if user_balance >= dog['price']:
            users[username]['gems'] -= dog['price']
            save_users_to_file('users.txt', users)
            save_dog_info(dog_id)
            update_dog_data()  # Reload dog data to reflect the purchase
            return jsonify({
                'message': f"You have bought {dog['name']} the {dog['breed']}! \nNew gem-balance: {users[username]['gems']}",
                'dogs': dogs,
                'balance': users[username]['gems']
            }), 200
        return jsonify({'error': 'Insufficient gem-balance'}), 400
    return jsonify({'error': 'Dog not found'}), 404

@app.route('/reset', methods=['POST'])
def reset_shop():
    dogs = load_dogs_from_file('DB.txt')  # Preload dogs from file so we dont truncate the DB
    with open('DB.txt', 'w') as file:
        for dog in dogs:
            id = dog['id']
            breed = dog['breed']
            name = dog['name']
            price = dog['price']
            file.write(f"{id},{breed},{name},{price},AVAILABLE\n")

    for username in users: # This part does not need to preload users as the save method does that already
        users[username]['gems'] = 1200  # Set all users to 1200 gem-balance
    save_users_to_file('users.txt', users)

    return jsonify({'message': 'Shop has been reset successfully!'}), 200   

if __name__ == '__main__':
    dogs = load_dogs_from_file('DB.txt')  
    users = load_users_from_file('users.txt')  
    # Above i initialize the two "databases"
    app.run(debug=True)
