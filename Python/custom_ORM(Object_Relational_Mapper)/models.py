from orm import Model, CharField, IntegerField # Import ORM Components

class User(Model): # Inherits from Model (which uses ModelMeta metaclass)
    name = CharField(100) # column -> varchar(100)
    email = CharField(255) # varchar(255) column
    age = IntegerField() # Integer column
    