# Attendance.py
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime


# ==================== Auto Mark Attendance ====================
def mark_attendance(student_id, name, dept, batch, section, course, status="Present"):
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M:%S")
    filename = f"attendance_{dept}_{batch}_{section}_{course}.csv"

    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Date", "Time", "Status", "Marks"])

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = list(csv.reader(f))
            for row in reader[1:]:
                if len(row) >= 3 and row[0] == str(student_id) and row[2] == today:
                    return
    except:
        pass

    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([student_id, name, today, now, status, ""])


# ==================== Main Class ====================
class Face_Recognation_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1530x790+0+0')
        self.root.title("Face Recognation System")

        # ==================== Background ====================
        img_bg = Image.open(r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\UI Image\background.jpg")
        img_bg = img_bg.resize((1530, 790), Image.LANCZOS)
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)

        bg_image = Label(self.root, image=self.photoimg_bg)
        bg_image.place(x=3, y=0, width=1530, height=790)

        # ==================== Title ====================
        title_lbl = Label(bg_image, text="ATTENDANCE PORTAL",
                          font=('Algerian', 50, "bold"), bg='white', fg='red')
        title_lbl.place(x=-130, y=0, width=1800, height=100)

        # ==================== Main Frame ====================
        main_frame = Frame(bg_image, bd=2, bg="white")
        main_frame.place(x=450, y=200, width=650, height=450)

        # Variables
        self.var_dep = StringVar()
        self.var_batch = StringVar()
        self.var_section = StringVar()
        self.var_course = StringVar()

        # Course List
        self.course_list = ["OS", "DBMS", "OOP", "DSA", "Networking", "AI"]

        # Department
        Label(main_frame, text="Select Department:", font=("times new roman", 20, "bold"), bg="white").place(x=100, y=50)
        self.combo_dep = ttk.Combobox(main_frame, textvariable=self.var_dep, state="readonly",
                                      font=("times new roman", 15), width=22)
        self.combo_dep["values"] = ("Select Department", "CSE", "EEE", "BBA")
        self.combo_dep.current(0)
        self.combo_dep.place(x=300, y=55)
        self.combo_dep.bind("<<ComboboxSelected>>", self.load_batches)

        # Batch
        Label(main_frame, text="Select Batch:", font=("times new roman", 20, "bold"), bg="white").place(x=100, y=120)
        self.combo_batch = ttk.Combobox(main_frame, textvariable=self.var_batch, state="disabled",
                                       font=("times new roman", 15), width=22)
        self.combo_batch.place(x=300, y=125)
        self.combo_batch.bind("<<ComboboxSelected>>", self.load_sections)

        # Section
        Label(main_frame, text="Select Section:", font=("times new roman", 20, "bold"), bg="white").place(x=100, y=190)
        self.combo_section = ttk.Combobox(main_frame, textvariable=self.var_section, state="disabled",
                                         font=("times new roman", 15), width=22)
        self.combo_section.place(x=300, y=195)
        self.combo_section.bind("<<ComboboxSelected>>", self.enable_course)

        # Course
        Label(main_frame, text="Select Course:", font=("times new roman", 20, "bold"), bg="white").place(x=100, y=260)
        self.combo_course = ttk.Combobox(main_frame, textvariable=self.var_course, state="disabled",
                                        font=("times new roman", 15), width=22)
        self.combo_course["values"] = self.course_list
        self.combo_course.place(x=300, y=265)

        # Button
        Button(main_frame, text="Show Attendance", command=self.open_attendance,
               font=("times new roman", 16, "bold"), bg="green", fg="white", width=15).place(x=220, y=340)

    # ==================== Load Dropdowns ====================
    def load_batches(self, event):
        dep = self.var_dep.get()
        if dep == "CSE":
            batches = ("28", "29")
        elif dep == "EEE":
            batches = ("30", "31")
        elif dep == "BBA":
            batches = ("12", "13")
        else:
            batches = ()

        self.combo_batch.config(state="readonly")
        self.combo_batch["values"] = batches
        if batches:
            self.combo_batch.current(0)
        self.combo_section.config(state="disabled")
        self.combo_course.config(state="disabled")

    def load_sections(self, event):
        self.combo_section.config(state="readonly")
        self.combo_section["values"] = ("A", "B", "C")
        self.combo_section.current(0)
        self.combo_course.config(state="disabled")

    def enable_course(self, event):
        self.combo_course.config(state="readonly")
        if self.course_list:
            self.combo_course.current(0)

    # ==================== Open Attendance Window ====================
    def open_attendance(self):
        dep = self.var_dep.get()
        batch = self.var_batch.get()
        section = self.var_section.get()
        course = self.var_course.get()

        # === ফিক্স: "Select Batch" চেক ===
        if dep == "Select Department" or not batch or section in ("A", "B", "C") == False or not course:
            messagebox.showerror("Error", "Please select Department, Batch, Section & Course")
            return

        filename = f"attendance_{dep}_{batch}_{section}_{course}.csv"

        if not os.path.exists(filename):
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Date", "Time", "Status", "Marks"])

        # Fullscreen
        self.new_win = Toplevel(self.root)
        self.new_win.title(f"{dep} - Batch {batch} - Section {section} - {course}")
        self.new_win.state("zoomed")

        Label(self.new_win, text="Search:", font=("times new roman", 15)).place(x=20, y=20)
        self.search_var = StringVar()
        Entry(self.new_win, textvariable=self.search_var, width=25, font=("times new roman", 15)).place(x=100, y=20)
        
        Button(self.new_win, text="Search", command=lambda: self.filter_table(filename),
               bg="blue", fg="white", width=7, font=("times new roman", 12, "bold")).place(x=350, y=18)

        Button(self.new_win, text="Show All", command=lambda: self.load_table(filename),
               bg="black", fg="white", width=9, font=("times new roman", 12, "bold")).place(x=430, y=18)

        Label(self.new_win, text="Date:", font=("times new roman", 15)).place(x=530, y=20)
        self.date_var = StringVar()
        Entry(self.new_win, textvariable=self.date_var, width=12, font=("times new roman", 15)).place(x=590, y=20)

        Button(self.new_win, text="Filter", command=lambda: self.filter_by_date(filename),
               bg="purple", fg="white", width=7, font=("times new roman", 12, "bold")).place(x=720, y=18)

        Button(self.new_win, text="Export Excel", command=lambda: self.export_excel(filename),
               bg="green", fg="white", width=10, font=("times new roman", 12, "bold")).place(x=820, y=18)

        Button(self.new_win, text="Export PDF", command=lambda: self.export_pdf(filename),
               bg="red", fg="white", width=10, font=("times new roman", 12, "bold")).place(x=940, y=18)

        # Table
        table_frame = Frame(self.new_win, bd=2, relief=RIDGE)
        table_frame.place(x=10, y=60, relwidth=0.98, relheight=0.6)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.att_table = ttk.Treeview(table_frame, columns=("id", "name", "date", "time", "status", "marks"),
                                      xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.att_table.xview)
        scroll_y.config(command=self.att_table.yview)

        for col in ("id", "name", "date", "time", "status", "marks"):
            self.att_table.heading(col, text=col.upper())
            self.att_table.column(col, width=130)

        self.att_table["show"] = "headings"
        self.att_table.pack(fill=BOTH, expand=1)

        self.total_present_var = StringVar()
        self.total_absent_var = StringVar()
        self.total_all_var = StringVar()

        Label(self.new_win, textvariable=self.total_present_var, font=("times new roman", 14)).place(x=20, y=680)
        Label(self.new_win, textvariable=self.total_absent_var, font=("times new roman", 14)).place(x=200, y=680)
        Label(self.new_win, textvariable=self.total_all_var, font=("times new roman", 14)).place(x=380, y=680)

        self.canvas = None
        self.load_table(filename)

    # ==================== Table Functions ====================
    def load_table(self, filename):
        if not os.path.exists(filename):
            return
        df = pd.read_csv(filename)
        if df.empty:
            return

        df['ID'] = df['ID'].astype(str)
        total_count = df.groupby('ID')['Status'].count()
        present_count = df[df['Status'].str.lower() == 'present'].groupby('ID')['Status'].count()

        df['Marks'] = df.apply(
            lambda row: round((present_count.get(row['ID'], 0) / total_count.get(row['ID'], 1)) * 10, 2),
            axis=1
        )
        df.to_csv(filename, index=False)

        for i in self.att_table.get_children():
            self.att_table.delete(i)

        for _, r in df.iterrows():
            self.att_table.insert("", END, values=(r['ID'], r['Name'], r['Date'], r['Time'], r['Status'], r['Marks']))

        present = len(df[df['Status'].str.lower() == "present"])
        absent = len(df[df['Status'].str.lower() == "absent"])
        total = len(df)

        self.total_present_var.set(f"Present: {present}")
        self.total_absent_var.set(f"Absent: {absent}")
        self.total_all_var.set(f"Total: {total}")
        self.update_pie_chart(present, absent)

    def filter_table(self, filename):
        key = self.search_var.get().lower()
        df = pd.read_csv(filename)
        df = df[df.apply(lambda row: key in str(row).lower(), axis=1)]
        for i in self.att_table.get_children():
            self.att_table.delete(i)
        for _, r in df.iterrows():
            self.att_table.insert("", END, values=(r['ID'], r['Name'], r['Date'], r['Time'], r['Status'], r['Marks']))

    def filter_by_date(self, filename):
        date = self.date_var.get()
        df = pd.read_csv(filename)
        df = df[df['Date'] == date]
        for i in self.att_table.get_children():
            self.att_table.delete(i)
        for _, r in df.iterrows():
            self.att_table.insert("", END, values=(r['ID'], r['Name'], r['Date'], r['Time'], r['Status'], r['Marks']))

    # ==================== Pie Chart ====================
    def update_pie_chart(self, present, absent):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        fig = plt.Figure(figsize=(2.5, 2.5))
        ax = fig.add_subplot(111)
        wedges, texts, autotexts = ax.pie([present, absent], labels=["Present", "Absent"], autopct="%0.1f%%", startangle=90, wedgeprops={'edgecolor':'black', 'linewidth':1.5})
        for text in texts + autotexts:
            text.set_fontsize(10)
            text.set_fontweight('bold')
        ax.set_title("Attendance Overview", fontsize=12, fontweight='bold')
        self.canvas = FigureCanvasTkAgg(fig, master=self.new_win)
        self.canvas.get_tk_widget().place(x=1000, y=550)

    # ==================== Export ====================
    def export_excel(self, filename):
        df = pd.read_csv(filename)
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if save_path:
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Success", "Exported to Excel successfully")

    def export_pdf(self, filename):
        df = pd.read_csv(filename)
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if save_path:
            df.to_html("temp.html", index=False)
            os.system(f"wkhtmltopdf temp.html {save_path}")
            os.remove("temp.html")
            messagebox.showinfo("Success", "Exported to PDF successfully")


# ==================== Run App ====================
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognation_System(root)
    root.mainloop()