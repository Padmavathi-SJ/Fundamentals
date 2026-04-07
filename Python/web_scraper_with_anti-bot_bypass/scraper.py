from playwright.sync_api import sync_playwright # imports playwright fro browser automation, playwright handles javascript rendered websites
from utils import log

def get_page_content(url): #function to fetch HTML page content from a url
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # Launches chrome browser and headless=True -> runs in background (no UI)
        page = browser.new_page() # opens a new browser tab
       
        log(f"Loading {url}") # logs the url being loaded
        
        page.goto(url) # opens the webpage at the given url
        page.wait_for_selector(".product_pod") # waits until elements with class .product load(this selector pattern(product_pod) is famously used by the practise website "Books to scrape"(http://books.toscrape.com/))
        
        content = page.content()
        browser.close() 
        
        return content 

