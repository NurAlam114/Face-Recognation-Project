from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk  # pillow
import subprocess
from tkinter import messagebox
import mysql.connector
import os, sys, json


class Face_Recognation_System:
    def exit_app(self):
        self.root.destroy()

    def __init__(self, root):
        self.root = root
        self.root.geometry('1530x790+0+0')
        self.root.title("Face Recognation System")

        # ==================== Background Image ====================
        img_bg = Image.open(r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\UI Image\background.jpg")
        img_bg = img_bg.resize((1530, 790), Image.LANCZOS)
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)

        bg_image = Label(self.root, image=self.photoimg_bg)
        bg_image.place(x=3, y=0, width=1530, height=790)

        # ==================== Title Label ====================
        title_lbl = Label(
            bg_image,
            text="STUDENT MANAGEMENT SYSTEM",
            font=('times new roman', 40, "bold"),
            bg='white',
            fg='red'
        )
        title_lbl.place(x=-130, y=0, width=1800, height=100)

        #  Student details LebelFrame
        main_frame = LabelFrame(
            bg_image, bd=10, relief=RIDGE,
            text="Stdent Information",
            font=('times new roman', 12, 'bold')
        )
        main_frame.place(x=255, y=170, width=1000, height=550)

        # Search system frame
        search_frame = LabelFrame(
            bg_image, bd=5, relief=RIDGE,
            text="Search", font=('times new roman', 12, 'bold')
        )
        search_frame.place(x=300, y=210, width=900, height=70)

        # search label
        search_label = Label(
            search_frame, text='Search :',
            font=('times new roman', 14, 'bold'),
            bg="lightgray", fg='black'
        )
        search_label.grid(row=0, column=0, padx=70, pady=5, sticky=W)

        # --- Entry (Search Box with placeholder) ---
        self.search_var = StringVar()
        search_entry = Entry(
            search_frame, textvariable=self.search_var,
            font=("times new roman", 13, "bold"),
            width=20, fg="gray"
        )
        search_entry.grid(row=0, column=1, padx=10, sticky="w")

        # placeholder setup
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

        # --- Search Button ---
        def search_action():
            user_id = self.search_var.get().strip()
            if user_id == "" or user_id == "Id":
                messagebox.showwarning("Warning", "Please enter a valid Id!", parent=self.root)
                return
            # optional: টেবিলে local filter (ইচ্ছে হলে DB কুয়েরি করেও করা যায়)
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
                cursor.execute("SELECT * FROM face_recognizer WHERE Student_ID=%s", (user_id,))
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

        # Table frame
        table_frame = LabelFrame(
            bg_image, bd=5, relief=RIDGE,
            font=('times new roman', 12, 'bold')
        )
        table_frame.place(x=300, y=290, width=900, height=410)

        # Scrollbar
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "dep", "course", "year", "sem",
                     "section", "gender", "blood", "nationality",
                     "email", "phone", "address", "teacher", "photo"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # ===== Heading =====
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

        # ===== Column Widths =====
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

        # ডাটা লোড
        self.fetch_data()

        # ==================== Back Button (init-এর ভিতরে) ====================
        back_btn = Button(
            self.root,
            text="←",
            width=3, height=1, cursor="hand2",
            bg="#373773", fg="white",
            font=("Segoe UI Symbol", 11, "bold"),
            command=self.back_to_details
        )
        back_btn.place(x=10, y=110)

        # Hover
        def on_enter(e):
            back_btn["bg"] = "#e74c3c"
            back_btn["fg"] = "white"

        def on_leave(e):
            back_btn["bg"] = "#373773"
            back_btn["fg"] = "white"

        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)

    # শুধু ডাটা লোড করবে
    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="face_recognation"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM face_recognizer")
            rows = cursor.fetchall()
            if rows:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    self.student_table.insert('', END, values=row)
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}", parent=self.root)

    # Back: selected row -> temp.json -> Student_Details.py
    def back_to_details(self):
        # 1) সিলেক্টেড রো খুঁজে বের করো
        item_id = None
        sel = self.student_table.selection()
        if sel:
            item_id = sel[0]
        else:
            item_id = self.student_table.focus()

        if not item_id:
            messagebox.showwarning("Select a row", "Please select a row before going back.", parent=self.root)
            return

        values = self.student_table.item(item_id, "values")

        # 2) dict বানাও (কলাম অর্ডার অনুযায়ী)
        # ("id","name","dep","course","year","sem","section","gender",
        #  "blood","nationality","email","phone","address","teacher","photo")
        student = {
            "id": values[0],
            "name": values[1],
            "dept": values[2],
            "course": values[3],
            "year": values[4],
            "sem": values[5],
            "section": values[6],
            "gender": values[7],
            "blood": values[8],
            "nationality": values[9],
            "email": values[10],
            "phone": values[11],
            "address": values[12],
            "teacher": values[13],
            "photo": values[14],
        }

        # 3) temp.json লিখো (স্ক্রিপ্টের ফোল্ডারে)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        temp_path = os.path.join(base_dir, "temp.json")
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(student, f, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("File Error", f"Couldn't write temp.json:\n{e}", parent=self.root)
            return

        # 4) Student_Details.py চালাও একই Python দিয়ে (absolute path)
        details_path = os.path.join(base_dir, "Student_Details.py")
        if not os.path.exists(details_path):
            messagebox.showerror("Path Error", f"Student_Details.py not found at:\n{details_path}", parent=self.root)
            return

        self.root.destroy()
        subprocess.Popen([sys.executable, details_path])


# ==================== Run Main Application ====================
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognation_System(root)
    root.mainloop()
