class StudentGrades:
    def __init__(self):
        """
        Initialize the student grades system.
        This will hold a dictionary of student names and their list of grades.
        """
        self.grades = {}

    def add_student(self, name):
        """
        Add a student with no grades yet.
        """

        if name not in self.grades:
            self.grades[name] = []
            print(f"Student {name} added.")
        else:
            print(f"Student {name} already exists.")

    def add_grade(self, name, grade):
        """
        Add a grade to a student's record.
        """
        if name in self.grades:
            self.grades[name].append(grade)
            print(f"Added grade {grade} for {name}.")
        else:
            print(f"Student {name} not found!")
        
    def average_grade(self, name):
        """
        Calculate the avergae grade of a student.
        """
        if name in self.grades and self.grades[name]:
            return sum(self.grades[name]) / len(self.grades[name])
        return 0
    
    def top_students(self, min_average):
        """
        Return students with avergae grade higher than the given threshold.
        """
        return [name for name in self.grades if self.average_grade(name) > min_average]

    def __str__(self):
        """
        Return a string representation of all students and their grades.
        """
        return '\n'.join([f"{name}: {grades}" for name, grades in self.grades.items()])
    
# Example Usage
grades_system = StudentGrades()
grades_system.add_student("Alice")
grades_system.add_student("Bob")
grades_system.add_grade("Alice", 90)
grades_system.add_grade("Alice", 85)
grades_system.add_grade("Bob", 70)
grades_system.add_grade("Bob", 80)

print(f"Alice's average grade: {grades_system.average_grade('Alice')}")
print(f"Top students with average > 80: {grades_system.top_students(80)}")

print("\n All students with their grades: ")
print(grades_system)
