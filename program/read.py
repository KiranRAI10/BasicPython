# read.py

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
