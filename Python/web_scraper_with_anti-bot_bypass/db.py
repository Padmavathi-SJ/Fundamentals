import sqlite3 # import database library
from datetime import date 

conn = sqlite3.connect("products.db") # connect to a SQLite database named products.db
cursor = conn.cursor() # cursor executes sql queries

def create_table(): # function to create table
    cursor.execute("""
        create table if not exists products (
            sku text,
            name text,
            price real,
            date text
        )
    """)
    conn.commit()
    

def save_products(products): #function to insert products data
    today = str(date.today())
  
    for sku, name, price in products:
        cursor.execute(
            "insert into products values (?, ?, ?, ?)",
            (sku, name, price, today)
        )

    conn.commit() #commit changes to database
    


