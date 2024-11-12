from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Sample data for orders
orders = [
    {"id": 1, "user_id": 1, "product": "Laptop", "quantity": 1},
    {"id": 2, "user_id": 2, "product": "Phone", "quantity": 2},
]

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((order for order in orders if order['id'] == order_id), None)
    if order:
        # Fetch user info from user-service
        try:
            user_response = requests.get(f'http://user-service:5001/users/{order["user_id"]}')
            if user_response.status_code == 200:
                order['user'] = user_response.json()
            else:
                order['user'] = "User information not available"
        except requests.exceptions.RequestException:
            order['user'] = "User information not available"
        
        return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
