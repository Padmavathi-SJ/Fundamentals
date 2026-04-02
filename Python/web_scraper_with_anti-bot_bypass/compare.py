from db import cursor 

def get_price_changes():
    query = """
            select old.name, old.price, new.price
            from products old
            join products new
            on old.sku = new.sku
            where old.date = date('now', '-1 day')
            and new.date = date('now') 
            and old.price != new.price
            """
    return cursor.execute(query).fetchall() 