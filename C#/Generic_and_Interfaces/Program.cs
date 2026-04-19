using System;
using System.Collections.Generic;
using System.Linq;

namespace Repository
{
    class Student
    {
        public int Id{ get; set; }
        public string? Name { get; set; }
        public int Age { get; set; }

        public override string ToString()
        {
            return $"ID: {Id}, Name: {Name}, Age: {Age}";
        }
    }

    // This is the contract that All repositories must follow
    interface IRepository<T>
    {
        void Add(T item); // create
        T? Get(int id); // Read one (returns nullable)
        List<T> GetAll(); // Read All
        void Update(T item); // update
        void Delete(int id); // delete
    }

    // Generic Repository Implementation
    // "where T : Student" means T must be a Student or derived from Student (not int, double, etc..)
    class Repository<T> : IRepository<T> where T : class
    {
        // storage
        private List<T> list = new List<T>();
        private int nextId = 1;

        // create 
        public void Add(T item)
        {
           // set the Id property using simple reflection (since we don't know the type of T, we can't directly access Id)
           var idProperty = item.GetType().GetProperty("Id");
           if (idProperty != null)
            {
                idProperty.SetValue(item, nextId);
                nextId++;
                list.Add(item);
                Console.WriteLine("Added successfully");
            }
            else
            {
                Console.WriteLine(" Item does not have an Id property!");
            }
        }

        // Read one
        public T? Get(int id)
        {
            foreach (T item in list)
            {
               var idProperty = item.GetType().GetProperty("Id");
               if (idProperty != null)
                {
                    int itemId = (int)(idProperty.GetValue(item) ?? 0);
                    if(itemId == id)
                    
                        return item;
                    
                }
            }
            return null;
        }

        // Read All
        public List<T> GetAll()
        {
            return list;
        }

        // Update
        public void Update(T item)
        {
            var idProperty = item.GetType().GetProperty("Id");
            if (idProperty == null)
            {
                Console.WriteLine("Item does not have an Id property!");
                return;
            }
            int id = (int)(idProperty.GetValue(item) ?? 0);
            T old = Get(id);

            if(old != null)
            {
                int index = list.IndexOf(old);
                list[index] = item;
                Console.WriteLine("updated successfully!");
            }
            else
            {
                Console.WriteLine("Item notfound!");
            }
        }

