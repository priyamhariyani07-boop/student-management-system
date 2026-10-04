
import json
import os
import csv


class Students:
    def __init__(self, student_id: str, name: str, age: int,
                 email: str, Courses=None, grades=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.email = email
        self.Courses = Courses if Courses is not None else []
        self.grades = grades if grades is not None else {}

    def calculate_gpa(self) -> float:
        if not self.grades:
            return 0.0
        return round(sum(self.grades.values()) / len(self.grades), 2)

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "Courses": self.Courses,
            "grades": self.grades
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            email=data["email"],
            Courses=data.get("Courses", []),
            grades=data.get("grades", {})
        )


class StudentManagementSystem:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.filename):
            return {}

        try:
            with open(self.filename, "r") as f:
                data = json.load(f)

            return {
                student_id: Students.from_dict(info)
                for student_id, info in data.items()
            }

        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading data: {e}")
            return {}

    def _save_data(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(
                    {
                        student_id: student.to_dict()
                        for student_id, student in self.students.items()
                    },
                    f,
                    indent=4
                )
        except IOError as e:
            print(f"Error saving data to {self.filename}: {e}")

    def add_student(self, student_id: str, age: int,
                    name: str, email: str):
        if student_id in self.students:
            print(f"Student with ID {student_id} already exists.")
            return

        self.students[student_id] = Students(
            student_id=student_id,
            name=name,
            age=age,
            email=email
        )

        self._save_data()
        print(f"Student {name} added successfully.")

    def view_all_students(self):
        if not self.students:
            print("No students found.")
            return

        print("\n--- All Students ---")

        for student_id, s in self.students.items():
            gpa = s.calculate_gpa()
            print(
                f"ID: {s.student_id}, Name: {s.name}, "
                f"Age: {s.age}, Email: {s.email}, GPA: {gpa}"
            )

    def search_student(self, student_id: str):
        student = self.students.get(student_id)

        if not student:
            print(f"Student with ID {student_id} not found.")
            return

        print(
            f"ID: {student.student_id}, Name: {student.name}, "
            f"Age: {student.age}, Email: {student.email}, "
            f"GPA: {student.calculate_gpa()}"
        )

    def delete_student(self, student_id: str):
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found.")
            return

        del self.students[student_id]
        self._save_data()
        print(f"Student with ID {student_id} deleted successfully.")

    def export_to_csv(self, csv_filename="students.csv"):
        try:
            with open(csv_filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    ["Student ID", "Name", "Age", "Email", "Average Grade"]
                )

                for s in self.students.values():
                    writer.writerow([
                        s.student_id,
                        s.name,
                        s.age,
                        s.email,
                        s.calculate_gpa()
                    ])

            print(f"Data exported to {csv_filename} successfully.")

        except IOError as e:
            print(f"Error exporting data to {csv_filename}: {e}")


def main():
    sms = StudentManagementSystem()

    while True:
        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Delete Student by ID")
        print("5. Export Data to CSV")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_id = input("Enter Student ID: ")
            name = input("Enter Name: ")
            email = input("Enter Email: ")

            try:
                age = int(input("Enter Age: "))
            except ValueError:
                print("Invalid age. Please enter a number.")
                continue

            sms.add_student(student_id, age, name, email)

        elif choice == "2":
            sms.view_all_students()

        elif choice == "3":
            student_id = input("Enter Student ID to search: ")
            sms.search_student(student_id)

        elif choice == "4":
            student_id = input("Enter Student ID to delete: ")
            sms.delete_student(student_id)

        elif choice == "5":
            csv_filename = (
                input("Enter CSV filename (default: students.csv): ")
                or "students.csv"
            )
            sms.export_to_csv(csv_filename)

        elif choice == "6":
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()