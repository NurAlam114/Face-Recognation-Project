from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk  # pillow
from tkinter import messagebox
import subprocess
import mysql.connector
import os, sys, json


class Student_Details:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1530x790+0+0')
        self.root.title("Face Recognation System")

        # ================= Vars =================
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_sec = StringVar()
        self.var_gender = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_blood = StringVar()
        self.var_nationality = StringVar()
        self.var_teacher = StringVar()
        self.var_radio1 = StringVar(value="No")  # default

        
        self.selected_from_store = False

        # ================= Preload from temp.json =================
        base_dir = os.path.dirname(os.path.abspath(__file__))
        temp_path = os.path.join(base_dir, "temp.json")
        if os.path.exists(temp_path):
            try:
                with open(temp_path, "r", encoding="utf-8") as f:
                    student = json.load(f)
                self.var_std_id.set(student.get("id", ""))
                self.var_std_name.set(student.get("name", ""))
                self.var_dep.set(student.get("dept", ""))
                self.var_course.set(student.get("course", ""))
                self.var_year.set(str(student.get("year", "")))
                self.var_semester.set(student.get("sem", ""))
                self.var_sec.set(student.get("section", ""))
                self.var_gender.set(student.get("gender", ""))
                self.var_blood.set(student.get("blood", ""))
                self.var_nationality.set(student.get("nationality", ""))
                self.var_email.set(student.get("email", ""))
                self.var_phone.set(str(student.get("phone", "")))
                self.var_address.set(student.get("address", ""))
                self.var_teacher.set(student.get("teacher", ""))
                self.var_radio1.set(student.get("photo", "No"))
                # mark: আমরা স্টোর থেকে এসেছি
                self.selected_from_store = True
            except Exception as e:
                messagebox.showerror("File Error", f"temp.json read failed:\n{e}", parent=self.root)
            finally:
                try:
                    os.remove(temp_path)
                except:
                    pass

        # ==================== Background Image ====================
        img_bg = Image.open(r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\UI Image\background.jpg")
        img_bg = img_bg.resize((1530, 790), Image.LANCZOS)
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)

        bg_image = Label(self.root, image=self.photoimg_bg)
        bg_image.place(x=3, y=0, width=1530, height=790)

        # ==================== Title Label ====================
        title_lbl = Label(bg_image, text="STUDENT MANAGEMENT SYSTEM",
                          font=('times new roman', 40, "bold"), bg='white', fg='darkgreen')
        title_lbl.place(x=-130, y=0, width=1800, height=100)

        #  Student details LabelFrame
        main_frame = LabelFrame(bg_image, bd=10, relief=RIDGE, text="Stdent Details", font=('times new roman', 12, 'bold'))
        main_frame.place(x=255, y=170, width=1000, height=550)

        # Current course LabelFrame
        Current_Course_frame = LabelFrame(bg_image, bd=5, relief=RIDGE, text="Current course", font=('times new roman', 12, 'bold'))
        Current_Course_frame.place(x=300, y=210, width=900, height=150)

        # ---------- Department ----------
        dep_label = Label(Current_Course_frame, text="Select Department:", font=("Times New Roman", 12, "bold"), bg="light gray")
        dep_label.grid(row=0, column=0, padx=20, pady=20, sticky=W)

        dep_combo = ttk.Combobox(Current_Course_frame, textvariable=self.var_dep, font=("Times New Roman", 12), state="readonly", width=25)
        dep_combo["values"] = ("CSE", "IT", "Civil", "Pharmacy", "Mechanical", "EEE", "BBA")
        dep_combo.grid(row=0, column=1, padx=20, pady=20, sticky=W)

        # ---------- Semester ----------
        sem_label = Label(Current_Course_frame, text="Select Semester:", font=("Times New Roman", 12, "bold"), bg="light gray")
        sem_label.grid(row=0, column=2, padx=20, pady=20, sticky=W)

        sem_combo = ttk.Combobox(Current_Course_frame, textvariable=self.var_semester, font=("Times New Roman", 12), state="readonly", width=20)
        sem_combo["values"] = ("1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th")
        sem_combo.grid(row=0, column=3, padx=20, pady=20, sticky=W)

        # ---------- Course ----------
        course_label = Label(Current_Course_frame, text="Select Course:", font=("Times New Roman", 12, "bold"), bg="light gray")
        course_label.grid(row=1, column=0, padx=20, pady=10, sticky=W)

        course_combo = ttk.Combobox(Current_Course_frame, textvariable=self.var_course, font=("Times New Roman", 12), state="readonly", width=25)
        course_combo["values"] = ("Python", "Data Structures", "Math", "AI", "DBMS", "Networking")
        course_combo.grid(row=1, column=1, padx=20, pady=10, sticky=W)

        # ---------- Year ----------
        year_label = Label(Current_Course_frame, text="Select Year:", font=("Times New Roman", 12, "bold"), bg="light gray")
        year_label.grid(row=1, column=2, padx=20, pady=10, sticky=W)

        year_combo = ttk.Combobox(Current_Course_frame, textvariable=self.var_year, font=("Times New Roman", 12), state="readonly", width=20)
        year_combo["values"] = ("2020", "2021", "2022", "2023", "2024", "2025")
        year_combo.grid(row=1, column=3, padx=20, pady=10, sticky=W)

        # Student Information LabelFrame
        student_details_frame = LabelFrame(bg_image, bd=5, relief=RIDGE, text="Student Information", font=('times new roman', 12, 'bold'))
        student_details_frame.place(x=300, y=370, width=900, height=320)

        # ================= Left Column Labels & Entries =================
        # StudentID
        studentId_label = Label(student_details_frame, text="StudentID:",
                                font=("times new roman", 12, "bold"), bg="white")
        studentId_label.grid(row=0, column=0, padx=(10, 30), pady=5, sticky=W)

        studentId_entry = Entry(student_details_frame, width=20, textvariable=self.var_std_id,
                                font=("times new roman", 12, "bold"))
        studentId_entry.grid(row=0, column=1, padx=(10, 40), pady=5, sticky=W)

        # Class Section
        classSec_label = Label(student_details_frame, text="Class Section:",
                               font=("times new roman", 12, "bold"), bg="white")
        classSec_label.grid(row=1, column=0, padx=(10, 30), pady=5, sticky=W)

        classDiv_entry = Entry(student_details_frame, width=20,
                               textvariable=self.var_sec,
                               font=("times new roman", 12, "bold"))
        classDiv_entry.grid(row=1, column=1, padx=(10, 40), pady=5, sticky=W)

        # Gender
        gender_label = Label(student_details_frame, text="Gender:",
                             font=("times new roman", 12, "bold"), bg="white")
        gender_label.grid(row=2, column=0, padx=(10, 30), pady=5, sticky=W)

        gender_combobox = ttk.Combobox(student_details_frame,
                                       textvariable=self.var_gender,
                                       font=("times new roman", 12, "bold"),
                                       width=18, state="readonly")
        gender_combobox["values"] = ("Male", "Female")
        gender_combobox.grid(row=2, column=1, padx=(10, 40), pady=5, sticky=W)

        # Email
        email_label = Label(student_details_frame, text="Email:",
                            font=("times new roman", 12, "bold"), bg="white")
        email_label.grid(row=3, column=0, padx=(10, 30), pady=5, sticky=W)

        email_entry = Entry(student_details_frame, width=20,
                            textvariable=self.var_email,
                            font=("times new roman", 12, "bold"))
        email_entry.grid(row=3, column=1, padx=(10, 40), pady=5, sticky=W)

        # Address
        address_label = Label(student_details_frame, text="Address:",
                              font=("times new roman", 12, "bold"), bg="white")
        address_label.grid(row=4, column=0, padx=(10, 30), pady=5, sticky=W)

        address_entry = Entry(student_details_frame, width=20,
                              textvariable=self.var_address,
                              font=("times new roman", 12, "bold"))
        address_entry.grid(row=4, column=1, padx=(10, 40), pady=5, sticky=W)

        # ================= Right Column Labels & Entries =================
        # Student Name
        studentName_label = Label(student_details_frame, text="Student Name:",
                                  font=("times new roman", 12, "bold"), bg="white")
        studentName_label.grid(row=0, column=2, padx=(10, 30), pady=5, sticky=W)

        studentName_entry = Entry(student_details_frame, width=20,
                                  textvariable=self.var_std_name,
                                  font=("times new roman", 12, "bold"))
        studentName_entry.grid(row=0, column=3, padx=(10, 40), pady=5, sticky=W)

        # Blood group
        blood_group_label = Label(student_details_frame, text="Blood Group:",
                                  font=("times new roman", 12, "bold"), bg="white")
        blood_group_label.grid(row=1, column=2, padx=(10, 30), pady=5, sticky=W)

        blood_group_entry = Entry(student_details_frame, width=20,
                                  textvariable=self.var_blood,
                                  font=("times new roman", 12, "bold"))
        blood_group_entry.grid(row=1, column=3, padx=(10, 40), pady=5, sticky=W)

        # Nationality
        nationality_label = Label(student_details_frame, text="Nationality:",
                                  font=("times new roman", 12, "bold"), bg="white")
        nationality_label.grid(row=2, column=2, padx=(10, 30), pady=5, sticky=W)

        nationalit_entry = Entry(student_details_frame, width=20,
                                 textvariable=self.var_nationality,
                                 font=("times new roman", 12, "bold"))
        nationalit_entry.grid(row=2, column=3, padx=(10, 40), pady=5, sticky=W)

        # Phone No
        phone_label = Label(student_details_frame, text="Phone No:",
                            font=("times new roman", 12, "bold"), bg="white")
        phone_label.grid(row=3, column=2, padx=(10, 30), pady=5, sticky=W)

        phone_entry = Entry(student_details_frame, width=20,
                             textvariable=self.var_phone,
                             font=("times new roman", 12, "bold"))
        phone_entry.grid(row=3, column=3, padx=(10, 40), pady=5, sticky=W)

        # Teacher Name
        teacher_label = Label(student_details_frame, text="Teacher Name:",
                              font=("times new roman", 12, "bold"), bg="white")
        teacher_label.grid(row=4, column=2, padx=(10, 30), pady=5, sticky=W)

        teacher_entry = Entry(student_details_frame, width=20,
                              textvariable=self.var_teacher,
                              font=("times new roman", 12, "bold"))
        teacher_entry.grid(row=4, column=3, padx=(10, 40), pady=5, sticky=W)

        # Radio Button
        style = ttk.Style()
        style.configure("Bold.TRadiobutton", font=("times new roman", 12, "bold"))

        radiobtn1 = ttk.Radiobutton(student_details_frame, text='Take Photo Sample',
                                    value="Yes", variable=self.var_radio1, style="Bold.TRadiobutton")
        radiobtn1.grid(row=1, column=4, padx=1, pady=5, sticky=W)

        radiobtn2 = ttk.Radiobutton(student_details_frame, text='No Photo Sample',
                                    value="No", variable=self.var_radio1, style="Bold.TRadiobutton")
        radiobtn2.grid(row=2, column=4, padx=1, pady=5, sticky=W)

        # Stored Data Button (optional shortcut)
        def open_store_data():
            self.open_store_for_update()

        stored_btn = Button(student_details_frame, text="Stored Data", width=15,
                            bg="#28a745", fg="white",
                            font=("times new roman", 10, "bold"),
                            command=open_store_data)
        stored_btn.grid(row=3, column=4, padx=5, pady=10, sticky=W)

        # Buttons frame 1
        inner_frame_1 = LabelFrame(student_details_frame, bd=3, relief=RIDGE,
                                   font=('times new roman', 12, 'bold'))
        inner_frame_1.place(x=10, y=190, width=870, height=48)

        # Save button (INSERT)
        save_button = Button(inner_frame_1, text='Save', command=self.add_data, width=15,
                             font=('times new roman', 13, 'bold'), bg='#4CAF50', fg='white')
        save_button.grid(row=0, column=0, pady=5, padx=27.5)

        # Update button (smart: first go select, then save)
        update_button = Button(inner_frame_1, text='Update', width=15,
                               font=('times new roman', 13, 'bold'),
                               bg='#2196F3', fg='white',
                               command=self.handle_update_click)
        update_button.grid(row=0, column=1, pady=5, padx=27.5)

        # Reset button
        reset_button = Button(inner_frame_1, text='Reset', width=15,
                              font=('times new roman', 13, 'bold'),
                              bg='#9E9E9E', fg='white', command=self.reset_form)
        reset_button.grid(row=0, column=2, pady=5, padx=27.5)

        # Delete button (placeholder – implement if needed)
        delete_button = Button(inner_frame_1, text='Delete', width=15,
                               font=('times new roman', 13, 'bold'),
                               bg="#BF2E24", fg='white')
        delete_button.grid(row=0, column=3, pady=5, padx=27.5)

        # Buttons frame 2
        inner_frame_2 = LabelFrame(student_details_frame, bd=3, relief=RIDGE,
                                   font=('times new roman', 12, 'bold'))
        inner_frame_2.place(x=10, y=240, width=870, height=48)

        take_photo_sample_button = Button(inner_frame_2, text='Take Photo Sample', width=30,
                                          font=('times new roman', 13, 'bold'), bg='#4CAF50', fg='white')
        take_photo_sample_button.grid(row=0, column=1, pady=5, padx=63)

        update_photo_sample_button = Button(inner_frame_2, text='Update Photo Sample', width=30,
                                            font=('times new roman', 13, 'bold'), bg='#2196F3', fg='white')
        update_photo_sample_button.grid(row=0, column=2, pady=5, padx=63)

        # ==================== Back Button ====================
        back_btn = Button(self.root, text="←", width=3, height=1, cursor="hand2",
                          bg="#373773", fg="white",
                          font=("Segoe UI Symbol", 10, "bold"),
                          command=self.back_to_details)
        back_btn.place(x=10, y=110)

        def on_enter(e):
            back_btn["bg"] = "#e74c3c"
            back_btn["fg"] = "white"

        def on_leave(e):
            back_btn["bg"] = "#373773"
            back_btn["fg"] = "white"

        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    # ======= Smart Update click: select first, then save =======
    def handle_update_click(self):
        """
        1st click (not selected yet) -> open stored screen to select a row
        2nd click (selected_from_store == True) -> run update_data() to save
        """
        if self.selected_from_store:
            self.update_data()  # save to DB
            # Optional: reset flag so next time it goes to select again
            # self.selected_from_store = False
        else:
            self.open_store_for_update()

    def open_store_for_update(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        store_path = os.path.join(base_dir, "Student_Information_store.py")
        self.root.destroy()
        subprocess.Popen([sys.executable, store_path])

    def back_to_details(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(base_dir, "Main_UI.py")
        self.root.destroy()
        subprocess.Popen([sys.executable, main_path])

    def reset_form(self):
        self.var_dep.set("")
        self.var_course.set("")
        self.var_year.set("")
        self.var_semester.set("")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_sec.set("")
        self.var_gender.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_blood.set("")
        self.var_nationality.set("")
        self.var_teacher.set("")
        self.var_radio1.set("No")
        # flow reset
        self.selected_from_store = False

    # =============== INSERT ===============
    def add_data(self):
        if self.var_dep.get() == "":
            messagebox.showerror("Error", "Department is required", parent=self.root); return False
        if self.var_course.get() == "":
            messagebox.showerror("Error", "Course is required", parent=self.root); return False
        if self.var_year.get() == "":
            messagebox.showerror("Error", "Year is required", parent=self.root); return False
        if self.var_semester.get() == "":
            messagebox.showerror("Error", "Semester is required", parent=self.root); return False
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID is required", parent=self.root); return False
        if self.var_std_name.get() == "":
            messagebox.showerror("Error", "Student Name is required", parent=self.root); return False
        if self.var_sec.get() == "":
            messagebox.showerror("Error", "Section is required", parent=self.root); return False
        if self.var_gender.get() == "":
            messagebox.showerror("Error", "Gender is required", parent=self.root); return False
        if self.var_email.get() == "":
            messagebox.showerror("Error", "Email is required", parent=self.root); return False
        if self.var_phone.get() == "":
            messagebox.showerror("Error", "Phone is required", parent=self.root); return False
        if self.var_address.get() == "":
            messagebox.showerror("Error", "Address is required", parent=self.root); return False
        if self.var_blood.get() == "":
            messagebox.showerror("Error", "Blood Group is required", parent=self.root); return False
        if self.var_nationality.get() == "":
            messagebox.showerror("Error", "Nationality is required", parent=self.root); return False
        if self.var_teacher.get() == "":
            messagebox.showerror("Error", "Teacher Name is required", parent=self.root); return False
        if self.var_radio1.get() == "":
            messagebox.showerror("Error", "Please select Yes/No", parent=self.root); return False

        try:
            std_id = int(self.var_std_id.get())
            year = int(self.var_year.get())
            phone = int(self.var_phone.get())
        except ValueError:
            messagebox.showerror("Error", "Student ID, Year and Phone must be numbers", parent=self.root)
            return False

        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="face_recognation"
            )
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO face_recognizer (
                    Student_ID, Student_Name, Department, Course, Year, Semester,
                    Class_Section, Gender, Blood_Group, Nationality, Email, Phone_No,
                    Address, Teacher_Name, Photo_Sample
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    std_id, self.var_std_name.get(), self.var_dep.get(), self.var_course.get(),
                    year, self.var_semester.get(), self.var_sec.get(), self.var_gender.get(),
                    self.var_blood.get(), self.var_nationality.get(), self.var_email.get(),
                    phone, self.var_address.get(), self.var_teacher.get(), self.var_radio1.get(),
                ),
            )
            conn.commit()
            messagebox.showinfo("Success", "Successfully added student details", parent=self.root)
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}", parent=self.root)
            return False
        finally:
            try: conn.close()
            except: pass

    # =============== UPDATE ===============
    def update_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID is required", parent=self.root)
            return

        try:
            year_val = int(self.var_year.get()) if self.var_year.get() else None
        except ValueError:
            messagebox.showerror("Error", "Year must be a number", parent=self.root); return
        try:
            phone_val = int(self.var_phone.get()) if self.var_phone.get() else None
        except ValueError:
            messagebox.showerror("Error", "Phone must be a number", parent=self.root); return

        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="face_recognation",
            )
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE face_recognizer SET
                    Student_Name=%s,
                    Department=%s,
                    Course=%s,
                    Year=%s,
                    Semester=%s,
                    Class_Section=%s,
                    Gender=%s,
                    Blood_Group=%s,
                    Nationality=%s,
                    Email=%s,
                    Phone_No=%s,
                    Address=%s,
                    Teacher_Name=%s,
                    Photo_Sample=%s
                WHERE Student_ID=%s
                """,
                (
                    self.var_std_name.get(), self.var_dep.get(), self.var_course.get(),
                    year_val, self.var_semester.get(), self.var_sec.get(), self.var_gender.get(),
                    self.var_blood.get(), self.var_nationality.get(), self.var_email.get(),
                    phone_val, self.var_address.get(), self.var_teacher.get(), self.var_radio1.get(),
                    self.var_std_id.get(),
                ),
            )
            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Not Found", "No record found for this Student ID.", parent=self.root)
            else:
                messagebox.showinfo("Success", "Student details updated successfully", parent=self.root)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}", parent=self.root)
        finally:
            try: conn.close()
            except: pass


# ==================== Run Main Application ====================
if __name__ == "__main__":
    root = Tk()
    obj = Student_Details(root)
    root.mainloop()
