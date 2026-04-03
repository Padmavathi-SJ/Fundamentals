from models import User

# Create table
User.create_table() # create DB table

# Insert
u1 = User(name="Padma", email="padma@test.com", age=20) # create object
u1.save() # insert into DB

# Query
users = User.filter(age__gte=20) # Query

print(users)