import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Descriptor Field
class Field:
    def __init__(self, column_type): #
        self.column_type = column_type 
        self.name = None
    
    def __set_name__(self, owner, name): # called when accessing value -> user.name
        self.name = name
    
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
            if isinstance(value, Field): # collects only fields (CharField, IntegerField)
                fields[key] = value
        
        attrs["_fields"] = fields # store fields inside class as _fields
        attrs["_table"] = name.lower() # table name = class name in lowercase, ex: User -> user
                
        return super().__new__(cls, name, bases, attrs) # create the final class
            
# Base Model
class Model(metaclass=ModelMeta): # all model inherit from this
    def __init__(self, **kwargs): # accept dynamic values (name="padma")
         for key in self._fields: # assign values to fields
            setattr(self, key, kwargs.get(key))

    @classmethod # class method -> works on class, not instance
    def create_table(cls):
        columns = ["id integer primary key autoincrement"] # add default id column
                
        for name, field in cls._fields.items():
            columns.append(f"{name} {field.column_type}") # add each field to SQL
        sql = f"create table if not exists {cls._table} ({', '.join(columns)})" # build SQL query dynamically
        print("SQL: ", sql) # Debug output

        cursor.execute(sql)
        conn.commit() # execute query and save

    def save(self): # save object to database
        fields = ", ".join(self._fields.keys()) # get column names
        values = tuple(getattr(self, f) for f in self._fields) # get values from object
        placeholders = ", ".join(["?"] * len(values)) # prevent SQL injection
            
        sql = f"insert into {self._table} ({fields}) values ({placeholders})" # buil insert query
        print ("SQL:", sql)
                        
        cursor.execute(sql, values)
        conn.commit() # execute and store data
                        
                        
    @classmethod
    def filter(cls, **kwargs): # Query method
        query = f"select * from {cls._table}" # Base query
                            
        if kwargs:
            conditions = []
            values = [] # store where conditions
                            
            for key, value in kwargs.items(): # Loop through filters
                if "__gte" in key:
                    field = key.split("__")[0]
                    conditions.append(f"{field} >= ?") # Handle age__gte=20
                    
                else:
                    field = key
                    conditions.append(f"{key} = ?")
                                    
                values.append(value)
                
            query += " where " + " and ".join(conditions)
            
        print("SQL:", query)

            
        cursor.execute(query, values if kwargs else [])
        rows = cursor.fetchall()

        return rows # Return data
                                    

