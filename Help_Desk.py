from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser,subprocess,sys,os

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Presence - Face Recognition Attendance System")
        self.root.geometry("1536x864+0+0")
        self.root.state('zoomed')
     #   self.root.wm_iconbitmap("Logo.ico")

        # ===================== Background Image =====================
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

        # Dark overlay for better text visibility
        canvas.create_rectangle(0, 0, 1536, 864, fill="#000000", stipple="gray50")

        # ===================== Main Title =====================
        canvas.create_text(
            768, 150,
            text="Help Desk",
            font=("Algerian", 85, "bold"),
            fill="#ff1744"
        )

        canvas.create_text(
            768, 230,
            text="Advanced Face Recognition Attendance System",
            font=("Helvetica", 28, "italic"),
            fill="#ffffff"
        )


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


        # ===================== Contact Card =====================
        card = Frame(canvas, bg="#1e1e1e", highlightbackground="#00e676", highlightthickness=3)
        card.place(x=768-350, y=350, width=700, height=280)

        # Message
        Label(card, text="Facing any issue or need customization?",
              font=("Helvetica", 18), fg="#cccccc", bg="#1e1e1e").place(x=350, y=50, anchor="center")

        Label(card, text="Feel free to contact me anytime",
              font=("Helvetica", 22, "bold"), fg="white", bg="#1e1e1e").place(x=350, y=95, anchor="center")

        # Contact Buttons
        def open_email():
            webbrowser.open("https://mail.google.com/mail/u/0/?view=cm&fs=1&to=221311114@vu.edu.bd&su=Smart%20Presence%20-%20Support%20Request&body=Hello%2C%0A%0AI%20am%20using%20your%20Smart%20Presence%20Face%20Recognition%20System.%0A%0AI%20need%20help%20with%3A%0A%0A%5BPlease%20write%20your%20issue%20here%5D%0A%0AThank%20you!")  

        def open_whatsapp():
            webbrowser.open("https://wa.me/+8801756448948")  

        btn_email = Button(card, text="Email Me", font=("Helvetica", 16, "bold"),
                           bg="#4285f4", fg="white", activebackground="#3367d6",
                           cursor="hand2", bd=0, padx=30, pady=12, command=open_email)
        btn_email.place(x=140, y=170)

        btn_wp = Button(card, text="WhatsApp", font=("Helvetica", 16, "bold"),
                        bg="#25d366", fg="white", activebackground="#128c7e",
                        cursor="hand2", bd=0, padx=30, pady=12, command=open_whatsapp)
        btn_wp.place(x=390, y=170)

        # ===================== Footer =====================
        canvas.create_text(
            768, 820,
            text="© 2025 Smart Presence • All Rights Reserved",
            font=("Helvetica", 12),
            fill="#666666"
        )
    def back_to_details(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(base_dir, "Main_UI.py")
        self.root.destroy()
        subprocess.Popen([sys.executable, main_path])


# ===================== Run the Application =====================
if __name__ == "__main__":
    root = Tk()
    app = Face_Recognition_System(root)
    root.mainloop()