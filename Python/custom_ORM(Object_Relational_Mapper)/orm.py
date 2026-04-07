import sqlite3 

conn = sqlite3.connect("database.db")  # creates/connects to SQLite file
cursor = conn.cursor() # Creates cursor for executing SQL

# Descriptor Field
class Field:
    def __init__(self, column_type): 
        self.column_type = column_type # SQL data type (e.g., "varchar(100)")
        self.name = None  # will store feild name (e.g., "name")
    
    def __set_name__(self, owner, name): # called when accessing value -> user.name
        self.name = name # store the feild name (e.g., "name", "email", "age")
    
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value): # called when setting value -> user.name = "padma"
        instance.__dict__[self.name] = value # stores value in object dictionary


class CharField(Field):
    def __init__(self, max_length):
        super().__init__(f"varchar({max_length})")  # defines string field -> SQL type VARCHAR


class IntegerField(Field):
    def __init__(self):
        super().__init__("integer") # defines integer field


# Metaclass
class ModelMeta(type): # special class that controls how models are created
    def __new__(cls, name, bases, attrs): # runs when a model class is defined
        fields = {} # dictionary to store all feild definitions
        
        for key, value in attrs.items(): # loop through class attributes
            if isinstance(value, Field): # check if it's a field and collects only fields (CharField, IntegerField)
                fields[key] = value  # store it in fields dict
        
        # Add metadata to the class
        attrs["_fields"] = fields # store fields inside class as _fields
        attrs["_table"] = name.lower() # table name = class name in lowercase, ex: User -> user

       # Create the final class   
        return super().__new__(cls, name, bases, attrs) # create the final class
            
# Base Model
class Model(metaclass=ModelMeta): # all model inherit from this
    def __init__(self, **kwargs): # accept dynamic values (name="padma")
         for key in self._fields: # loop through fields names & assign values to fields
            setattr(self, key, kwargs.get(key)) # set each field from kwargs

    @classmethod # class method -> works on class, not instance
    def create_table(cls):
        columns = ["id integer primary key autoincrement"] # add default id column

        # add each field to columns list   
        for name, field in cls._fields.items():
            columns.append(f"{name} {field.column_type}") # add each field to SQL
        
        # Build SQL query
        sql = f"create table if not exists {cls._table} ({', '.join(columns)})" # build SQL query dynamically
        print("SQL: ", sql) # Debug output

        cursor.execute(sql) # Executes SQL
        conn.commit() # execute query and save

    def save(self): # save object to database
        fields = ", ".join(self._fields.keys()) # get column names
        # for User: "name, email, age"

        values = tuple(getattr(self, f) for f in self._fields) # get values from object
        # For User: ("Alice", "alice@gmail.com", 30)

        placeholders = ", ".join(["?"] * len(values)) # prevent SQL injection
        
        # Build insert query
        sql = f"insert into {self._table} ({fields}) values ({placeholders})" # buil insert query
        print ("SQL:", sql)

        # Execute with values (safe from SQL injection)        
        cursor.execute(sql, values)
        conn.commit() # execute and store data
                        
                        
    @classmethod
    def filter(cls, **kwargs): # Query method
        query = f"select * from {cls._table}" # Base query
                            
        if kwargs:
            conditions = []
            values = [] # store where conditions
                            
            for key, value in kwargs.items(): # Loop through filters
                if "__gte" in key: # Handles greater-than-or-equal oerator
                    field = key.split("__")[0] # Extract field name
                    conditions.append(f"{field} >= ?") # Handle age__gte=20 (age >= ?)
                    
                else:
                    field = key
                    conditions.append(f"{key} = ?") # Regular equality
                                    
                values.append(value)
                
            query += " where " + " and ".join(conditions)
            
        print("SQL:", query)

            
        cursor.execute(query, values if kwargs else [])
        rows = cursor.fetchall()

        return rows # Return data
                                    

