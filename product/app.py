from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Lưu trữ data trong memory để đơn giản
products = []

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    product = request.json
    product['id'] = len(products) + 1
    products.append(product)
    return jsonify(product), 201

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product['id'] == product_id), None)
    if product:
        # Lấy thông tin user từ user-service
        try:
            user_response = requests.get(f'http://user-service:5001/users/{product["user_id"]}')
            if user_response.status_code == 200:
                product['user'] = user_response.json()
        except:
            product['user'] = None
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
