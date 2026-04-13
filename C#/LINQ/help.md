LINQ - Language Integrrated Query

--> INQ is a feature in C#, that lets us write SQL-like queries directly in our code to search, filter, sort and transform data from collections (list, arrays, databases, etc.).

without LINQ -> you write loops and if statements to manually search through data

With LINQ - you write one line that describe WHAT you want, not HOW to get it.

### Three types of LINQ:

1. Query syntax(like SQL):
```
var results = from s in students 
              where s.Grade >= 80
              orderby s.Name
              select s;
```

2. Method Syntax(used dot notation):

var result = students
     .Where(s => s.Grade >= 80)
     .OrderBy(s => s.Name)


3. Mixed Syntax (combine both)
   
var result = (from s in students
              where s.Grade >= 80
              select s)
              .OrderBy(s => s.Name)
