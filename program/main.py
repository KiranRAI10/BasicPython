# main.py

import sys
from operation import order_furniture, sell_furniture
from read import available

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
if __name__ == "__main__":
    print("-----------------------------------------------------------")
    print("--------------------WELCOME TO FURNITURE SHOP--------------")
    print("-----------------------------------------------------------")
    details()
    options()
