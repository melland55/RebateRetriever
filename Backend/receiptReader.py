import pdfplumber
import re
from crawler import getProductsFromItemNumbers

pdf_path = "C:\\Users\\andre\\OneDrive\\Desktop\\GIT\\RebateRetriever\\Backend\\test2.pdf"
with pdfplumber.open(pdf_path) as pdf:
    
    # Store receipt data
    product_data = []
    
    # Define regex patterns
    item_pattern = re.compile(r'([A-Z]?)\s*(\d+)\s(.*?)(\d+\.\d+)\s(\w)\s?$')
    discount_pattern = re.compile(r'(\d+)\s*/\d+\s+(\d+\.\d+)-')

    for page in pdf.pages:
        lines = page.extract_text().split('\n')
        for line in lines:
            item_match = item_pattern.match(line)
            if item_match:
                eligibility_symbol, item_code, description, price, tax_symbol = item_match.groups()
                price = float(price)
                discount = 0.0
                
                # Check for discount in the same line or the next line
                next_line_index = lines.index(line) + 1
                if next_line_index < len(lines):
                    discount_match = discount_pattern.search(lines[next_line_index])
                    if discount_match:
                        _, discount_value = discount_match.groups()
                        discount = float(discount_value)
                
                product_data.append({
                    'eligibility_symbol': eligibility_symbol,
                    'item_code': item_code,
                    'description': description.strip(),
                    'price': price,
                    'tax_symbol': tax_symbol,
                    'discount': discount
                })
    

item_numbers = [item['item_code'] for item in product_data]
getProductsFromItemNumbers(item_numbers)
    