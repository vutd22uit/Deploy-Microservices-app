from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# In-memory data storage for simplicity
products = []

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products), 200

@app.route('/products', methods=['POST'])
def create_product():
    product = request.json
    if not product or 'name' not in product or 'user_id' not in product:
        return jsonify({'error': 'Invalid data'}), 400
    product['id'] = len(products) + 1
    products.append(product)
    return jsonify(product), 201

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product['id'] == product_id), None)
    if product:
        # Fetch user info from user-service
        try:
            user_response = requests.get(f'http://user-service:5001/users/{product["user_id"]}')
            if user_response.status_code == 200:
                product['user'] = user_response.json()
            else:
                product['user'] = {'error': 'User not found'}
        except requests.exceptions.RequestException:
            product['user'] = {'error': 'User service unavailable'}
        return jsonify(product), 200
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
