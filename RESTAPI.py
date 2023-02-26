from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Define a username and password for your web app
username1 = 'myusername'
password1 = 'mypassword'

@auth.verify_password
def verify_password(username, password):
    """
    Verify the username and password provided by the client
    """
    if username1 == username and password1 == password:
        return True
    else:
        return False

# Define some sample data in a dictionary
data = {'apples': 5, 'oranges': 2, 'pears': 1}

@app.route('/api/fruits', methods=['GET'])
@auth.login_required
def get_fruits():
    """
    GET request to retrieve all the fruits
    """
    return jsonify(data)

@app.route('/api/fruits/<fruit>', methods=['GET'])
@auth.login_required
def get_fruit(fruit):
    """
    GET request to retrieve a specific fruit
    """
    if fruit in data:
        return jsonify({fruit: data[fruit]})
    else:
        return jsonify({'error': 'Fruit not found'})

@app.route('/api/fruits', methods=['POST'])
@auth.login_required
def add_fruit():
    """
    POST request to add a new fruit
    """
    fruit = request.json['fruit']
    quantity = request.json['quantity']
    data[fruit] = quantity
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
