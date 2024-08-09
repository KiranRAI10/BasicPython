import datetime

VAT_RATE = 0.13

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
            VAT: {item['VAT']:.2f}
            Total with VAT: {item['grand_total']:.2f}                                              
            ___________________________________________________________________
            '''
        else:
            invoice += f'''
            Product: {item['name']}                                        
            Quantity: {item['quantity']}                                              
            Per price: {item['price']:.2f}                                  
            Total : {item['total_without_Shipping']:.2f}                        
            VAT: {item['VAT']:.2f}
            Shipping Cost: {item['shipping']:.2f}
            Total with VAT and Shipping: {item['grand_total']:.2f}                                              
            ___________________________________________________________________
            '''
    
    invoice += '''
    Thank you for your order!
    ___________________________________________________________________
    '''
    
    with open(filename, 'w') as f:
        f.write(invoice)
        print(f"Your invoice has been generated in the file '{filename}'")
