import numpy as np

FILE_PATH = "/home/ariyan/vs project/std_info_4042.txt"

SUBJECTS = ["advanced_programming", "data_structure",
            "mathematics2", "physic", "farsi"]


class Student:

    def __init__(self, std_id, firstname, lastname, advanced_programming,
                 data_structure, mathematics2, physic, farsi):
        self.std_id = std_id
        self.firstname = firstname
        self.lastname = lastname
        self.advanced_programming = advanced_programming
        self.data_structure = data_structure
        self.mathematics2 = mathematics2
        self.physic = physic
        self.farsi = farsi

    def to_line(self):
        return ",".join([
            self.std_id, self.firstname, self.lastname,
            str(self.advanced_programming), str(self.data_structure),
            str(self.mathematics2), str(self.physic), str(self.farsi)
        ])

    @property
    def gpa(self):
        
        values = []
        for subject in SUBJECTS:
            grade = getattr(self, subject)
            if grade != "n":
                try:
                    values.append(float(grade))
                except ValueError:
                    pass
        if not values:
            return None
        return float(np.mean(np.array(values)))

    def print_grades(self):
        print(f"{self.std_id} - {self.firstname} {self.lastname}")
        subjects = {
            "advanced_programming": self.advanced_programming,
            "data_structure": self.data_structure,
            "mathematics2": self.mathematics2,
            "physic": self.physic,
            "farsi": self.farsi,
        }
        for name, grade in subjects.items():
            if grade != "n":
                print(f"    {name} : {grade}")
        gpa = self.gpa
        if gpa is not None:
            print(f"    Moadel : {gpa:.2f}")


class StudentManager:
    

    def __init__(self, filepath):
        self.filepath = filepath
        self.students = []
        self.load()

    def load(self):
        with open(self.filepath, "r") as f:
            lines = f.readlines()

        cleaned = [line.replace(" ", "").replace("\n", "").strip() for line in lines]
        if cleaned:
            cleaned.pop(0)  

        self.students = []
        for line in cleaned:
            if not line:
                continue
            parts = line.split(",")
            while len(parts) < 8:
                parts.append("n")
            self.students.append(Student(*parts[:8]))

    def save(self):
        header = "std_id,fistname,lastname,advanced_programming,data_structure,mathematics2,physic,Farsi\n"
        with open(self.filepath, "w") as f:
            f.write(header)
            for s in self.students:
                f.write(s.to_line() + "\n")

    def find_student(self, std_id):
        for s in self.students:
            if s.std_id == std_id:
                return s
        return None

    def list_students(self):
        if not self.students:
            print("hich daneshjooyi sabt nashode.")
            return
        for s in self.students:
            print("-" * 30)
            s.print_grades()

    def set_grade(self, std_id, subject, grade):
        
        student = self.find_student(std_id)
        if student is None:
            print("daneshjooyi ba in code peyda nashod.")
            return False
        if subject not in SUBJECTS:
            print("naam e dars motabar nist.")
            return False
        setattr(student, subject, str(grade))
        self.save()
        return True

    def delete_grade(self, std_id, subject):
        
        return self.set_grade(std_id, subject, "n")

    def add_student(self, std_id, firstname, lastname):
        if self.find_student(std_id):
            print("daneshjooyi ba in code az ghabl vojood darad.")
            return False
        new_student = Student(std_id, firstname, lastname, "n", "n", "n", "n", "n")
        self.students.append(new_student)
        self.save()
        return True

    def class_average(self):
        
        gpas = [s.gpa for s in self.students if s.gpa is not None]
        if not gpas:
            return None
        return float(np.mean(np.array(gpas)))

    def top_and_bottom_student(self):
        
        with_gpa = [s for s in self.students if s.gpa is not None]
        if not with_gpa:
            return None, None
        gpa_array = np.array([s.gpa for s in with_gpa])
        top_student = with_gpa[int(np.argmax(gpa_array))]
        bottom_student = with_gpa[int(np.argmin(gpa_array))]
        return top_student, bottom_student

    def bubble_sort_by_gpa(self):
        
        arr = [s for s in self.students if s.gpa is not None]
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j].gpa < arr[j + 1].gpa:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


def admin_menu(manager: StudentManager):
    while True:
        print("\n----- Admin Menu -----")
        print("1. Namayesh e list e hame daneshjoo ha va nomre hashoon")
        print("2. Sabt/Virayesh e nomre ye dars baraye daneshjoo")
        print("3. Hazf e ye dars baraye daneshjoo")
        print("4. Ezafe kardan e daneshjoo ye jadid")
        print("5. Moadel e miangin e kelas va bishtarin/kamtarin")
        print("6. Namayesh e daneshjoo ha be tartib e moadel")
        print("7. Khorooj")
        choice = input("Yek gozine ro entekhab konid: ")

        if choice == "1":
            manager.list_students()

        elif choice == "2":
            std_id = input("Code e daneshjooyi ro vared konid: ")
            print("Doroos:", ", ".join(SUBJECTS))
            subject = input("Naam e dars ro vared konid: ")
            grade = input("Nomre ro vared konid: ")
            if manager.set_grade(std_id, subject, grade):
                print("Nomre ba movafaghiat sabt shod.")

        elif choice == "3":
            std_id = input("Code e daneshjooyi ro vared konid: ")
            print("Doroos:", ", ".join(SUBJECTS))
            subject = input("Naam e darsi ke mikhahid hazf beshe ro vared konid: ")
            if manager.delete_grade(std_id, subject):
                print("dars ba movafaghiat hazf shod.")

        elif choice == "4":
            std_id = input("Code e daneshjoo ye jadid: ")
            firstname = input("Naam: ")
            lastname = input("Naam e khanevadegi: ")
            if manager.add_student(std_id, firstname, lastname):
                print("Daneshjoo ba movafaghiat ezafe shod.")

        elif choice == "5":
            avg = manager.class_average()
            if avg is None:
                print("Hich daneshjoo ba moadel peyda nashod.")
            else:
                print(f"Miangin e moadel e kelas: {avg:.2f}")
                top_student, bottom_student = manager.top_and_bottom_student()
                print(f"Bishtarin moadel: {top_student.firstname} {top_student.lastname} "
                      f"({top_student.std_id}) - {top_student.gpa:.2f}")
                print(f"Kamtarin moadel: {bottom_student.firstname} {bottom_student.lastname} "
                      f"({bottom_student.std_id}) - {bottom_student.gpa:.2f}")

        elif choice == "6":
            sorted_students = manager.bubble_sort_by_gpa()
            if not sorted_students:
                print("Hich daneshjoo ba moadel peyda nashod.")
            else:
                print("Daneshjoo ha be tartib e nozooli e moadel:")
                for rank, s in enumerate(sorted_students, start=1):
                    print(f"{rank}. {s.firstname} {s.lastname} ({s.std_id}) - {s.gpa:.2f}")

        elif choice == "7":
            break

        else:
            print("Gozine namotabar ast.")


manager = StudentManager(FILE_PATH)

logged_in = False
is_admin = False
current_student = None

while not logged_in:
    username = input("enter your username: ")
    password = input("enter your password: ")

    if username == "admin" and password == "admin":
        logged_in = True
        is_admin = True
        break

    for s in manager.students:
        if username == s.firstname and password == s.std_id:
            logged_in = True
            current_student = s
            break

    if not logged_in:
        print("username or password is incorrect")

if is_admin:
    admin_menu(manager)
else:
    current_student.print_grades()
