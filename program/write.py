# write.py

def update_inventory(inventory):
    with open('furniture.txt', 'w') as f:
        for item in inventory.values():
            id_ = item['id']
            brand = item['brand']
            name = item['name']
            price = item['price']
            quantity = item['quantity']
            f.write(f"{id_}, {brand}, {name}, {quantity}, ${price}\n")
