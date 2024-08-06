import datetime
import sys

# Define constants for VAT and shipping cost
VAT_RATE = 0.13
SHIPPING_COST = 50  # Flat shipping cost

# Function to read inventory from a text file
def available():
    av = {}
    print(f"{'Name':<20}{'Brand':<30}{'Price':<10}{'Quantity':<10}")
    with open('furniture.txt', 'r') as f:
        for line in f:
            try:
                id_, brand, name, quantity, price = line.strip().split(', ')
                price = price.strip('$')
                av[name.lower()] = {
                    'id': id_,
                    'brand': brand,
                    'name': name,  # Store the original case
                    'price': float(price),
                    'quantity': int(quantity)
                }
                print(f"{name:<20}{brand:<30}{price:<10}{quantity:<10}")
            except ValueError as e:
                print(f"Error processing line: {line.strip()} - {e}")
    return av

# Function to generate invoice for multiple items
def generate_invoice(items, filename, invoice_type, is_manufacturing=True):
    invoice = f'''
    *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* 
    Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}     
    {invoice_type}
    ___________________________________________________________________
    '''
    
    for item in items:
        if is_manufacturing:
            invoice += f'''
            Product: {item['name']}                                        
            Quantity: {item['quantity']}                                              
            Per price: {item['price']:.2f}                                  
            Total without VAT: {item['total_without_VAT']:.2f}                        
            Total with VAT: {item['grand_total']:.2f}                                              
            ___________________________________________________________________
            '''
        else:
            invoice += f'''
            Product: {item['name']}                                        
            Quantity: {item['quantity']}                                              
            Per price: {item['price']:.2f}                                  
            Total without Shipping: {item['total_without_Shipping']:.2f}                        
            Total with Shipping: {item['grand_total']:.2f}                                              
            ___________________________________________________________________
            '''
    
    invoice += '''
    Thank you for your order!
    ___________________________________________________________________
    '''
    
    with open(filename, 'w') as f:
        f.write(invoice)
        print("Your invoice has been generated")

# Function to order furniture from manufacturer
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
        vat = VAT_RATE * total_without_VAT
        grand_total = vat + total_without_VAT

        # Update the inventory
        furniture_item['quantity'] += quantity
        existing_order_items.append({
            'name': furniture_item['name'],
            'quantity': quantity,
            'price': furniture_item['price'],
            'total_without_VAT': total_without_VAT,
            'grand_total': grand_total
        })

        print(f"Order placed for {quantity} {furniture_item['name']}.")
        
        more_items = input("Do you want to add more items (Yes/No)? ")
        if more_items.upper() != 'YES':
            break

    # Generate the invoice
    generate_invoice(existing_order_items, 'manufacturer_order.txt', f'Distributor name: {distributor_name.upper()}', is_manufacturing=True)

    # Update the inventory file
    with open('furniture.txt', 'w') as f:
        for item in furniture_inventory.values():
            id_ = item['id']
            brand = item['brand']
            name = item['name']
            price = item['price']
            quantity = item['quantity']
            f.write(f'{id_}, {brand}, {name}, {quantity}, ${price}\n')

# Function to handle customer purchase
def sell_furniture(customer_name=None, existing_purchase_items=None):
    print("List of Available Furniture: ")
    furniture_inventory = available()
    
    if existing_purchase_items is None:
        existing_purchase_items = []

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
        shipping = SHIPPING_COST if input("Do you want it to be shipped? (Yes/No) ").upper() == 'YES' else 0
        total = price_without_shipping + shipping

        # Update the inventory
        furniture_item['quantity'] -= quantity
        existing_purchase_items.append({
            'name': furniture_item['name'],
            'quantity': quantity,
            'price': furniture_item['price'],
            'total_without_Shipping': price_without_shipping,
            'grand_total': total
        })

        print(f"Purchase completed for {quantity} {furniture_item['name']}.")

        more_items = input("Do you want to add more items (Yes/No)? ")
        if more_items.upper() != 'YES':
            break

    # Generate the invoice
    generate_invoice(existing_purchase_items, 'customer_invoice.txt', f'Customer name: {customer_name.upper()}', is_manufacturing=False)

    # Update the inventory file
    with open('furniture.txt', 'w') as f:
        for item in furniture_inventory.values():
            id_ = item['id']
            brand = item['brand']
            name = item['name']
            price = item['price']
            quantity = item['quantity']
            f.write(f"{id_}, {brand}, {name}, {quantity}, ${price}\n")

# Display menu options
def details():
    print("A: Available details")
    print("B: Place Order from Manufacturer")
    print("C: Buy Furniture")
    print("D: Exit")
    print("Choose desired option:")

# Main options handler
def options():
    option = input()
    if option.upper() == 'A':
        available()
    elif option.upper() == 'B':
        order_furniture()
    elif option.upper() == 'C':
        sell_furniture()
    elif option.upper() == 'D':
        print("Thank you for shopping with us.")
        sys.exit()
    else:
        print("Enter a valid option")
    options()

# Entry point of the program
print("-----------------------------------------------------------")
print("--------------------WELCOME TO OUR SHOP--------------------")
print("-----------------------------------------------------------")
details()
options()
