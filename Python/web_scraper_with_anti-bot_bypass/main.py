from scraper import get_page_content
from parser import parse_products
from db import create_table, save_products
from compare import get_price_changes
from report import generate_report
from utils import log, delay

def run():
    log("Scraper started")

    create_table()

    all_products = []

    for page in range(1, 6): #scrape first 5 pages
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

        html = get_page_content(url) # fetch HTML content of the page
        products = parse_products(html) # extract product data from HTML

        log(f"Page {page} - {len(products)} products extracted")

        all_products.extend(products) # add products from current page to all_products list
        
        delay() # add delay between requests to mimic human behavior and avoid bot detection

    save_products(all_products) # save all products to daatabase

    log(f"Total:{len(all_products)} products saved") # log total number of products saved to database

    changes = get_price_changes() # fetch price changes from database

    print("\n=== Price Change Report ===") # print header for price change report
    for name, old, new in changes: # iterate through price changes and print product name, old price, new price and % change
            change = ((new - old) / old) * 100 # calculate percentage change in price
            print(f"{name}: {old} -> {new} ({round(change, 2)}%)") # print product name, old price, new price and percentage change
 
    generate_report(changes) # generate csv report of price changes

if __name__ == "__main__": # check if script is run directly (not imported as a module) and call run function
    run() # start the scraper when the script is executed(Ensures run() only executes when I run main.py directly, noe when imported elsewhere)