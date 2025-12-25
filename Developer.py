from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser
import os, subprocess,sys

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Presence - Face Recognition Attendance System")
        self.root.geometry("1536x864+0+0")
        self.root.state('zoomed')
        #self.root.wm_iconbitmap("Logo.ico")


        # ===================== Background =====================
        try:
            bg = Image.open(r"UI Image/background.jpg")
            bg = bg.resize((1536, 864), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(bg)
        except:
            self.bg_image = None

        canvas = Canvas(self.root, highlightthickness=0)
        canvas.pack(fill=BOTH, expand=True)

        if self.bg_image:
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        canvas.create_rectangle(0, 0, 1536, 864, fill="#000000", stipple="gray50")

        # ===================== Title =====================
        canvas.create_text(768, 70, text="DEVELOPERS", font=("Algerian", 70, "bold"), fill="#ff1744")
        canvas.create_text(768, 180, text="Advanced Face Recognition Attendance System",
                           font=("Helvetica", 25, "italic"), fill="#ffffff")
        
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

        # ===================== Developers Card =====================
        card = Frame(self.root, bg="#0a1e3d", highlightbackground="#00e676", highlightthickness=5)
        card.place(relx=0.5, rely=0.55, anchor=CENTER, width=950, height=640)

        Label(card, text="Meet the Developers", font=("Arial", 25, "bold"), fg="#00e676", bg="#0a1e3d").pack(pady=25)
        Label(card, text="Feel free to reach out for help or collaboration", font=("Arial", 15), fg="#bbbbbb", bg="#0a1e3d").pack(pady=8)

        # ===================== 3 Developers (Name + Email + GitHub) =====================
        developers = [
            {
                "name": "MD. NUR ALAM",
                "email": "221311114@vu.edu.bd",
                "github": "https://github.com/NurAlam114"
            },
            {
                "name": "ABDULLAH AL NOMAN",
                "email": "221311094@vu.edu.bd",
                "github": "https://github.com/aalnoman24"
            },
            {
                "name": "MARUFA YEASMIN MOU",
                "email": "221311088@vu.edu.bd",
                "github": "https://github.com/mou-cse"
            }
        ]

        for dev in developers:
            box = Frame(card, bg="#112240", bd=2, relief="groove")
            box.pack(pady=15, padx=50, fill=X)

            Label(box, text=dev["name"], font=("Helvetica", 15, "bold"), fg="#00e676", bg="#112240").pack(pady=8)

            # Email Link
            email_link = Label(box, text=dev["email"], font=("Helvetica", 13), fg="#64b5f6", bg="#112240", cursor="hand2")
            email_link.pack(pady=4)
            email_link.bind("<Button-1>", lambda e, mail=dev["email"]: webbrowser.open(f"mailto:{mail}"))

            # GitHub Link
            gh_link = Label(box, text="GitHub Profile →", font=("Helvetica", 13), fg="#ff8a65", bg="#112240", cursor="hand2")
            gh_link.pack(pady=6)
            gh_link.bind("<Button-1>", lambda e, url=dev["github"]: webbrowser.open(url))

        # ===================== Close Button =====================
        Button(card, text="Close Application", font=("Arial", 18, "bold"), bg="#d32f2f", fg="white",
               width=20, height=2, command=self.root.destroy, cursor="hand2").pack(pady=40)
        
    def back_to_details(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(base_dir, "Main_UI.py")
        self.root.destroy()
        subprocess.Popen([sys.executable, main_path])




# ==================== Run Main Application ====================
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()