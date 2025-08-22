from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk  # pillow
import subprocess



class Student_Details:
    def exit_app(self):
        self.root.destroy()

    def __init__(self, root):
        self.root = root
        self.root.geometry('1530x790+0+0')
        self.root.title("Face Recognation System")

        # variables
        # self.var_dep = StringVar()
        # self.var_course = StringVar()
        # self.var_year = StringVar()
        # self.var_semester = StringVar()
        # self.var_std_id = StringVar()
        # self.var_std_name = StringVar()
        # self.var_sec = StringVar()
        # self.var_roll = StringVar()
        # self.var_gender = StringVar()
        # self.var_email = StringVar()
        # self.var_phone = StringVar()
        # self.var_address = StringVar()
        # self.var_blood = StringVar()
        # self.var_nationality = StringVar()
        # self.var_photo = StringVar(value="No") 

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


        #  Student details LebelFrame
        main_frame = LabelFrame( bg_image,bd=10,relief=RIDGE,text="Stdent Details",font=('times new roman',12,'bold'))
        main_frame.place(x=255,y=170,width=1000,height=550)

        # Current ourse LebelFrame
        Current_Course_frame = LabelFrame( bg_image,bd=5,relief=RIDGE,text="Current course",font=('times new roman',12,'bold'))
        Current_Course_frame.place(x=300,y=210,width=900,height=150)


        # ---------- Department ----------
        dep_label = Label(Current_Course_frame, text="Select Department:", font=("Times New Roman", 12, "bold"), bg="light gray")
        dep_label.grid(row=0, column=0, padx=20, pady=20, sticky=W)

        dep_combo = ttk.Combobox(Current_Course_frame, font=("Times New Roman", 12), state="readonly", width=25)
        dep_combo["values"] = ("Select Department", "CSE", "IT", "Civil", "Pharmacy", "Mechanical", "EEE", "BBA")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=20, pady=20, sticky=W)

        # ---------- Semester ----------
        sem_label = Label(Current_Course_frame, text="Select Semester:", font=("Times New Roman", 12, "bold"), bg="light gray")
        sem_label.grid(row=0, column=2, padx=20, pady=20, sticky=W)

        sem_combo = ttk.Combobox(Current_Course_frame, font=("Times New Roman", 12), state="readonly", width=20)
        sem_combo["values"] = ("Select Semester", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th")
        sem_combo.current(0)
        sem_combo.grid(row=0, column=3, padx=20, pady=20, sticky=W)

        # ---------- Course ----------
        course_label = Label(Current_Course_frame, text="Select Course:", font=("Times New Roman", 12, "bold"), bg="light gray")
        course_label.grid(row=1, column=0, padx=20, pady=10, sticky=W)

        course_combo = ttk.Combobox(Current_Course_frame, font=("Times New Roman", 12), state="readonly", width=25)
        course_combo["values"] = ("Select Course", "Python", "Data Structures", "Math", "AI", "DBMS", "Networking")
        course_combo.current(0)
        course_combo.grid(row=1, column=1, padx=20, pady=10, sticky=W)

        # ---------- Year ----------
        year_label = Label(Current_Course_frame, text="Select Year:", font=("Times New Roman", 12, "bold"), bg="light gray")
        year_label.grid(row=1, column=2, padx=20, pady=10, sticky=W)

        year_combo = ttk.Combobox(Current_Course_frame, font=("Times New Roman", 12), state="readonly", width=20)
        year_combo["values"] = ("Select Year", "2020", "2021", "2022", "2023", "2024", "2025")
        year_combo.current(0)
        year_combo.grid(row=1, column=3, padx=20, pady=10, sticky=W)





        # Student Information LebelFrame
        student_details_frame = LabelFrame( bg_image,bd=5,relief=RIDGE,text="Student Information",font=('times new roman',12,'bold'))
        student_details_frame.place(x=300,y=370,width=900,height=320)

        # ================= Left Column Labels & Entries =================
        # StudentID
        studentId_label = Label(student_details_frame, text="StudentID:", 
                                font=("times new roman", 12, "bold"), bg="white")
        studentId_label.grid(row=0, column=0, padx=(10,30), pady=5, sticky=W)

        studentId_entry = Entry(student_details_frame, width=20, 
                                font=("times new roman", 12, "bold"))
        studentId_entry.grid(row=0, column=1, padx=(10,40), pady=5, sticky=W)

        # Class Section
        classSec_label = Label(student_details_frame, text="Class Section:", 
                            font=("times new roman", 12, "bold"), bg="white")
        classSec_label.grid(row=1, column=0, padx=(10,30), pady=5, sticky=W)

        classDiv_entry = Entry(student_details_frame, width=20, 
                            font=("times new roman", 12, "bold"))
        classDiv_entry.grid(row=1, column=1, padx=(10,40), pady=5, sticky=W)

        # Gender
        gender_label = Label(student_details_frame, text="Gender:", 
                            font=("times new roman", 12, "bold"), bg="white")
        gender_label.grid(row=2, column=0, padx=(10,30), pady=5, sticky=W)

        gender_entry = Entry(student_details_frame, width=20, 
                            font=("times new roman", 12, "bold"))
        gender_entry.grid(row=2, column=1, padx=(10,40), pady=5, sticky=W)

        # Email
        email_label = Label(student_details_frame, text="Email:", 
                            font=("times new roman", 12, "bold"), bg="white")
        email_label.grid(row=3, column=0, padx=(10,30), pady=5, sticky=W)

        email_entry = Entry(student_details_frame, width=20, 
                            font=("times new roman", 12, "bold"))
        email_entry.grid(row=3, column=1, padx=(10,40), pady=5, sticky=W)

        # Address
        address_label = Label(student_details_frame, text="Address:", 
                            font=("times new roman", 12, "bold"), bg="white")
        address_label.grid(row=4, column=0, padx=(10,30), pady=5, sticky=W)

        address_entry = Entry(student_details_frame, width=20, 
                            font=("times new roman", 12, "bold"))
        address_entry.grid(row=4, column=1, padx=(10,40), pady=5, sticky=W)

        # ================= Right Column Labels & Entries =================
        # Student Name
        studentName_label = Label(student_details_frame, text="Student Name:", 
                                font=("times new roman", 12, "bold"), bg="white")
        studentName_label.grid(row=0, column=2, padx=(10,30), pady=5, sticky=W)

        studentName_entry = Entry(student_details_frame, width=20, 
                                font=("times new roman", 12, "bold"))
        studentName_entry.grid(row=0, column=3, padx=(10,40), pady=5, sticky=W)

        # Blood group
        blood_group_label = Label(student_details_frame, text="Blood Group:", 
                            font=("times new roman", 12, "bold"), bg="white")
        blood_group_label.grid(row=1, column=2, padx=(10,30), pady=5, sticky=W)

        blood_group_entry = Entry(student_details_frame, width=20, 
                            font=("times new roman", 12, "bold"))
        blood_group_entry.grid(row=1, column=3, padx=(10,40), pady=5, sticky=W)

        # Nationality
        nationality_label = Label(student_details_frame, text="Nationality:", 
                        font=("times new roman", 12, "bold"), bg="white")
        nationality_label.grid(row=2, column=2, padx=(10,30), pady=5, sticky=W)

        nationalit_entry = Entry(student_details_frame, width=20, 
                        font=("times new roman", 12, "bold"))
        nationalit_entry.grid(row=2, column=3, padx=(10,40), pady=5, sticky=W)

        # Phone No
        phone_label = Label(student_details_frame, text="Phone No:", 
                            font=("times new roman", 12, "bold"), bg="white")
        phone_label.grid(row=3, column=2, padx=(10,30), pady=5, sticky=W)

        phone_entry = Entry(student_details_frame, width=20, 
                            font=("times new roman", 12, "bold"))
        phone_entry.grid(row=3, column=3, padx=(10,40), pady=5, sticky=W)

        # Teacher Name
        teacher_label = Label(student_details_frame, text="Teacher Name:", 
                            font=("times new roman", 12, "bold"), bg="white")
        teacher_label.grid(row=4, column=2, padx=(10,30), pady=5, sticky=W)

        teacher_entry = Entry(student_details_frame, width=20, 
                            font=("times new roman", 12, "bold"))
        teacher_entry.grid(row=4, column=3, padx=(10,40), pady=5, sticky=W)




        # Radio Button
        photo_var = StringVar(value="No") 
        style = ttk.Style()
        style.configure("Bold.TRadiobutton", 
        font=("times new roman", 12, "bold"))

        radiobtn1 = ttk.Radiobutton(student_details_frame,text='Take Photo Sample',value="Yes",variable=photo_var,style="Bold.TRadiobutton",)
        radiobtn1.grid(row=1,column=4,padx=1, pady=5, sticky=W)

        radiobtn2 = ttk.Radiobutton(student_details_frame,text='No Photo Sample',value="No",variable=photo_var,style="Bold.TRadiobutton")
        radiobtn2.grid(row=2,column=4,padx=1, pady=5, sticky=W)

        # Stored Data Button
        def open_store_data():
            subprocess.Popen(["python", "Student_Information_store.py"], shell=True)

        stored_btn = Button(student_details_frame,
                            text="Stored Data",
                            width=15,   
                            height=2,  
                            bg="#28a745", 
                            fg="white",
                            font=("times new roman", 12, "bold"),
                            command=open_store_data)  # <--- command যুক্ত করতে হবে
        stored_btn.grid(row=3, column=4, padx=5, pady=10, sticky=W)

        



        # Buttons frame 1
        inner_frame_1 = LabelFrame(student_details_frame, bd=3, relief=RIDGE,
                         font=('times new roman', 12, 'bold'))
        inner_frame_1.place(x=10, y=180, width=870, height=48)

        # Save button
        take_photo_sample_button = Button(inner_frame_1, text='Save',width=15,font=('times new roman',13,'bold'),bg='#4CAF50',fg='white')
        take_photo_sample_button.grid(row=0,column=0,pady=5,padx=27.5)

        # Update button
        take_photo_sample_button = Button(inner_frame_1, text='Update',width=15,font=('times new roman',13,'bold'),bg='#2196F3',fg='white')
        take_photo_sample_button.grid(row=0,column=1,pady=5,padx=27.5)

        # Reset button
        take_photo_sample_button = Button(inner_frame_1, text='Reset',width=15,font=('times new roman',13,'bold'),bg='#9E9E9E',fg='white')
        take_photo_sample_button.grid(row=0,column=2,pady=5,padx=27.5)

        # Delete button
        take_photo_sample_button = Button(inner_frame_1, text='Delete',width=15,font=('times new roman',13,'bold'),bg="#BF2E24",fg='white')
        take_photo_sample_button.grid(row=0,column=3,pady=5,padx=27.5)


        # Buttons frame 2
        inner_frame_2 = LabelFrame(student_details_frame, bd=3, relief=RIDGE,
                         font=('times new roman', 12, 'bold'))
        inner_frame_2.place(x=10, y=230, width=870, height=48)

        # Take photo sample button
        take_photo_sample_button = Button(inner_frame_2, text='Take Photo Sample',width=30,font=('times new roman',13,'bold'),bg='#4CAF50',fg='white')
        take_photo_sample_button.grid(row=0,column=1,pady=5,padx=63)

        # Take photo sample button
        take_photo_sample_button = Button(inner_frame_2, text='Update Photo Sample',width=30,font=('times new roman',13,'bold'),bg='#2196F3',fg='white')
        take_photo_sample_button.grid(row=0,column=2,pady=5,padx=63)



        # ==================== Back Button ====================
        back_btn = Button(self.root,
                          text="←",                      
                          width=5,
                          height=1,
                          cursor="hand2",
                          bg="#e74c3c",
                          fg="white",
                          font=("Segoe UI Symbol", 14, "bold"),
                          command=self.back_to_details)
        back_btn.place(x=10, y=110)

    def back_to_details(self):
        self.root.destroy()
        subprocess.Popen(["python", "Main_UI.py"], shell=True)





        # Data add function

        #def add_data(self):







        # ==================== Run Main Application ====================
if __name__ == "__main__":
    root = Tk()
    obj = Student_Details(root)
    root.mainloop()