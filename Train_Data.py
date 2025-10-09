from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np
import time
import threading
import re

class TrainUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # ==================== Background Image ====================
        img_bg = Image.open(
            r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\UI Image\background.jpg"
        ).resize((1530, 790), Image.LANCZOS)
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)

        bg_image = Label(self.root, image=self.photoimg_bg)
        bg_image.place(x=3, y=0, width=1530, height=790)

        # ==================== Title ====================
        title_lbl = Label(
            bg_image, text="TRAIN DATASET",
            font=('Algerian', 60, "bold"),
            bg='white', fg='darkgreen'
        )
        title_lbl.place(x=-130, y=0, width=1800, height=100)

        # ==================== Center Card / Panel ====================
        # Shadow
        shadow = Frame(bg_image, bg="#cfd8dc")
        shadow.place(relx=0.5, rely=0.52, anchor=CENTER, width=740, height=360)

        # Card
        card = Frame(bg_image, bg="white", bd=0, highlightthickness=0)
        card.place(relx=0.5, rely=0.5, anchor=CENTER, width=740, height=360)

        header = Label(
            card,
            text="Prepare your dataset for face recognition",
            bg="white", fg="#263238",
            font=("Segoe UI", 18, "bold")
        )
        header.pack(pady=(28, 4))

        sub = Label(
            card,
            text="Click the button below to start training.\nMake sure your face images are ready.",
            bg="white", fg="#546e7a",
            font=("Segoe UI", 12)
        )
        sub.pack(pady=(0, 18))

        # Train Button 
        self.train_btn = Button(
            card,
            text="⚡  Train Now",
            command=self.on_train_click,  
            font=("Segoe UI Semibold", 20),
            bg="#2e7d32", fg="white",
            activebackground="#1b5e20", activeforeground="white",
            relief="flat", padx=28, pady=10, cursor="hand2",
        )
        self.train_btn.pack(pady=(0, 18))

        # Hover effect
        self.train_btn.bind("<Enter>", lambda e: self.train_btn.config(bg="#1b5e20"))
        self.train_btn.bind("<Leave>", lambda e: self.train_btn.config(bg="#2e7d32"))

        # Status text
        self.status_var = StringVar(value="Status: Not trained yet.")
        status_lbl = Label(card, textvariable=self.status_var, bg="white", fg="#37474f", font=("Segoe UI", 11))
        status_lbl.pack(pady=(8, 6))

        # Progress bar 
        self.pbar = ttk.Progressbar(card, mode="indeterminate", length=420)
        self.pbar.pack(pady=(4, 0))

        # Dataset folder
        #self.dataset_dir = r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\Sample image data"


    # ==================== works train button ====================
    def on_train_click(self):
        self.train_btn.config(state="disabled", text="⏳ Training...")
        self.status_var.set("Status: Training in progress…")
        self.pbar.start(10)

       
        t = threading.Thread(target=self._run_training, daemon=True)
        t.start()

    def _run_training(self):
        try:
            self.train_classifier() 
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Status: Failed — {e}"))
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        else:
            self.root.after(0, lambda: self.status_var.set("Status: Training completed ✅"))
            self.root.after(0, lambda: messagebox.showinfo("Result", "Training datasets completed!!"))
        finally:
            self.root.after(0, self.pbar.stop)
            self.root.after(0, lambda: self.train_btn.config(state="normal", text="⚡  Train Now"))



    # ==================== your original style: show images while training ====================
    def train_classifier(self):
        data_dir = "Sample image data"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L')  # Gray scale image
            imageNp = np.array(img, 'uint8')
            id = int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)

            cv2.imshow("Training", imageNp)
            cv2.waitKey(1) == 13  # Press Enter to exit training preview

        ids = np.array(ids)


        # ============ Train the classifier and save ============
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        




    
if __name__ == "__main__":
    root = Tk()
    app = TrainUI(root)
    root.mainloop()
