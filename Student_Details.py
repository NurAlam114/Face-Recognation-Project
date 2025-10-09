from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk  # pillow
from tkinter import messagebox
import subprocess
import mysql.connector
import os, sys, json
import cv2
import time



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
        self.var_radio1 = StringVar(value="")  # default

        
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

                self.original_id = self.var_std_id.get()

            # come to store
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
        title_lbl = Label(bg_image, text="STUDENT INFO HUB",
                          font=('Algerian', 60, "bold"), bg='white', fg='darkgreen')
        title_lbl.place(x=-130, y=0, width=1800, height=100)

        #  Student details LabelFrame
        main_frame = LabelFrame(bg_image, bd=10, relief=RIDGE, text="Student Details", font=('times new roman', 12, 'bold'))
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

        studentId_entry = Entry(student_details_frame, width=20,
                        textvariable=self.var_std_id,
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
        radiobtn1.grid(row=2, column=4, padx=1, pady=5, sticky=W)

        radiobtn2 = ttk.Radiobutton(student_details_frame, text='No Photo Sample',
                                    value="No", variable=self.var_radio1, style="Bold.TRadiobutton")
        radiobtn2.grid(row=3, column=4, padx=1, pady=5, sticky=W)

        

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
            self.var_radio1.set("")   # ✅ এখন কোনো রেডিওবাটন সিলেক্ট থাকবে না
            # flow reset
            self.selected_from_store = False



        # View Stored Data Button
        def open_store_data():
            self.open_store_for_update()

        stored_btn = Button(inner_frame_1, text="View Stored Data", width=15,
                            bg="#28a745", fg="white",
                            font=("times new roman", 13, "bold"),
                            command=open_store_data)
        stored_btn.grid(row=0, column=3, padx=27.5, pady=5)



        # Buttons frame 2
        inner_frame_2 = LabelFrame(student_details_frame, bd=3, relief=RIDGE,
                                   font=('times new roman', 12, 'bold'))
        inner_frame_2.place(x=10, y=240, width=870, height=48)


        # Take photo sample button
        take_photo_sample_button = Button(inner_frame_2, command=self.generate_dataset, text='Take Photo Sample', width=30,
                                          font=('times new roman', 13, 'bold'), bg='#4CAF50', fg='white')
        take_photo_sample_button.grid(row=0, column=1, pady=5, padx=63)


        # Update photo sample button
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
        # new ID (what user typed now)
        new_id = str(self.var_std_id.get()).strip()
        if not new_id:
            messagebox.showerror("Error", "Student ID is required", parent=self.root); return

        # original ID (what came from temp.json initially)
        original_id = getattr(self, "original_id", "").strip() or new_id

        # helper: cast optional ints
        def to_int_or_none(x):
            x = str(x).strip()
            if x == "": return None
            try: return int(x)
            except ValueError: return None

        year_val  = to_int_or_none(self.var_year.get())
        phone_val = to_int_or_none(self.var_phone.get())

        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="face_recognation",
            )
            cursor = conn.cursor()

            # 1) original row exists?
            cursor.execute("SELECT COUNT(*) FROM face_recognizer WHERE Student_ID=%s", (original_id,))
            if cursor.fetchone()[0] == 0:
                messagebox.showwarning("Not Found", f"No record found for Student ID: {original_id}", parent=self.root)
                return

            # 2) if user changed ID, ensure new_id not used by another row
            if new_id != original_id:
                cursor.execute(
                    "SELECT COUNT(*) FROM face_recognizer WHERE Student_ID=%s AND Student_ID<>%s",
                    (new_id, original_id)
                )
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Duplicate ID", f"Student ID {new_id} already exists.", parent=self.root)
                    return

            # 3) perform update (notice: Student_ID is also being updated)
            cursor.execute(
                """
                UPDATE face_recognizer SET
                    Student_ID=%s,
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
                    new_id,
                    self.var_std_name.get(), self.var_dep.get(), self.var_course.get(),
                    year_val, self.var_semester.get(), self.var_sec.get(), self.var_gender.get(),
                    self.var_blood.get(), self.var_nationality.get(), self.var_email.get(),
                    phone_val, self.var_address.get(), self.var_teacher.get(), self.var_radio1.get(),
                    original_id,  
                ),
            )
            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo("No Change", "Record exists but no changes were made.", parent=self.root)
            else:
                # update local original_id to the new one (so next updates work)
                self.original_id = new_id
                messagebox.showinfo("Success", "Student details updated successfully.", parent=self.root)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}", parent=self.root)
        finally:
            try: conn.close()
            except: pass









    # Take photo sample button finction
    def generate_dataset(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return
        try:
            sid = str(self.var_std_id.get())
            import mysql.connector
            import pyttsx3
            import threading
            import time, os, cv2

            # ========== DB Update ==========
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="face_recognation"
            )
            my_cursor = conn.cursor()
            my_cursor.execute("select * from face_recognizer")
            _ = my_cursor.fetchall()

            my_cursor.execute(
                """
                UPDATE face_recognizer SET
                    Student_ID=%s,
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
                    sid,
                    self.var_std_name.get(),
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_sec.get(),
                    self.var_gender.get(),
                    self.var_blood.get(),
                    self.var_nationality.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio1.get(),
                    sid,
                )
            )
            conn.commit()
            self.reset_form()
            conn.close()

            # ====== Face detectors ======
            face_cascade_path = "haarcascade_frontalface_default.xml"
            profile_cascade_path = "haarcascade_profileface.xml"
            if not os.path.exists(face_cascade_path):
                face_cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
            if not os.path.exists(profile_cascade_path):
                profile_cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_profileface.xml")

            face_classifier = cv2.CascadeClassifier(face_cascade_path)
            profile_cascade = cv2.CascadeClassifier(profile_cascade_path)
            if face_classifier.empty() or profile_cascade.empty():
                messagebox.showerror("Error", "Cascade files not found!", parent=self.root)
                return

            # ====== Voice guidance ======
            def speak_async(text):
                def run_voice():
                    try:
                        engine = pyttsx3.init()
                        engine.say(text)
                        engine.runAndWait()
                    except Exception:
                        pass
                threading.Thread(target=run_voice, daemon=True).start()

            # ====== Helper: pick best face (Frontal + Left + Right) ======
            def face_cropped_best(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces_f = face_classifier.detectMultiScale(gray, 1.2, 6, minSize=(80, 80))
                faces_p = profile_cascade.detectMultiScale(gray, 1.2, 6, minSize=(80, 80))

                # Left profile detection by flipping
                gray_flipped = cv2.flip(gray, 1)
                faces_p_flipped = profile_cascade.detectMultiScale(gray_flipped, 1.2, 6, minSize=(80, 80))
                faces_p_flipped_corrected = []
                for (x, y, w, h) in faces_p_flipped:
                    x_corrected = gray.shape[1] - x - w
                    faces_p_flipped_corrected.append((x_corrected, y, w, h))

                candidates = list(faces_f) + list(faces_p) + faces_p_flipped_corrected
                if not candidates:
                    return None, None

                x1, y1, x2, y2, _ = sorted(
                    [(x, y, x + w, y + h, w * h) for (x, y, w, h) in candidates],
                    key=lambda t: t[4],
                    reverse=True
                )[0]

                crop = img[y1:y2, x1:x2]
                return crop, (x1, y1, x2, y2)

            # ====== Camera init ======
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Error", "Camera not accessible!", parent=self.root)
                return
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

            img_id = 0
            save_dir = "Sample image data"
            os.makedirs(save_dir, exist_ok=True)

            messagebox.showinfo(
                "Info",
                "Camera is ON.\nFollow the instructions.\nPress Enter to stop early.",
                parent=self.root
            )

            instructions = [
                ("Look Straight", "Straight"),
                ("Turn Left", "Left"),
                ("Turn Right", "Right"),
                ("Look Down", "Down"),
            ]
            instruction_index = 0
            photos_per_pose = 25
            per_pose_count = 0
            pose_switch_grace_s = 1.5
            pose_ready_at = time.time() + pose_switch_grace_s

            speak_async("Camera is on. Please follow my instructions.")
            speak_async(instructions[instruction_index][0])

            # ====== Capture loop ======
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                current_instruction = instructions[instruction_index][0]

                cv2.putText(frame, f"Instruction: {current_instruction}", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                cv2.putText(frame, f"Pose {instruction_index+1}/{len(instructions)}  Photo {per_pose_count}/{photos_per_pose}", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                face, box = face_cropped_best(frame)

                if face is not None and face.size > 0 and time.time() >= pose_ready_at:
                    img_id += 1
                    per_pose_count += 1

                    face_resized = cv2.resize(face, (500, 500))
                    face_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
                    file_name_path = os.path.join(save_dir, f"user.{sid}.{img_id}.jpg")
                    cv2.imwrite(file_name_path, face_gray)

                    if box:
                        x1, y1, x2, y2 = box
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"Saved: {img_id}", (20, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                    if per_pose_count >= photos_per_pose:
                        instruction_index += 1
                        if instruction_index < len(instructions):
                            per_pose_count = 0
                            pose_ready_at = time.time() + pose_switch_grace_s
                            speak_async(instructions[instruction_index][0])
                        else:
                            break

                cv2.imshow("Camera Preview", frame)
                key = cv2.waitKey(150) & 0xFF
                if key == 13 or key == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
            speak_async("Dataset generation completed.")
            messagebox.showinfo("Result", f"Generating data sets completed!\nSaved: {img_id} samples", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)


      


    # def generate_dataset(self):
    #     # --------- Basic form validation ----------
    #     if (self.var_dep.get() == "Select Department" or
    #         self.var_std_name.get() == "" or
    #         self.var_std_id.get() == ""):
    #         messagebox.showerror("Error", "All Fields are required", parent=self.root)
    #         return

    #     # --------- DB UPDATE ----------
    #     try:
    #         sid = str(self.var_std_id.get())
    #         conn = mysql.connector.connect(
    #             host="localhost",
    #             user="root",
    #             password="",
    #             database="face_recognation"
    #         )
    #         cur = conn.cursor()
    #         cur.execute("""
    #             UPDATE face_recognizer SET
    #                 Student_ID=%s,
    #                 Student_Name=%s,
    #                 Department=%s,
    #                 Course=%s,
    #                 Year=%s,
    #                 Semester=%s,
    #                 Class_Section=%s,
    #                 Gender=%s,
    #                 Blood_Group=%s,
    #                 Nationality=%s,
    #                 Email=%s,
    #                 Phone_No=%s,
    #                 Address=%s,
    #                 Teacher_Name=%s,
    #                 Photo_Sample=%s
    #             WHERE Student_ID=%s
    #         """, (
    #             sid,
    #             self.var_std_name.get(),
    #             self.var_dep.get(),
    #             self.var_course.get(),
    #             self.var_year.get(),
    #             self.var_semester.get(),
    #             self.var_sec.get(),
    #             self.var_gender.get(),
    #             self.var_blood.get(),
    #             self.var_nationality.get(),
    #             self.var_email.get(),
    #             self.var_phone.get(),
    #             self.var_address.get(),
    #             self.var_teacher.get(),
    #             self.var_radio1.get(),
    #             sid
    #         ))
    #         conn.commit()
    #         try: cur.close(); conn.close()
    #         except Exception: pass
    #         # self.fetch_data()  # থাকলে আনকমেন্ট করো
    #         self.reset_form()
    #     except Exception as es:
    #         messagebox.showerror("Error", f"DB Error: {str(es)}", parent=self.root)
    #         return

    #     # --------- Capture config ----------
    #     import os, time
    #     os.makedirs("sample_image_data", exist_ok=True)

    #     face_frontal = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    #     face_profile = cv2.CascadeClassifier("haarcascade_profileface.xml")  # left-profile ধরে
    #     # ডান-প্রোফাইল ধরতে আমরা ফ্রেম flip করে একই cascade চালাবো

    #     TARGET_SAMPLES = 100
    #     REQUIRED_STABLE = 2        # টানা 2 ফ্রেম ভালো হলে সেভ
    #     BLUR_THRESH = 15.0         # কম রাখলে লো-কোয়ালিটি ক্যামেরায়ও পাস করবে
    #     MARGIN_PX = 50             # wide crop
    #     PATIENCE_NOFACE = 300      # এতগুলো ফ্রেম ফেস না পেলে hint দেখালেও লুপ চালু থাকবে
    #     MAX_RUNTIME_SEC = 300      # সেফটি: ৫ মিনিট পর ব্রেক

    #     def detect_all_faces(bgr):
    #         """frontal + left-profile + right-profile (flip trick)"""
    #         gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    #         faces_f = face_frontal.detectMultiScale(gray, 1.2, 5)

    #         faces_p_left = face_profile.detectMultiScale(gray, 1.2, 5)

    #         # right-profile: flip horizontally, detect, then map back
    #         flipped = cv2.flip(gray, 1)
    #         faces_p_right_flipped = face_profile.detectMultiScale(flipped, 1.2, 5)
    #         faces_p_right = []
    #         W = gray.shape[1]
    #         for (x, y, w, h) in faces_p_right_flipped:
    #             # flip map: x' = W - (x + w)
    #             faces_p_right.append((W - (x + w), y, w, h))

    #         all_faces = list(faces_f) + list(faces_p_left) + list(faces_p_right)
    #         return all_faces

    #     def best_face_box(bgr):
    #         """একাধিক থাকলে সবচেয়ে বড় বক্সটি নাও"""
    #         boxes = detect_all_faces(bgr)
    #         if not boxes:
    #             return None
    #         # area অনুযায়ী সবচেয়ে বড়টা
    #         boxes.sort(key=lambda r: r[2]*r[3], reverse=True)
    #         return boxes[0]

    #     def crop_with_margin(bgr, box, margin=MARGIN_PX):
    #         x, y, w, h = box
    #         H, W = bgr.shape[:2]
    #         x1 = max(0, x - margin)
    #         y1 = max(0, y - margin)
    #         x2 = min(W, x + w + margin)
    #         y2 = min(H, y + h + margin)
    #         crop = bgr[y1:y2, x1:x2]
    #         return crop if crop.size else None

    #     # --------- Camera open ----------
    #     cap = cv2.VideoCapture(0)
    #     # low webcam fix: resolution & fps সেট করো (সব ক্যামে নাও কাজ করতে পারে)
    #     cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    #     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    #     cap.set(cv2.CAP_PROP_FPS,          30)
    #     # কিছু প্ল্যাটফর্মে অটো এক্সপোজার/ফোকাস সেটগুলো no-op হতে পারে:
    #     cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # চেষ্টা; OS ভেদে ভিন্ন
    #     cap.set(cv2.CAP_PROP_AUTOFOCUS,     1)

    #     if not cap.isOpened():
    #         messagebox.showerror("Error", "Camera not found / cannot open", parent=self.root)
    #         return

    #     img_id = 0
    #     stable = 0
    #     noface_frames = 0
    #     t0 = time.time()

    #     try:
    #         while True:
    #             ok, frame = cap.read()
    #             if not ok:
    #                 if cv2.waitKey(1) & 0xFF == 27: break
    #                 continue

    #             # light/denoise (লো-কোয়ালিটি ফ্রেম smooth করতে)
    #             frame = cv2.bilateralFilter(frame, d=5, sigmaColor=25, sigmaSpace=25)

    #             box = best_face_box(frame)
    #             if box is None:
    #                 noface_frames += 1
    #                 stable = 0
    #                 cv2.putText(frame, "Show your face (front/side)", (20, 40),
    #                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    #                 cv2.imshow("Capture", frame)
    #             else:
    #                 noface_frames = 0
    #                 crop = crop_with_margin(frame, box, margin=MARGIN_PX)
    #                 if crop is None or crop.size == 0:
    #                     stable = 0
    #                     cv2.putText(frame, "Adjust position...", (20, 40),
    #                                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    #                     cv2.imshow("Capture", frame)
    #                 else:
    #                     # Sharpness check (লো threshold)
    #                     gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    #                     blur_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    #                     if blur_var >= BLUR_THRESH:
    #                         stable += 1
    #                     else:
    #                         stable = 0

    #                     # ডায়াগনস্টিক টেক্সট
    #                     x, y, w, h = box
    #                     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #                     cv2.putText(frame, f"Sharp:{blur_var:.1f}  Stable:{stable}/{REQUIRED_STABLE}", (20, 70),
    #                                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    #                     if stable >= REQUIRED_STABLE:
    #                         img_id += 1
    #                         stable = 0
    #                         face = cv2.resize(gray, (500, 500))
    #                         save_path = f"sample_image_data/user.{sid}.{img_id}.jpg"
    #                         cv2.imwrite(save_path, face)

    #                         cv2.putText(face, f"{img_id}", (20, 40),
    #                                     cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    #                         cv2.imshow("Capture", face)
    #                     else:
    #                         cv2.putText(frame, "Hold steady...", (20, 40),
    #                                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    #                         cv2.imshow("Capture", frame)

    #             # স্টপ কন্ডিশন
    #             key = cv2.waitKey(1) & 0xFF
    #             if key == 27 or key == 13:   # ESC বা Enter
    #                 break
    #             if img_id >= TARGET_SAMPLES:
    #                 break
    #             if noface_frames >= PATIENCE_NOFACE:
    #                 # অনেকক্ষণ ফেস না পেলে hint দিয়ে হলেও break
    #                 cv2.putText(frame, "No face for a while. Adjust camera/lighting.", (20, 100),
    #                             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    #                 cv2.imshow("Capture", frame)
    #                 # সামান্য বিরতি দেখাতে:
    #                 cv2.waitKey(800)
    #                 break
    #             if (time.time() - t0) > MAX_RUNTIME_SEC:
    #                 break

    #         cap.release()
    #         cv2.destroyAllWindows()
    #         messagebox.showinfo("Result",
    #             f"Generating data sets completed! Saved: {img_id}/{TARGET_SAMPLES} images")
    #     except Exception as es:
    #         cap.release()
    #         cv2.destroyAllWindows()
    #         messagebox.showerror("Error", f"Capture Error: {str(es)}", parent=self.root)








# ==================== Run Main Application ====================
if __name__ == "__main__":
    root = Tk()
    obj = Student_Details(root)
    root.mainloop()
