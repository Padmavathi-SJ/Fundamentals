from orm import Model, CharField, IntegerField # Import ORM Components

class User(Model): # Define table
    name = CharField(100) # column -> varchar(100)
    email = CharField(255)
    age = IntegerField()
    