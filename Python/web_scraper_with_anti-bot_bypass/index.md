--> chromium from playwright 
  --> chromium is the open-source browser project that Google Chrome is built from.
  --> browser = p.chromium.launch(headless=True)
  --> this line literally launches a real Chromium browser instance on my computer, but with headless = True, it runs invisibly in the backgound (no windows pop up).

--> what happens behind the scenes:
 --> playwright downloads Chromium - The first time you run Playwright, it downloads a complete Chromium browser(like 100-200MB)
 --> Python starts a Chromium process - It launches Chromium as a seperate backgound process
 --> Playwright controls Chromium via DevTools Protocol
 --> this script interacts with a real browser - Javascript runs, AJAX calls happen, cookies work -- everything a real user would experience

 page.goto(url) # navigate to page
 page.wait_for_selector(".product_pod) # waits for DYNAMIC content

 --> Load initial HTML structure
 --> Run javascript to fetch product data(AJAX/fetch calls)
 --> Dynamically inject (.product_pod) elements into the page
 --> Then playwright waits untill those elements exist


-> get_page_content("http://books.toscrape.com)
1. Python - "Hey Chromium, open this url"
2. Chromium - "Loading..."
3. Chroimium - "Executing all javascript on the page"
4. Chromium - "Fetching product data from APIs"
5. Chromium - Rendering final HTML with all .product_pod elements
6. Chromium - "Here's the complete, rendered HTML
7. Python: Returns that HTML to the code to parse the data.

1. requests.get() - calling a restaurant and asking for their menu(we only get text description)
2. chormium.launch() - Actually going to the restaurant, sitting down, having a waiter serve you, watching the kitchen prepare the food, then getting your meal (full experience).



--> after fetching data, need to parse the data from html string

from bs4 import BeautifulSoup
 --> A python library that turns messy HTML into a navigable tree structure.
 --> BeautifullSoup lets you "search" and "extract" like a human would:

 example:
 --> without BeautifulSoup :
 html_string = "<div class='product'><h3>Book Title</h3><p>$20</p></div>"
 -> need to find title

 --> with BeautifulSoup :
 soup.find('h3').text  --> Returns "Book Title"

--> BeautifulSoup elements behave like dictionaries for attributes.