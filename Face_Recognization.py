from tkinter import *
from PIL import Image, ImageTk
import cv2
import sqlite3
import threading
import os
import numpy as np

class FaceDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Detector")

        self.stop_detection = False  # Stop Flag

        # ==================== Background UI ====================
        bg_img = Image.open(
            r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\UI Image\background.jpg"
        ).resize((1530, 790))
        self.photo_bg = ImageTk.PhotoImage(bg_img)
        bg_lbl = Label(self.root, image=self.photo_bg)
        bg_lbl.place(x=0, y=0, width=1530, height=790)

        title_lbl = Label(bg_lbl, text="FACE DETECTOR",
                          font=("Algerian", 60, "bold"),
                          bg="white", fg="red", relief=RIDGE, bd=5)
        title_lbl.place(x=0, y=0, width=1530, height=100)

        main_frame = Frame(bg_lbl, bg="white", bd=4, relief=RIDGE)
        main_frame.place(x=380, y=150, width=750, height=520)

        sub_lbl = Label(main_frame, text="Face Detection Control Panel",
                        font=("times new roman", 28, "bold"),
                        bg="navy", fg="white")
        sub_lbl.place(x=0, y=0, width=750, height=60)

        img_student = Image.open(
            r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\UI Image\detected_image.png"
        ).resize((746, 450), Image.LANCZOS)
        self.photoimg_student = ImageTk.PhotoImage(img_student)
        self.preview_lbl = Label(main_frame, image=self.photoimg_student, bd=2, relief=RIDGE)
        self.preview_lbl.place(x=2, y=60, width=746, height=450)

        # ==================== Buttons ====================
        start_btn = Button(main_frame, text="▶ Start Detection",
                           font=("times new roman", 18, "bold"),
                           bg="#28a745", fg="white",
                           command=self.start_detection_thread)
        start_btn.place(x=120, y=410, width=220, height=50)

        stop_btn = Button(main_frame, text="⏹ Stop Detection",
                          font=("times new roman", 18, "bold"),
                          bg="#dc3545", fg="white",
                          command=self.stop_detection_func)
        stop_btn.place(x=400, y=410, width=220, height=50)

    # ================== Threading ==================
    def start_detection_thread(self):
        self.stop_detection = False
        t = threading.Thread(target=self.face_recog)
        t.daemon = True
        t.start()

    def stop_detection_func(self):
        self.stop_detection = True

    # ================== Face Recognition ==================
    def face_recog(self):
        base_path = r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation"

        modelFile = os.path.join(base_path, "res10_300x300_ssd_iter_140000.caffemodel")
        configFile = os.path.join(base_path, "deploy.prototxt")
        classifierFile = os.path.join(base_path, "classifier.xml")
        dbFile = os.path.join(base_path, "face_recognation.db")

        # Load DNN Face Detector
        net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

        # Load trained recognizer
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read(classifierFile)

        # Load database info
        conn = sqlite3.connect(dbFile)
        cursor = conn.cursor()
        cursor.execute("SELECT Student_ID, Student_Name, Department FROM face_recognizer")
        data_rows = cursor.fetchall()
        conn.close()
        db_dict = {str(row[0]): {"name": row[1], "dept": row[2]} for row in data_rows}

        # Initialize camera
        video_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # Helper function: check overlap
        def overlap(b1, b2):
            xa = max(b1[0], b2[0])
            ya = max(b1[1], b2[1])
            xb = min(b1[2], b2[2])
            yb = min(b1[3], b2[3])
            inter_area = max(0, xb - xa) * max(0, yb - ya)
            box1_area = (b1[2] - b1[0]) * (b1[3] - b1[1])
            box2_area = (b2[2] - b2[0]) * (b2[3] - b2[1])
            union = box1_area + box2_area - inter_area
            return inter_area / union > 0.4 if union > 0 else False

        # Start face recognition loop
        while True:
            if self.stop_detection:
                break

            ret, img = video_cap.read()
            if not ret:
                break

            h, w = img.shape[:2]

            blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
                                        (300, 300), (104.0, 177.0, 123.0))
            net.setInput(blob)
            detections = net.forward()

            processed_boxes = []

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence < 0.45:
                    continue

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")

                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w - 1, x2), min(h - 1, y2)

                if any(overlap((x1, y1, x2, y2), pb) for pb in processed_boxes):
                    continue

                roi_gray = cv2.cvtColor(img[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)

                try:
                    id, predict = clf.predict(roi_gray)
                    acc = int((100 * (1 - predict / 300)))
                except:
                    continue

                info = db_dict.get(str(id), {"name": "Unknown", "dept": ""})
                name, dept = info["name"], info["dept"]

                if acc > 75:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(img, f"ID: {id}", (x1, y1 - 55),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(img, f"Name: {name}", (x1, y1 - 30),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(img, f"Department: {dept}", (x1, y1 - 5),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
                else:
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(img, "Unknown", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

                processed_boxes.append((x1, y1, x2, y2))

            cv2.imshow("Face Recognition (DNN)", img)

            if cv2.waitKey(1) == 13:
                break

        video_cap.release()
        cv2.destroyAllWindows()



















    #     # ================== CNN ভিত্তিক Face Recognition ==================
    # def face_recog(self):
    #     from tensorflow.keras.models import load_model
    #     from tensorflow.keras.preprocessing.image import img_to_array
    #     import numpy as np

    #     model = load_model("face_cnn_model.h5")
    #     label_map = np.load("label_map.npy", allow_pickle=True).item()
    #     label_map = {int(k): str(v) for k, v in label_map.items()}

    #     faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    #     video_cap = cv2.VideoCapture(0)

    #     while True:
    #         if self.stop_detection:  # ✅ যদি stop চাপা হয়
    #             break

    #         ret, frame = video_cap.read()
    #         if not ret:
    #             break

    #         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #         faces = faceCascade.detectMultiScale(gray, 1.3, 5)

    #         for (x, y, w, h) in faces:
    #             face_roi = gray[y:y + h, x:x + w]
    #             face_resized = cv2.resize(face_roi, (100, 100))
    #             face_array = img_to_array(face_resized) / 255.0
    #             face_array = np.expand_dims(face_array, axis=0)
    #             face_array = np.expand_dims(face_array, axis=-1)

    #             preds = model.predict(face_array)
    #             class_id = np.argmax(preds)
    #             confidence = preds[0][class_id] * 100
    #             id_str = label_map[class_id]

    #             conn = sqlite3.connect("face_recognation.db")
    #             cursor = conn.cursor()
    #             cursor.execute("SELECT Student_Name FROM face_recognizer WHERE Student_ID = ?", (str(id_str),))
    #             n = cursor.fetchone()
    #             n = n[0] if n else "Unknown"
    #             conn.close()

    #             color = (0, 255, 0) if confidence > 80 else (0, 0, 255)
    #             label_text = f"{n} ({confidence:.1f}%)" if confidence > 80 else "Unknown Face"
    #             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    #             cv2.putText(frame, label_text, (x, y - 10),
    #                         cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    #         cv2.imshow("CNN Face Recognition", frame)
    #         if cv2.waitKey(1) == 13:  # Enter চাপলে বন্ধ হবে
    #             break

    #     video_cap.release()
    #     cv2.destroyAllWindows()





if __name__ == "__main__":
    root = Tk()
    app = FaceDetectorGUI(root)
    root.mainloop()
