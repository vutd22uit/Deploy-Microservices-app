from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data storage for simplicity
users = []

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@app.route('/users', methods=['POST'])
def create_user():
    user = request.json
    if not user or 'name' not in user:
        return jsonify({'error': 'Invalid data'}), 400
    user['id'] = len(users) + 1
    users.append(user)
    return jsonify(user), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
