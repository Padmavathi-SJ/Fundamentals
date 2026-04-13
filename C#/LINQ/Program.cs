using System;
using System.Collections.Generic;
using System.Linq; 

namespace StudentManagement
{
    // Student class with properties
    class Student
    {
        public string Name {get; set;}
        public int Grade {get; set;}
        public int Age { get; set; }

        // Constructor to create students
        public Student(string name, int grade, int age)
        {
            Name = name;
            Grade = grade;
            Age = age;
    }

    // Method to display student info
    public void Display()
        {
            Console.WriteLine($"Name: {Name, -10} | Grade: {Grade, 3} | Age: {Age, 2}");
        }
}

class Program
    {
        static void Main(string[] args)
        {
            List<Student> students = new List<Student>
            {
                new Student("Aliya", 85, 20),
                new Student("Balia", 72, 19),
                new Student("Calia", 91, 21),
                new Student("Dalia", 68, 20),
                new Student("Ealia", 79, 22),
                new Student("Falia", 94, 19),
                new Student("Galia", 65, 21),
                new Student("Halia", 88, 20)
            };

            // Display all students
            Console.WriteLine("=== All Students ===");
            Console.WriteLine("Name        | Grade | Age");
            Console.WriteLine("-------------------------------");
            foreach (var student in students)
            {
                student.Display();
            }

            // Get grade threshold from users
            Console.Write("\nEnter minimun grade threshold (eg:, 75): ");
            int threshold = Convert.ToInt32(Console.ReadLine());

            // using LINQ to filter and sort
            var filteredAndSorted = from student in students
                                    where student.Grade >= threshold
                                    orderby student.Name
                                    select student;
            
            // Display Results
            Console.WriteLine($"\n=== Students with Grade >= {threshold} (sorted by Name) ===");
            Console.WriteLine("Name     | Grade | Age");

            if(filteredAndSorted.Any()) // check if students match
            {
                foreach(var student in filteredAndSorted)
                {
                    student.Display();
                }
                Console.WriteLine($"\nTotal students found: {filteredAndSorted.Count()}");

            }
            else
            {
                Console.WriteLine("No students found with grade above the threshold!");
            }

        }
    }
}