# operations.py

from datetime import datetime
from read import available
from write import update_inventory
from invoice import generate_invoice, VAT_RATE

def order_furniture(distributor_name=None, existing_order_items=None):
    print("List of Available Furniture: ")
    furniture_inventory = available()
    
    if existing_order_items is None:
        existing_order_items = []

    while True:
        if distributor_name is None:
            proceed = input("Do you want to proceed with an order (Yes/No): ")
            if proceed.upper() != 'YES':
                return

            distributor_name = input("Enter name of distributor: ")
        
        furniture_name = input("Enter name of furniture: ").strip().lower()
        if furniture_name not in furniture_inventory:
            print("Furniture not available")
            continue
        furniture_item = furniture_inventory[furniture_name]

        while True:
            try:
                quantity = int(input("Enter quantity to order: "))
                if quantity <= 0:
                    print("Enter a valid quantity greater than zero")
                else:
                    break
            except ValueError:
                print("Please enter a valid number for quantity")

        total_without_VAT = furniture_item['price'] * quantity
        vat = 0.13 * total_without_VAT  # Updated VAT calculation
        grand_total = vat + total_without_VAT

        # Update the inventory
        furniture_item['quantity'] += quantity
        existing_order_items.append({
            'name': furniture_item['name'],
            'quantity': quantity,
            'price': furniture_item['price'],
            'total_without_VAT': total_without_VAT,
            'VAT': vat,  # Include VAT in the order item
            'grand_total': grand_total
        })

        print(f"Order placed for {quantity} {furniture_item['name']}.")

        more_items = input("Do you want to add more items (Yes/No)? ")
        if more_items.upper() != 'YES':
            break

    # Generate the invoice with a unique filename
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    invoice_filename = f'manufacturer_order_{timestamp}.txt'
    generate_invoice(existing_order_items, invoice_filename, f'Distributor name: {distributor_name.upper()}', is_manufacturing=True)

    # Update the inventory file
    update_inventory(furniture_inventory)

def sell_furniture(customer_name=None, existing_purchase_items=None):
    print("List of Available Furniture: ")
    furniture_inventory = available()
    
    if existing_purchase_items is None:
        existing_purchase_items = []

    # Predefined dictionary of locations with specific shipping costs
    location_shipping_costs = {
        "Inside Valley": 50,
        "Itahari": 75,
        "Dharan": 80,
        "Biratnagar": 90,
        "Inaruwa": 85
    }

    while True:
        if customer_name is None:
            proceed = input("Do you want to proceed with a purchase (Yes/No): ")
            if proceed.upper() != 'YES':
                return

            customer_name = input("Enter your name: ")
        
        furniture_name = input("Enter the name of furniture: ").strip().lower()
        if furniture_name not in furniture_inventory:
            print("Furniture not available")
            continue
        furniture_item = furniture_inventory[furniture_name]

        while True:
            try:
                quantity = int(input("Enter quantity to purchase: "))
                if quantity <= 0:
                    print("Enter a valid quantity greater than zero")
                elif furniture_item['quantity'] < quantity:
                    print("Not enough stock")
                else:
                    break
            except ValueError:
                print("Please enter a valid number for quantity")

        price_without_shipping = furniture_item['price'] * quantity
        vat = 0.13 * price_without_shipping  # Updated VAT calculation

        shipping = 0
        if input("Do you want it to be shipped? (Yes/No) ").upper() == 'YES':
            # Display locations
            print("Choose your location:")
            for i, location in enumerate(location_shipping_costs.keys(), start=1):
                print(f"{i}. {location}")
            
            # Get user choice
            while True:
                try:
                    location_choice = int(input("Enter the number corresponding to your location: "))
                    if 1 <= location_choice <= len(location_shipping_costs):
                        location = list(location_shipping_costs.keys())[location_choice - 1]
                        shipping = location_shipping_costs[location]  # Get specific shipping cost
                        break
                    else:
                        print("Please enter a valid location number.")
                except ValueError:
                    print("Please enter a valid number for the location.")

        total = price_without_shipping + vat + shipping  # Include VAT and shipping in the total

        # Update the inventory
        furniture_item['quantity'] -= quantity
        existing_purchase_items.append({
            'name': furniture_item['name'],
            'quantity': quantity,
            'price': furniture_item['price'],
            'total_without_Shipping': price_without_shipping,
            'VAT': vat,  # Include VAT in the purchase item
            'shipping': shipping,  # Include specific shipping cost
            'grand_total': total
        })

        print(f"Purchase completed for {quantity} {furniture_item['name']}.")

        more_items = input("Do you want to add more items (Yes/No)? ")
        if more_items.upper() != 'YES':
            break

    # Generate the invoice with a unique filename
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    invoice_filename = f'customer_invoice_{timestamp}.txt'
    generate_invoice(existing_purchase_items, invoice_filename, f'Customer name: {customer_name.upper()}', is_manufacturing=False)

    # Update the inventory file
    update_inventory(furniture_inventory)
