from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import subprocess
import mysql.connector
import os, sys, json


class Face_Recognation_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1530x790+0+0')
        self.root.title("Face Recognation System")


        # Variables
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
        self.var_radio1 = StringVar()
        self.selected_from_store = False

        # ==================== Background Image ====================
        img_bg = Image.open(r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\UI Image\background.jpg")
        img_bg = img_bg.resize((1530, 790), Image.LANCZOS)
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)

        bg_image = Label(self.root, image=self.photoimg_bg)
        bg_image.place(x=3, y=0, width=1530, height=790)

        # ==================== Title Label ====================
        title_lbl = Label(
            bg_image,
            text="STUDENT RECORDS",
            font=('Algerian', 60, "bold"),
            bg='white',
            fg='#1E3A8A'
        )
        title_lbl.place(x=-130, y=0, width=1800, height=100)

        #  Student details LabelFrame
        main_frame = LabelFrame(
            bg_image, bd=10, relief=RIDGE,
            text="Student Directory",
            font=('times new roman', 12, 'bold')
        )
        main_frame.place(x=90, y=130, width=1350, height=650)

        # ==================== Search Bar ====================
        search_frame = LabelFrame(
            bg_image, bd=5, relief=RIDGE,
            text="Search", font=('times new roman', 12, 'bold')
        )
        search_frame.place(x=130, y=170, width=1300, height=70)

        search_label = Label(
            search_frame,
            text='Search :',
            font=('times new roman', 14, 'bold'),
            bg="lightgray",
            fg='black'
        )
        search_label.grid(row=0, column=0, padx=50, pady=5, sticky=W)

        self.search_var = StringVar()
        search_entry = Entry(
            search_frame, textvariable=self.search_var,
            font=("times new roman", 13, "bold"),
            width=20, fg="gray"
        )
        search_entry.grid(row=0, column=1, padx=10, sticky="w")
        search_entry.insert(0, "Id")

        def on_entry_click(event):
            if search_entry.get() == "Id":
                search_entry.delete(0, "end")
                search_entry.config(fg="black")

        def on_focusout(event):
            if search_entry.get() == "":
                search_entry.insert(0, "Id")
                search_entry.config(fg="gray")

        search_entry.bind("<FocusIn>", on_entry_click)
        search_entry.bind("<FocusOut>", on_focusout)

        def search_action():
            user_id = self.search_var.get().strip()
            if user_id == "" or user_id.lower() == "id":
                messagebox.showwarning("Warning", "Please enter a valid Id!", parent=self.root)
                return

            # Clear table first
            for i in self.student_table.get_children():
                self.student_table.delete(i)
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="face_recognation"
                )
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT
                        Student_ID,
                        Student_Name,
                        Department,
                        Course,
                        Year,
                        Semester,
                        Class_Section,
                        Gender,
                        Blood_Group,
                        Nationality,
                        Email,
                        Phone_No,
                        Address,
                        Teacher_Name,
                        Photo_Sample
                    FROM face_recognizer
                    WHERE Student_ID = %s
                """, (user_id,))
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        self.student_table.insert('', END, values=row)
                else:
                    messagebox.showinfo("Search Result", f"No result for ID: {user_id}", parent=self.root)
                conn.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}", parent=self.root)

        search_button = Button(
            search_frame, text="Search",
            font=("times new roman", 12, "bold"),
            bg="#2c3e50", fg="white",
            command=search_action
        )
        search_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        # ==================== Delete Button ====================
        delete_button = Button(
            search_frame,
            text='Delete',
            width=15,
            font=('times new roman', 13, 'bold'),
            bg="#BF2E24",
            fg='white',
            command=self.confirm_and_delete
        )
        delete_button.grid(row=0, column=3, padx=50, pady=5, sticky=W)

         # Refresh button
        Refresh_button = Button(search_frame, text='Refresh', width=15,
                                font=('times new roman', 13, 'bold'),
                                bg='#9E9E9E', fg='white', command=self.Refresh_form)
        Refresh_button.grid(row=0, column=4, pady=5, padx=50)


       
        
    



        # ==================== Table ====================
        table_frame = LabelFrame(
            bg_image, bd=5, relief=RIDGE,
            font=('times new roman', 12, 'bold')
        )
        table_frame.place(x=130, y=255, width=1300, height=500)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "dep", "course", "year", "sem",
                     "section", "gender", "blood", "nationality",
                     "email", "phone", "address", "teacher", "photo"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            selectmode="browse"  # single-select
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Headings
        self.student_table.heading("id", text="Student ID")
        self.student_table.heading("name", text="Student Name")
        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("section", text="Class Section")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("blood", text="Blood Group")
        self.student_table.heading("nationality", text="Nationality")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone No")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher Name")
        self.student_table.heading("photo", text="Photo Sample")

        self.student_table["show"] = "headings"

        # Column widths
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=120)
        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=80)
        self.student_table.column("sem", width=100)
        self.student_table.column("section", width=100)
        self.student_table.column("gender", width=80)
        self.student_table.column("blood", width=80)
        self.student_table.column("nationality", width=100)
        self.student_table.column("email", width=150)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=150)
        self.student_table.column("teacher", width=120)
        self.student_table.column("photo", width=100)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<Double-1>", lambda event: self.back_to_details())
        self.student_table.bind("<Double-1>", self.open_selected_in_details)


        # Load data initially
        self.fetch_data()

        # ==================== Back Button ====================
        back_btn = Button(
            self.root,
            text="←",
            width=3, height=1, cursor="hand2",
            bg="#373773", fg="white",
            font=("Segoe UI Symbol", 11, "bold"),
            command=self.back_to_details
        )
        back_btn.place(x=10, y=110)

        def on_enter(e):
            back_btn["bg"] = "#e74c3c"; back_btn["fg"] = "white"

        def on_leave(e):
            back_btn["bg"] = "#373773"; back_btn["fg"] = "white"

        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    # ================== Fetch all data ==================
    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="face_recognation"
            )
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    Student_ID,           -- id
                    Student_Name,         -- name
                    Department,           -- dep
                    Course,               -- course
                    Year,                 -- year
                    Semester,             -- sem
                    Class_Section,        -- section
                    Gender,               -- gender
                    Blood_Group,          -- blood
                    Nationality,          -- nationality
                    Email,                -- email
                    Phone_No,             -- phone
                    Address,              -- address
                    Teacher_Name,         -- teacher
                    Photo_Sample          -- photo
                FROM face_recognizer
            """)
            rows = cursor.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for row in rows:
                self.student_table.insert('', END, values=row)
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}", parent=self.root)

    # ================== Delete function ==================
    def confirm_and_delete(self):
        sel = self.student_table.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a row to delete.", parent=self.root)
            return

        item_id = sel[0]
        values = self.student_table.item(item_id, "values")
        if not values or len(values) < 1:
            messagebox.showerror("Error", "Could not read the selected row.", parent=self.root)
            return

        student_id = values[0]  # ensured by explicit SELECT order

        ok = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete Student ID {student_id}?",
            parent=self.root
        )
        if not ok:
            return

        try:
            deleted = self.delete_from_db(student_id)
            if not deleted:
                messagebox.showerror("Not Found", f"Student ID {student_id} not found.", parent=self.root)
                return
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete: {e}", parent=self.root)
            return

        self.fetch_data()
        messagebox.showinfo("Deleted", f"Student ID {student_id} deleted successfully.", parent=self.root)

    def delete_from_db(self, student_id):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="face_recognation"
        )
        cur = conn.cursor()
        cur.execute("DELETE FROM face_recognizer WHERE Student_ID = %s", (student_id,))
        conn.commit()
        rowcount = cur.rowcount
        cur.close()
        conn.close()
        return rowcount > 0
    


    def open_selected_in_details(self, event=None):
        item_id = self.student_table.identify_row(event.y) if event else None
        if not item_id:
            sel = self.student_table.selection()
            if not sel:
                messagebox.showwarning("No selection", "Please double-click a row.", parent=self.root)
                return
            item_id = sel[0]

        values = self.student_table.item(item_id, "values")
        if not values or len(values) < 15:
            messagebox.showerror("Error", "Could not read row values.", parent=self.root)
            return

        base_dir = os.path.dirname(os.path.abspath(__file__))
        details_path = os.path.join(base_dir, "Student_Details.py")
        if not os.path.exists(details_path):
            messagebox.showerror("Path Error", f"Student_Details.py not found:\n{details_path}", parent=self.root)
            return

        student = {
            "id":         str(values[0]),
            "name":       values[1],
            "dept":       values[2],
            "course":     values[3],
            "year":       str(values[4]),
            "sem":        values[5],
            "section":    values[6],
            "gender":     values[7],
            "blood":      values[8],
            "nationality":values[9],
            "email":      values[10],
            "phone":      str(values[11]),
            "address":    values[12],
            "teacher":    values[13],
            "photo":      values[14],
        }

        try:
            temp_path = os.path.join(base_dir, "temp.json")
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(student, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to write temp.json:\n{e}", parent=self.root)
            return

        try:
            self.root.destroy()
        finally:
            subprocess.Popen([sys.executable, details_path])


    # ================== back function ==================
    def back_to_details(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        details_path = os.path.join(base_dir, "Student_Details.py")

        if not os.path.exists(details_path):
            messagebox.showerror("Path Error", f"Student_Details.py not found at:\n{details_path}", parent=self.root)
            return

        self.root.destroy()
        subprocess.Popen([sys.executable, details_path])



        

 # Refresh method – class method হিসেবে
    def Refresh_form(self):
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
        self.var_radio1.set("")  
        self.selected_from_store = False

    




# ==================== Run Main Application ====================
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognation_System(root)
    root.mainloop()
