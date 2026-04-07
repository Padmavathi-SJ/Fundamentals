from models import User

# Create table
User.create_table() # create 'user' table in database

# Insert
u1 = User(name="Padma", email="padma@test.com", age=20) # create object
u1.save() # insert into DB

# Query
users = User.filter(age__gte=20) # Finds users age >= 25

print(users) # Prints raw query results