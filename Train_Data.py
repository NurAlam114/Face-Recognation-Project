#=====================Its use for LBPH ========================
# from tkinter import *
# from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter import messagebox
# import cv2
# import os
# import numpy as np
# import time
# import threading
# import re

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
#             bg_image, text="TRAIN DATASET",
#             font=('Algerian', 60, "bold"),
#             bg='white', fg='darkgreen'
#         )
#         title_lbl.place(x=-130, y=0, width=1800, height=100)

#         # ==================== Center Card / Panel ====================
#         # Shadow
#         shadow = Frame(bg_image, bg="#cfd8dc")
#         shadow.place(relx=0.5, rely=0.52, anchor=CENTER, width=740, height=360)

#         # Card
#         card = Frame(bg_image, bg="white", bd=0, highlightthickness=0)
#         card.place(relx=0.5, rely=0.5, anchor=CENTER, width=740, height=360)

#         header = Label(
#             card,
#             text="Prepare your dataset for face recognition",
#             bg="white", fg="#263238",
#             font=("Segoe UI", 18, "bold")
#         )
#         header.pack(pady=(28, 4))

#         sub = Label(
#             card,
#             text="Click the button below to start training.\nMake sure your face images are ready.",
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

#         # Hover effect
#         self.train_btn.bind("<Enter>", lambda e: self.train_btn.config(bg="#1b5e20"))
#         self.train_btn.bind("<Leave>", lambda e: self.train_btn.config(bg="#2e7d32"))

#         # Status text
#         self.status_var = StringVar(value="Status: Not trained yet.")
#         status_lbl = Label(card, textvariable=self.status_var, bg="white", fg="#37474f", font=("Segoe UI", 11))
#         status_lbl.pack(pady=(8, 6))

#         # Progress bar 
#         self.pbar = ttk.Progressbar(card, mode="indeterminate", length=420)
#         self.pbar.pack(pady=(4, 0))

#         # Dataset folder
#         #self.dataset_dir = r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\Sample image data"


#     # ==================== works train button function ====================
#     def on_train_click(self):
#         self.train_btn.config(state="disabled", text="⏳ Training...")
#         self.status_var.set("Status: Training in progress…")
#         self.pbar.start(10)

       
#         t = threading.Thread(target=self._run_training, daemon=True)
#         t.start()

#     def _run_training(self):
#         try:
#             self.train_classifier() 
#         except Exception as e:
#             self.root.after(0, lambda: self.status_var.set(f"Status: Failed — {e}"))
#             self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
#         else:
#             self.root.after(0, lambda: self.status_var.set("Status: Training completed ✅"))
#             self.root.after(0, lambda: messagebox.showinfo("Result", "Training datasets completed!!"))
#         finally:
#             self.root.after(0, self.pbar.stop)
#             self.root.after(0, lambda: self.train_btn.config(state="normal", text="⚡  Train Now"))



#     # ==================== your original style: show images while training ====================
#     def train_classifier(self):
#         data_dir = "Sample image data"
#         path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

#         faces = []
#         ids = []

#         for image in path:
#             img = Image.open(image).convert('L')  # Gray scale image
#             imageNp = np.array(img, 'uint8')
#             id = int(os.path.split(image)[1].split('.')[1])

#             faces.append(imageNp)
#             ids.append(id)

#             cv2.imshow("Training", imageNp)
#             cv2.waitKey(1) == 13
            

#         ids = np.array(ids)


#         # ============ Train the classifier and save ============
#         clf = cv2.face.LBPHFaceRecognizer_create()
#         clf.train(faces, ids)
#         clf.write("classifier.xml")
#         cv2.destroyAllWindows()
    









# =============== Its use for CNN (Adapted for Color Dataset) ===============

# =============== Full Fixed Training Code (Uses fixed_dataset with subfolders) ===============

from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os, shutil, threading
import numpy as np
import os, sys, json
import subprocess

# ====== TensorFlow / Keras ======
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

os.environ.setdefault("TF_FORCE_GPU_ALLOW_GROWTH", "true")

class TrainUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
       # self.root.wm_iconbitmap("Logo.ico")

        # Background
        bg_path = r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\UI Image\background.jpg"
        if os.path.exists(bg_path):
            img_bg = Image.open(bg_path).resize((1530, 790), Image.LANCZOS)
            self.photoimg_bg = ImageTk.PhotoImage(img_bg)
            bg_image = Label(self.root, image=self.photoimg_bg)
        else:
            bg_image = Label(self.root, bg="#f5f5f5")
        bg_image.place(x=3, y=0, width=1530, height=790)

        # Title
        title_lbl = Label(bg_image, text="TRAIN DATASET", font=('Algerian', 55, "bold"), bg='white', fg='darkgreen')
        title_lbl.place(x=-130, y=0, width=1800, height=100)

        # ===================== Beautiful Train Model Card =====================
        # Shadow for depth
        shadow = Frame(bg_image, bg="#000000")
        shadow.place(relx=0.5, rely=0.52, anchor=CENTER, width=760, height=380)
        shadow.config(highlightbackground="#000000", highlightthickness=8, highlightcolor="#000000")

        # Main Card
        card = Frame(bg_image, bg="white", bd=0, highlightbackground="#e0e0e0", highlightthickness=2)
        card.place(relx=0.5, rely=0.5, anchor=CENTER, width=760, height=380)

        # Header Bar with accent color
        header_frame = Frame(card, bg="#1b5e20", height=80)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)  # Prevent resizing

        # Header Icon + Title
        title_frame = Frame(header_frame, bg="#1b5e20")
        title_frame.pack(expand=True)

        # Icon (using unicode for simplicity - you can replace with image later)
        icon_label = Label(title_frame, text="🧠", font=("Segoe UI Emoji", 36), bg="#1b5e20", fg="white")
        icon_label.pack(side=LEFT, padx=20)

        title_label = Label(title_frame, text="Train Model", font=("Segoe UI", 22, "bold"), 
                            bg="#1b5e20", fg="white")
        title_label.pack(side=LEFT, pady=18)

        # Description
        desc = Label(card, 
                    text="Click the button below to start training the face recognition model.\nDataset folder: 'sample_image_data'\nFormat: user.ID.num.jpg",
                    bg="white", fg="#455a64", font=("Segoe UI", 13), justify=CENTER)
        desc.pack(pady=(20, 10))

        # Train Button - Big & Beautiful
        self.train_btn = Button(card, 
                                text="⚡ Train Model Now", 
                                command=self.on_train_click,
                                font=("Segoe UI Semibold", 20),
                                bg="#2e7d32", 
                                fg="white",
                                activebackground="#388e3c",
                                activeforeground="white",
                                relief=FLAT,
                                cursor="hand2",
                                padx=30,
                                pady=15)
        self.train_btn.pack(pady=(10, 20))

        # Hover effect for button (optional enhancement)
        def on_enter(e):
            self.train_btn.config(bg="#388e3c")
        def on_leave(e):
            self.train_btn.config(bg="#2e7d32")

        self.train_btn.bind("<Enter>", on_enter)
        self.train_btn.bind("<Leave>", on_leave)

        # Status Label
        self.status_var = StringVar(value="Status: Ready to train")
        status_lbl = Label(card, textvariable=self.status_var, 
                        bg="white", fg="#1b5e20", font=("Segoe UI", 12, "bold"))
        status_lbl.pack(pady=(10, 8))

        # Progress Bar - Styled
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar", 
                        background="#4caf50", 
                        troughcolor="#e8f5e8", 
                        borderwidth=0, 
                        lightcolor="#4caf50", 
                        darkcolor="#4caf50")

        self.pbar = ttk.Progressbar(card, mode="indeterminate", length=500, style="Custom.Horizontal.TProgressbar")
        self.pbar.pack(pady=(5, 20))

        # ==================== Back Button ====================
        back_btn = Button(self.root, text="←", width=3, height=1, cursor="hand2",
                            bg="#373773", fg="white",
                            font=("Segoe UI Symbol", 10, "bold"),
                            command=self.back_to_details)
        back_btn.place(x=10, y=110)
        back_btn.lift()

        def on_enter(e):
            back_btn["bg"] = "#e74c3c"
            back_btn["fg"] = "white"

        def on_leave(e):
            back_btn["bg"] = "#373773"
            back_btn["fg"] = "white"

        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)



    

        # Folder names
        self.dataset_folder = "sample_image_data"   
        self.temp_folder = "temp_training_data"

    def back_to_details(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(base_dir, "Main_UI.py")
        self.root.destroy()
        subprocess.Popen([sys.executable, main_path])



    def on_train_click(self):
        self.train_btn.config(state="disabled", text="Training...")
        self.status_var.set("Status: Processing images...")
        self.pbar.start(10)
        threading.Thread(target=self._run_training, daemon=True).start()

    def _run_training(self):
        try:
            self.train_mobilenetv2_classifier()
            self.root.after(0, lambda: self.status_var.set("Status: Training completed successfully!"))
            self.root.after(0, lambda: messagebox.showinfo("Success", "Training completed!\nModel saved as face_mobilenetv2_final.keras"))
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.status_var.set(f"Status: Error - {error_msg}"))
            self.root.after(0, lambda: messagebox.showerror("Training Failed", error_msg))
        finally:
            self.root.after(0, self.pbar.stop)
            self.root.after(0, lambda: self.train_btn.config(state="normal", text="Train Now"))

    def train_mobilenetv2_classifier(self):
        # Step 1: Auto create subfolders from filename
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)
        os.makedirs(self.temp_folder, exist_ok=True)

        files = [f for f in os.listdir(self.dataset_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not files:
            raise Exception("No images found in 'sample_image_data' folder!")

        copied = 0
        for file in files:
            if "user." not in file.lower():
                continue
            try:
                user_id = file.split(".")[1]
                id_folder = os.path.join(self.temp_folder, user_id)
                os.makedirs(id_folder, exist_ok=True)
                shutil.copy(os.path.join(self.dataset_folder, file), os.path.join(id_folder, file))
                copied += 1
            except:
                continue

        if copied == 0:
            raise Exception("No valid images! Format must be: user.221311114.1.jpg")

        self.root.after(0, lambda: self.status_var.set(f"Status: Loaded {copied} images. Training started..."))

        # Data Generator
        datagen = ImageDataGenerator(
            preprocessing_function=preprocess_input,
            validation_split=0.2,
            rotation_range=20,
            width_shift_range=0.15,
            height_shift_range=0.15,
            zoom_range=0.15,
            horizontal_flip=True
        )

        train_gen = datagen.flow_from_directory(self.temp_folder, target_size=(224,224), batch_size=32,
                                                class_mode='categorical', subset='training')
        val_gen = datagen.flow_from_directory(self.temp_folder, target_size=(224,224), batch_size=32,
                                              class_mode='categorical', subset='validation')

        # Save label map
        label_map = {v: k for k, v in train_gen.class_indices.items()}
        np.save("label_map.npy", label_map)
        print("Label Map Saved:", label_map)     
                     
        # Model
        base = MobileNetV2(include_top=False, input_shape=(224,224,3), weights='imagenet')
        base.trainable = False

        model = Sequential([
            base,
            GlobalAveragePooling2D(),
            Dropout(0.4),
            Dense(256, activation='relu'),
            Dropout(0.3),
            Dense(train_gen.num_classes, activation='softmax')
        ])

        model.compile(optimizer=Adam(0.001), loss='categorical_crossentropy', metrics=['accuracy'])

        callbacks = [
            EarlyStopping(patience=8, restore_best_weights=True, monitor='val_accuracy'),
            ReduceLROnPlateau(patience=4),
            ModelCheckpoint("best_model.keras", save_best_only=True, monitor='val_accuracy')
        ]

        model.fit(train_gen, validation_data=val_gen, epochs=30, callbacks=callbacks)

        # Fine-tune
        base.trainable = True
        for layer in base.layers[:-35]:
            layer.trainable = False
        model.compile(optimizer=Adam(1e-5), loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(train_gen, validation_data=val_gen, epochs=15, callbacks=callbacks)

        model.save("face_mobilenetv2_final.keras")




if __name__ == "__main__":
    root = Tk()
    app = TrainUI(root)
    root.mainloop()