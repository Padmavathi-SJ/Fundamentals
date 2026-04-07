from bs4 import BeautifulSoup # import HTML parser

def parse_products(html): #function to extract product data
    soup = BeautifulSoup(html, "lxml") # converts HTMl -> structured format, lxml -> data parser(A fast, C-based HTML/XML parser. like the "engine" that reads the HTML.) 
    products = [] # empty list to store products
    
    for item in soup.select(".product_pod"): #finds all elements with class .product
        name = item.select_one("h3 a")["title"].strip() # extract product name from elements with class .title and removes extra spaces(.strip()) (.select_one gets the first <a> inside <h3>)
      
        price_text = item.select_one(".price_color").text.strip()
        price = float(price_text.replace("£", "").replace(",", "")) #removes $ and , and converts string -> float

        sku = name
        
        products.append((sku, name, price)) #add product data as tuple to products list
        
    return products
