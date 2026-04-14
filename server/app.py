from flask import Flask, request, jsonify
import requests
from data import inventory

app = Flask(__name__)


@app.route('/items')
def get_items():
    return jsonify(inventory), 200


@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.get_json()
    if 'id' not in new_item:
        new_item['id'] = len(inventory) + 1
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((item for item in inventory if item['id'] == item_id), None)
    if item:
        data = request.get_json()
        item.update(data)
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory
    new_inventory = [item for item in inventory if item['id'] != item_id]
    inventory.clear()
    inventory.extend(new_inventory)
    return jsonify({"message": "Item deletion successful"}), 200

@app.route('/fetch-product/<barcode>', methods=['GET'])
def fetch_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 1:
            product = data['product']
            return jsonify({
                "name": product.get("product_name", "Unknown"),
                "barcode": barcode,
                "quantity": 1
            }), 200
        
    return jsonify({"error": "The product you requested was not found"}), 404
    

if __name__ == '__main__':
    app.run(debug=True)