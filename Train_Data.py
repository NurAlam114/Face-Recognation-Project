#=====================Its use for LBPH ========================



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


    # ==================== works train button function ====================
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
            cv2.waitKey(1) == 13
            

        ids = np.array(ids)


        # ============ Train the classifier and save ============
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
    













#=============== Its use for CNN ===============

# from tkinter import *
# from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter import messagebox
# import os
# import numpy as np
# import threading
# import cv2
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# from tensorflow.keras.preprocessing.image import img_to_array, load_img
# from tensorflow.keras.optimizers import Adam
# import shutil

# class TrainUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.geometry("1530x790+0+0")
#         self.root.title("Face Recognition System")

#         # ==================== Background Image ====================
#         img_bg = Image.open(
#             r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\UI Image\background.jpg"
#         ).resize((1530, 790), Image.LANCZOS)
#         self.photoimg_bg = ImageTk.PhotoImage(img_bg)

#         bg_image = Label(self.root, image=self.photoimg_bg)
#         bg_image.place(x=3, y=0, width=1530, height=790)

#         # ==================== Title ====================
#         title_lbl = Label(
#             bg_image,
#             text="TRAIN DATASET",
#             font=('Algerian', 55, "bold"),
#             bg='white', fg='darkgreen'
#         )
#         title_lbl.place(x=-130, y=0, width=1800, height=100)

#         # ==================== Center Card / Panel ====================
#         shadow = Frame(bg_image, bg="#cfd8dc")
#         shadow.place(relx=0.5, rely=0.52, anchor=CENTER, width=740, height=360)

#         card = Frame(bg_image, bg="white", bd=0, highlightthickness=0)
#         card.place(relx=0.5, rely=0.5, anchor=CENTER, width=740, height=360)

#         header = Label(
#             card,
#             text="Train CNN Model for Face Recognition",
#             bg="white", fg="#263238",
#             font=("Segoe UI", 18, "bold")
#         )
#         header.pack(pady=(28, 4))

#         sub = Label(
#             card,
#             text="Click below to start CNN training.\nMake sure dataset folders are ready.",
#             bg="white", fg="#546e7a",
#             font=("Segoe UI", 12)
#         )
#         sub.pack(pady=(0, 18))

#         # Train Button
#         self.train_btn = Button(
#             card,
#             text="⚡  Train Now",
#             command=self.on_train_click,
#             font=("Segoe UI Semibold", 20),
#             bg="#2e7d32", fg="white",
#             activebackground="#1b5e20", activeforeground="white",
#             relief="flat", padx=28, pady=10, cursor="hand2",
#         )
#         self.train_btn.pack(pady=(0, 18))
#         self.train_btn.bind("<Enter>", lambda e: self.train_btn.config(bg="#1b5e20"))
#         self.train_btn.bind("<Leave>", lambda e: self.train_btn.config(bg="#2e7d32"))

#         # Status
#         self.status_var = StringVar(value="Status: Not trained yet.")
#         status_lbl = Label(card, textvariable=self.status_var, bg="white", fg="#37474f", font=("Segoe UI", 11))
#         status_lbl.pack(pady=(8, 6))

#         self.pbar = ttk.Progressbar(card, mode="indeterminate", length=420)
#         self.pbar.pack(pady=(4, 0))

#     # ==================== Button Action ====================
#     def on_train_click(self):
#         self.train_btn.config(state="disabled", text="⏳ Training CNN...")
#         self.status_var.set("Status: Training in progress…")
#         self.pbar.start(10)
#         t = threading.Thread(target=self._run_training, daemon=True)
#         t.start()

#     def _run_training(self):
#         try:
#             self.train_cnn_classifier()
#         except Exception as e:
#             self.root.after(0, lambda: self.status_var.set(f"Status: Failed — {e}"))
#             self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
#         else:
#             self.root.after(0, lambda: self.status_var.set("Status: CNN Training completed ✅"))
#             self.root.after(0, lambda: messagebox.showinfo("Result", "CNN model training completed successfully!"))
#         finally:
#             self.root.after(0, self.pbar.stop)
#             self.root.after(0, lambda: self.train_btn.config(state="normal", text="⚡  Train CNN Now"))



#     # ==================== CNN Model Training with Image Preview ====================
#     def train_cnn_classifier(self):
#         original_dir = "Sample image data"  
#         temp_dir = "temp_dataset"

#         if not os.path.exists(original_dir):
#             raise Exception(f"Dataset folder not found: {original_dir}")

#         # Clean temp folder if exists
#         if os.path.exists(temp_dir):
#             shutil.rmtree(temp_dir)
#         os.makedirs(temp_dir)

#         # ==================== Convert dataset automatically ====================
#         for filename in os.listdir(original_dir):
#             if not filename.lower().endswith((".jpg", ".png", ".jpeg")):
#                 continue
#             try:
#                 id = filename.split('.')[1]  # LBPH style filename: User.ID.any.jpg
#             except:
#                 raise Exception(f"Filename {filename} is not in expected format 'User.ID.x.jpg'")

#             class_dir = os.path.join(temp_dir, id)
#             if not os.path.exists(class_dir):
#                 os.makedirs(class_dir)
#             shutil.copy(os.path.join(original_dir, filename), os.path.join(class_dir, filename))

#         self.status_var.set("Status: Dataset converted automatically…")

#         # ==================== Prepare training data with image preview ====================
#         X = []
#         y = []

#         class_folders = os.listdir(temp_dir)
#         class_folders.sort()
#         label_map = {}

#         for idx, class_name in enumerate(class_folders):
#             class_path = os.path.join(temp_dir, class_name)
#             label_map[idx] = class_name
#             for img_file in os.listdir(class_path):
#                 img_path = os.path.join(class_path, img_file)
                
#                 # ==================== Show image preview ====================
#                 img_preview = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#                 cv2.imshow("Training Preview", img_preview)
#                 cv2.waitKey(100)  # 100ms delay between images

#                 # ==================== Process image for CNN ====================
#                 img = load_img(img_path, color_mode="grayscale", target_size=(100, 100))
#                 img_array = img_to_array(img) / 255.0
#                 X.append(img_array)
#                 y.append(idx)

#         cv2.destroyAllWindows()  # Close preview window

#         X = np.array(X)
#         y = np.array(y)
#         y = np.eye(len(label_map))[y]  # One-hot encoding

#         # ==================== Build CNN Model ====================
#         model = Sequential([
#             Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 1)),
#             MaxPooling2D(2, 2),
#             Conv2D(64, (3, 3), activation='relu'),
#             MaxPooling2D(2, 2),
#             Flatten(),
#             Dense(128, activation='relu'),
#             Dropout(0.5),
#             Dense(len(label_map), activation='softmax')
#         ])

#         model.compile(optimizer=Adam(learning_rate=0.001),
#                       loss='categorical_crossentropy',
#                       metrics=['accuracy'])

#         # ==================== Train Model ====================
#         model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2, verbose=1)

#         # ==================== Save Model ====================
#         model.save("face_cnn_model.h5")
#         np.save("label_map.npy", label_map)







#         self.status_var.set("Status: CNN training completed")
#         print("CNN Model and labels saved successfully.")






if __name__ == "__main__":
    root = Tk()
    app = TrainUI(root)
    root.mainloop()




