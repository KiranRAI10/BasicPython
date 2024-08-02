import datetime
import sys  
#  defining a function available
def available():
    # creating a dictionary
    av = {}
    # print heading of laptop details
    print("Name\t\t   ","Brand\t\t","Price\t\t   ","Quantity\t\t      ","Processor\t     ","Graphics")
    # openeing txt file in read mode
    with open('laptop.txt','r') as f:   
        for line in f:
            name, brand, price, quantity, processor, graphics= line.strip().split(', ')
            av[str(name.upper())]={'brand': brand,'price': float(price.strip("$")),'quantity': int(quantity),'processor':processor,'graphics':graphics}
            # printing all laptop details
            print(f"{name:<20}{brand:<21}{price:<22}{quantity:<23}{processor:<24}{graphics}")
        return av
    # creating a function companies
def companies():
    print("List of Available Laptops: ")
    laptopall = available()
    d= str(input("Do you want to proceed (Yes/No): "))
    # checking whether user want to continue or not
    if d.upper()=='YES':
        namedis=str(input("Enter name of distributor: "))
        namelap= str(input("Enter name of laptop: "))
        # checking whether demanded laptop is available or not
        if namelap.upper() not in laptopall:
            print("Not available")
            companies()
        else:
            laptop = laptopall[namelap.upper()]
        checked = False
        # checking condition is true or false
        while checked == False:
            # try block to catch invalid input like string
            try:
                quantity  = int(input("Enter number of laptop to purchase: "))
                # if quantity less than 0 print error message
                if (quantity <=0):
                    print("Enter valid amount")
                    checked = False
                else:
                    checked = True
            except :
                print("Please enter valid value")
        
        total_without_VAT=laptop['price']*quantity
        laptop['quantity'] +=quantity
        Vat = (0.13*total_without_VAT)
        grand_total=Vat+total_without_VAT 
    elif d.upper()=='NO':
        options()
    else :
        print("Please enter appropriate choice:")
        
    # creating a invoice 
    invoice = f'''
    *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* 
                                                  
                                                                   
    *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* 
    Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}     
    Retailer name: {namedis.upper()}                                  
   ___________________________________________________________________
    Product: {namelap.upper()}                                        
    Quantity: {quantity}                                              
    Per price: {laptop['price']:.2f}                                  
   ___________________________________________________________________
    Total without VAT: {total_without_VAT:.2f}                        
    Total: {grand_total}                                              
   ___________________________________________________________________
    Thank you for doing business with us!                             
   ___________________________________________________________________
    '''
    #  setting invoice to txt file
    with open('retail.txt','w') as f:
        f.write(invoice)
        print("Your bill has been generated")
        #  updating value in txt file
    with open('laptop.txt', 'w') as f:
        for namelap, details in laptopall.items():
            name=namelap
            brand = details ['brand']
            price = details ['price']
            quantity=details ['quantity']
            processor=details ['processor']
            graphics=details ['graphics']
            f.write(f'{name}, {brand}, ${price}, {quantity}, {processor}, {graphics}\n')
            
        
def customer():
    print("List of Available Laptops: ")
    laptopall = available()
    d= str(input("Do yo want to proceed (Yes/No): "))
    if d.upper()=='YES':
        name = str(input("Enter your name: "))
        namelap = input("Enter the name of laptop: ")
        # checking whether demanded laptop is available or not
        if namelap.upper() not in laptopall:
            print("Laptop not available")
            return customer()
        laptop_upper=laptopall[namelap.upper()]
        checked = False
        while checked == False:
            try:
                quantity  = int(input("Enter number of laptop to purchase: "))
                if (quantity <=0):
                    print("Enter valid amount")
                    checked = False
                else:
                    checked = True
            except ValueError:
                print("Please enter valid value")
            if laptop_upper['quantity']<quantity:
                print("Not enough stock")
                return customer()
        # laptop_upper['quantity']-=quantity
        price_without_shipping =laptop_upper['price']*quantity
        s = str(input("Do you want it to be shipped?"))
        if(s.upper()=='YES'):
            d = str(input("Enter your location: "))
            shipping = 50
        else:
            shipping =0
            d="none"
        total =price_without_shipping+shipping
    elif d.upper()=='NO':
        return options()

    invoice =f'''
     *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*  
     *                    Itahari Laptop Shop                      *  
     *                    Itahari-20, Sunsari                      *    
     *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*    
    Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}     
    Customer name: {name.upper()}                                                           
    Shipping Location: {d.upper()}                                      
    ___________________________________________________________________
    Product: {namelap.upper()}                                         
    Quantity: {quantity}                                               
    Per price: {laptop_upper['price']:.2f}                             
   ___________________________________________________________________             
   Shipping cost = {shipping}                                          
   Total: {total}                                                      
   ___________________________________________________________________
    Thank you for doing business with us!                              
   ___________________________________________________________________     
    '''
    
    with open ('sell_laptop.txt', 'w') as f:
        f.write(invoice)
        print("Your bill has been generated")
    laptop_upper['quantity']-= quantity
    
    with open('laptop.txt','w') as f:
        for namelap, details in laptopall.items():
            name = namelap
            brand = details['brand']
            price = details['price']
            quantity = details['quantity']
            processor = details['processor']
            graphics = details['graphics']
            f.write(f"{name}, {brand}, ${price}, {quantity}, {processor}, {graphics}\n")

    
print("-----------------------------------------------------------")
print("--------------------WELCOME TO OUR SHOP--------------------")
print("-----------------------------------------------------------")
def details():
    print("A: Available details")
    print("B: Place Order from Manufacturer")
    print("C: Buy a laptop: ")
    print("D: Exit")  
    print("Choose desired option:") 
def options():
    option= str(input())
    if option.upper()=='A':
        available()
    elif option.upper()=='B':
        companies()
    elif option.upper()=='C':
        customer()
    elif option.upper()=='D':       
        print("Thank you for shopping with us.")
        sys.exit()
    else:
        print("Enter valid option")
    options()
details()
options()