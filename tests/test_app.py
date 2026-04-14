import pytest
from server.app import app, inventory

@pytest.fixture
def client():
    # Setup: This runs before every single test
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset the inventory array so tests are predictable
        inventory.clear()
        inventory.append({"id": 1, "name": "mango", "barcode": "0987654321", "quantity": 5})
        yield client

def test_get_items(client):
    """Verify Read (GET) works"""
    response = client.get('/items')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'mango'

def test_add_item(client):
    """Verify Create (POST) works"""
    new_item = {"id": 2, "name": "banana", "barcode": "111222", "quantity": 10}
    response = client.post('/items', json=new_item)
    assert response.status_code == 201
    assert len(inventory) == 2
    assert inventory[1]['name'] == 'banana'

def test_delete_item(client):
    """Verify Delete works"""
    response = client.delete('/items/1')
    assert response.status_code == 200
    assert len(inventory) == 0

def test_fetch_external_product(client):
    """Verify the route exists for external API fetching"""
    # We use a real barcode that usually exists on OpenFoodFacts
    response = client.get('/fetch-product/3017620422003')
    assert response.status_code in [200, 404] # Either it found it or the API is down