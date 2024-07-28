from flask import Flask, jsonify, request, session
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed to use sessions

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

def load_users_from_file(filename):
    users = {}
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                username, password, balance = line.strip().split(',')
                users[username] = {'password': password, 'balance': int(balance)}
    return users

def save_users_to_file(filename, users):
    with open(filename, 'w') as file:
        for username, details in users.items():
            file.write(f"{username},{details['password']},{details['balance']}\n")

# Load data from text files
dogs = load_dogs_from_file('DB.txt')
users = load_users_from_file('users.txt')

@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        user_balance = users[username]['balance']
        return jsonify({
            'header': f'Welcome {username} to the Dog Shop API',
            'balance': user_balance,
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
    users[username] = {'password': password, 'balance': 1000}  # Starting balance
    save_users_to_file('users.txt', users)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    user = users.get(username)
    if user and user['password'] == password:
        session['username'] = username
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/buy/<int:dog_id>', methods=['POST'])
def buy_dog(dog_id):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    username = session['username']
    user_balance = users[username]['balance']
    
    dog = next((d for d in dogs if d['id'] == dog_id and d['status'] == 'AVAILABLE'), None)
    if dog:
        if user_balance >= dog['price']:
            users[username]['balance'] -= dog['price']
            save_users_to_file('users.txt', users)
            save_dog_info(dog_id)
            return jsonify({
                'message': f"You have bought {dog['name']} the {dog['breed']}!",
                'dogs': dogs  # Return the updated list of dogs
            }), 200
        return jsonify({'error': 'Insufficient balance'}), 400
    return jsonify({'error': 'Dog not found'}), 404


def save_dog_info(dog_id):
    # Read the current list of dogs from the file
    with open('DB.txt', 'r') as file:
        lines = file.readlines()

    # Update the status of the purchased dog
    with open('DB.txt', 'w') as file:
        for line in lines:
            id, breed, name, price, status = line.strip().split(',')
            if int(id) == dog_id:
                # Set status to "SOLD"
                file.write(f"{id},{breed},{name},{price},SOLD\n")
            else:
                file.write(line)

    # Update the in-memory list of dogs
    global dogs
    dogs = load_dogs_from_file('DB.txt')

       

        




if __name__ == '__main__':
    app.run(debug=True)