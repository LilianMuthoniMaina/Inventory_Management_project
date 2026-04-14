import requests

BASE_URL = "http://127.0.0.1:5555"

def main():
    print("-----------------------------------------")
    print("Welcome to the Inventory Management System")
    print("------------------------------------------")
    print("Select an option:")
    print("1. View inventory items")
    print("2. Add a new item")
    print("3. Update an existing item")
    print("4. Delete an item")
    print("5. Fetch product information")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")

    if choice == '1':
        view_inventory()
    elif choice == '2':
        add_item()
    elif choice == '3':
        update_item()
    elif choice == '4':
        delete_item()
    elif choice == '5':
        fetch_product()
    elif choice == '6':
        print("Exiting......")
        break
    else:
        print("Invalid choice. Please try again.")



def view_inventory():
    response = requests.get(f"{BASE_URL}/items")
    if response.status_code == 200:
        items = response.json()
        print("-----Inventory Items-----:")
        for item in items:
            print(f"ID: {item['id']}, Name: {item['name']}, Barcode: {item.get('barcode', 'N/A')}, Quantity: {item['quantity']}")
    else:
        print("Failed to retrieve inventory items.")


def add_item():
    name = input("Enter item name: ")
    barcode = input("Enter item barcode: ")
    quantity = int(input("Enter item quantity: "))
    new_item = {"name": name, "barcode": barcode, "quantity": quantity}
    response = requests.post(f"{BASE_URL}/items", json=new_item)
    if response.status_code == 201:
        print("Item added successfully.")
    else:
        print("Failed to add item.")


def update_item():
    item_id = int(input("Enter the ID of the item to update: "))
    name = input("Enter new item name (leave blank to keep current): ")
    barcode = input("Enter new item barcode (leave blank to keep current): ")
    quantity_input = input("Enter new item quantity (leave blank to keep current): ")

    update_data = {}
    if name:
        update_data["name"] = name
    if barcode:
        update_data["barcode"] = barcode
    if quantity_input:
        update_data["quantity"] = int(quantity_input)

    response = requests.patch(f"{BASE_URL}/items/{item_id}", json=update_data)
    if response.status_code == 200:
        print("Item updated successfully.")
    else:
        print("Failed to update item.")


def delete_item():
    item_id = int(input("Enter the ID of the item to delete: "))
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    if response.status_code == 200:
        print("Item deleted successfully.")
    else:
        print("Failed to delete item.")


def fetch_product():
    barcode = input("Enter the barcode of the product to fetch: ")
    print("Fetching product information......")
    response = requests.get(f"{BASE_URL}/fetch-product/{barcode}")
    if response.status_code == 200:
        product = response.json()
        print(f"Product Name: {product['name']}, Barcode: {product['barcode']}, Quantity: {product['quantity']}")
        add_to_inventory = input("Do you want to add this product to the inventory? (yes/no): ")
        if add_to_inventory.lower() == 'yes':
            response = requests.post(f"{BASE_URL}/items", json=product)
            if response.status_code == 201:
                print("Product added to inventory successfully.")
            else:
                print("Failed to add product to inventory.")
    else:
        print("Failed to fetch product information.")




if __name__ == "__main__":
    main()