        // Delete
        public void Delete(int id)
        {
            T item = Get(id);
            if (item != null)
            {
                list.Remove(item);
                Console.WriteLine(" Deleted successfully!");
            }
            else
            {
                Console.WriteLine("Item not found!");
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            // create a repository foa student entities
            Repository<Student> studentRepo = new Repository<Student>();

            bool exit = false;

            while (!exit)
            {
                Console.Clear();
                Console.WriteLine("1. Add New Student");
                Console.WriteLine("2. View All Students");
                Console.WriteLine("3. Search Student by ID");
                Console.WriteLine("4. Update Student");
                Console.WriteLine("5. Delete Student");
                Console.WriteLine("6. Exit");

                Console.WriteLine("Enter your choice: ");

                string? choice = Console.ReadLine();
                Console.WriteLine();

                switch (choice)
                {
                    case "1":
                    AddStudent(studentRepo);
                    break;

                    case "2":
                    ViewAllStudents(studentRepo);
                    break;

                    case "3":
                    SearchStudent(studentRepo);
                    break;

                    case "4":
                    UpdateStudent(studentRepo);
                    break;

                    case "5":
                    DeleteStudent(studentRepo);
                    break;

                    case "6":
                    exit = true;
                    Console.WriteLine("Goodbye!");
                    break;

                    default:
                    Console.WriteLine("Invalid choice! Press any key to try again....");
                  
                    Console.ReadKey();
                    break;
                }
            }
        }

        static void AddStudent(Repository<Student> repo)
        {
            Console.WriteLine("--- ADD NEW STUDENT ---");

            Console.Write("Enter Name: ");
            string? name = Console.ReadLine();

            Console.Write("Enter Age: ");
            int age = 0;
            if (int.TryParse(Console.ReadLine(), out age)){

            Student newStudent = new Student()
            {
                Name = name ?? "Unknown",
                Age = age
            };

            repo.Add(newStudent);
            }
            else
            {
                Console.WriteLine("Invalid age!");
            }

            Console.WriteLine("\nPress any key to continue...");
            Console.ReadKey();

        }

        static void ViewAllStudents(Repository<Student> repo)
        {
            Console.WriteLine("--- ALL STUDENTS ---");
            List<Student> students = repo.GetAll();

            if (students.Count == 0)
            {
                Console.WriteLine("No student found!");
            }
            else
            {
                Console.WriteLine($"Total Students: {students.Count}");
                foreach(Student student in students)
                {
                    Console.WriteLine(student);
                }
            }
            Console.WriteLine("\nPress any key to continue...");
            Console.ReadKey();
        }

        static void SearchStudent(Repository<Student> repo)
        {
            Console.WriteLine("--- SEARCH STUDENT ---");
            Console.Write("Enter student ID: ");

            int id = 0;
            if (int.TryParse(Console.ReadLine(), out id))
            {

            Student? student = repo.Get(id);

            if(student != null)
            {
                Console.WriteLine("\n Student Found: ");
                Console.WriteLine(student);
            }
            else
            {
                Console.WriteLine("\nStudent not found!");
            }
            }
            else
            {
                Console.WriteLine("Invalid ID!");
            }

            Console.WriteLine("\nPress any key to continue...");
            Console.ReadKey();
        }

        static void UpdateStudent(Repository<Student> repo)
        {
            Console.WriteLine("--- UPDATE STUDENT ---");
            Console.WriteLine("Enter Student ID to update: ");

            int id = 0;
            if (int.TryParse(Console.ReadLine(), out id))
            {

            Student? existingStudent = repo.Get(id);

            if(existingStudent != null)
            {
                Console.WriteLine($"Current details: {existingStudent}");
                Console.WriteLine("\nEnter new details: ");

                Console.Write($"Enter Name (current: {existingStudent.Name}): ");
                
                string? name = Console.ReadLine();
                if (string.IsNullOrWhiteSpace(name))
                    name = existingStudent.Name;
                
                Console.Write($"Enter Age (current: {existingStudent.Age}): ");
               
                string? ageInput = Console.ReadLine();
                int age = existingStudent.Age;
                if (!string.IsNullOrWhiteSpace(ageInput))
                    age = int.Parse(ageInput);
                
                Student updatedStudent = new Student()
                {
                    Id = id, // keep the same ID
                    Name = name,
                    Age = age
             };
             repo.Update(updatedStudent);
            }
            else
            {
                Console.WriteLine("Student not found!");
            }
            }
            else
            {
                Console.WriteLine("Student not found!");
            }

            Console.WriteLine("\nPress any key to continue...");
            Console.ReadKey();
        }

        static void DeleteStudent(Repository<Student> repo)
        {
            Console.WriteLine("--- DELETE STUDENT ---");
            Console.Write("Enter Student ID to delete: ");
           
            int id = 0;
            if(int.TryParse(Console.ReadLine(), out id))
            {
            Student? student = repo.Get(id);

            if(student != null)
            {
                Console.WriteLine($"Are you sure you want to delete: {student.Name}?");
                
                Console.Write("Confirm (y/n): ");
                string? confirm = Console.ReadLine();

                if(confirm != null && confirm.ToLower() == "y")
                {
                    repo.Delete(id);
                }
                else
                {
                    Console.WriteLine("Deletion concalled.");
                }
            }
            else
            {
                Console.WriteLine("Student not found!");
            }
            }
            else
            {
                Console.WriteLine("Invalid ID!");
            }

            Console.WriteLine("\nPress any key to continue...");
            Console.ReadKey();
        }
    }
}