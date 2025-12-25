# Face_Detector.py
import os
import subprocess,sys
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import sqlite3
import threading
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# ============== Import from Attendance.py ==============
from Attendance import mark_attendance
# ========================================================


class FaceDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Detector")
        self.stop_detection = False
       # self.root.wm_iconbitmap("Logo.ico")

        # ============== NEW: Track Present Students ==============
        self.present_students = set()  
        # ========================================================

        # ==================== Background UI ====================
        bg_path = r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\UI Image\background.jpg"
        if not os.path.exists(bg_path):
            raise FileNotFoundError(f"Background image not found at {bg_path}")

        bg_img = Image.open(bg_path).resize((1530, 790))
        self.photo_bg = ImageTk.PhotoImage(bg_img)
        bg_lbl = Label(self.root, image=self.photo_bg)
        bg_lbl.place(x=0, y=0, width=1530, height=790)

        title_lbl = Label(bg_lbl, text="FACE DETECTOR", font=("Algerian", 60, "bold"), bg="white", fg="red", relief=RIDGE, bd=5)
        title_lbl.place(x=0, y=0, width=1530, height=100)

        main_frame = Frame(bg_lbl, bg="white", bd=4, relief=RIDGE)
        main_frame.place(x=380, y=150, width=750, height=520)

        sub_lbl = Label(main_frame, text="Face Detection Control Panel", font=("times new roman", 28, "bold"), bg="navy", fg="white")
        sub_lbl.place(x=0, y=0, width=750, height=60)

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

        # ==================== Preview Image ====================
        img_path = r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\UI Image\detected_image.png"
        if os.path.exists(img_path):
            img_student = Image.open(img_path).resize((746, 450), Image.LANCZOS)
            self.photoimg_student = ImageTk.PhotoImage(img_student)
        else:
            self.photoimg_student = None

        self.preview_lbl = Label(main_frame, image=self.photoimg_student, bd=2, relief=RIDGE)
        self.preview_lbl.place(x=2, y=60, width=746, height=450)

        # ==================== Dropdown Data ====================
        self.department_data = {
            "CSE": {
                "29": ["A", "B", "C"],
                "28": ["A", "B", "C"]
            },
            "EEE": {
                "21": ["A"],
                "22": ["A", "B"]
            },
            "BBA": {
                "12": ["Morning", "Evening"]
            }
        }

        # Course List
        self.course_list = ["OS", "DBMS", "OOP", "DSA", "Networking", "AI"]

        # Variables
        self.var_department = StringVar()
        self.var_batch = StringVar()
        self.var_section = StringVar()
        self.var_course = StringVar()

        # Department
        Label(main_frame, text="Department:", font=("times new roman", 16, "bold"), bg="skyblue").place(x=160, y=330)
        self.combo_dep = ttk.Combobox(main_frame, textvariable=self.var_department, state="readonly", font=("times new roman", 14))
        self.combo_dep["values"] = list(self.department_data.keys())
        self.combo_dep.place(x=350, y=330, width=250)
        self.combo_dep.bind("<<ComboboxSelected>>", self.load_batches)

        # Batch
        Label(main_frame, text="Batch:", font=("times new roman", 16, "bold"), bg="skyblue").place(x=160, y=370)
        self.combo_batch = ttk.Combobox(main_frame, textvariable=self.var_batch, state="disabled", font=("times new roman", 14))
        self.combo_batch.place(x=350, y=370, width=250)
        self.combo_batch.bind("<<ComboboxSelected>>", self.load_sections)

        # Section
        Label(main_frame, text="Class_Section:", font=("times new roman", 16, "bold"), bg="skyblue").place(x=160, y=410)
        self.combo_section = ttk.Combobox(main_frame, textvariable=self.var_section, state="disabled", font=("times new roman", 14))
        self.combo_section.place(x=350, y=410, width=250)
        self.combo_section.bind("<<ComboboxSelected>>", self.enable_course)

        # Course
        Label(main_frame, text="Course:", font=("times new roman", 16, "bold"), bg="skyblue").place(x=160, y=450)
        self.combo_course = ttk.Combobox(main_frame, textvariable=self.var_course, state="disabled", font=("times new roman", 14))
        self.combo_course["values"] = self.course_list
        self.combo_course.place(x=350, y=450, width=250)

        # Buttons
        self.start_btn = Button(main_frame, text="Start Detection", font=("times new roman", 18, "bold"), bg="#28a745", fg="white",
                                command=self.start_detection_thread, state=DISABLED)
        self.start_btn.place(x=80, y=200, width=220, height=50)

        self.stop_btn = Button(main_frame, text="Stop Detection", font=("times new roman", 18, "bold"), bg="#dc3545", fg="white",
                               command=self.stop_and_mark_absent, state=DISABLED)
        self.stop_btn.place(x=440, y=200, width=220, height=50)

        # Trace
        self.var_department.trace("w", self.check_fields_filled)
        self.var_batch.trace("w", self.check_fields_filled)
        self.var_section.trace("w", self.check_fields_filled)
        self.var_course.trace("w", self.check_fields_filled)

    def back_to_details(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(base_dir, "Main_UI.py")
        self.root.destroy()
        subprocess.Popen([sys.executable, main_path])

    # ==================== Dropdown Logic ====================
    def load_batches(self, event):
        selected_dep = self.var_department.get()
        batches = list(self.department_data[selected_dep].keys())
        self.combo_batch.config(state="readonly")
        self.combo_batch["values"] = batches
        self.combo_batch.set("")
        self.combo_section.set("")
        self.combo_section.config(state="disabled")
        self.combo_course.set("")
        self.combo_course.config(state="disabled")

    def load_sections(self, event):
        selected_dep = self.var_department.get()
        selected_batch = self.var_batch.get()
        sections = self.department_data[selected_dep][selected_batch]
        self.combo_section.config(state="readonly")
        self.combo_section["values"] = sections
        self.combo_section.set("")
        self.combo_course.set("")
        self.combo_course.config(state="disabled")

    def enable_course(self, event):
        self.combo_course.config(state="readonly")
        self.combo_course.set(self.course_list[0] if self.course_list else "")

    def check_fields_filled(self, *args):
        if (self.var_department.get() and self.var_batch.get() and 
            self.var_section.get() and self.var_course.get()):
            self.start_btn.config(state=NORMAL)
        else:
            self.start_btn.config(state=DISABLED)

    # ==================== Threading ====================
    def start_detection_thread(self):
        self.stop_detection = False
        self.present_students = set() 

        self.stop_btn.config(state=NORMAL)
        self.start_btn.config(state=DISABLED)

        t = threading.Thread(target=self.face_recog, daemon=True)
        t.start()

    # ==================== STOP + MARK ABSENT ====================
    def stop_and_mark_absent(self):
        self.stop_detection = True

        self.mark_remaining_as_absent()

        
        self.stop_btn.config(state=DISABLED)
        self.start_btn.config(state=NORMAL)
        messagebox.showinfo("Session Ended", "Detection stopped. Absent students marked.")

    # ==================== Mark Remaining as Absent ====================
    def mark_remaining_as_absent(self):
        dept = self.var_department.get()
        batch_full = self.var_batch.get()
        batch = batch_full.strip()
        section = self.var_section.get()
        course = self.var_course.get()

        if not dept or not batch or not section or not course:
            return

        try:
            conn = sqlite3.connect("face_recognation.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Student_ID, Student_Name 
                FROM face_recognizer 
                WHERE Department = ? AND Batch = ? AND Class_Section = ?
            """, (dept, batch, section))
            all_students = cursor.fetchall()
            conn.close()
        except Exception as e:
            messagebox.showerror("DB Error", f"Failed to fetch students: {e}")
            return

        absent_count = 0
        for sid, name in all_students:
            if sid not in self.present_students:
                mark_attendance(
                    student_id=sid,
                    name=name,
                    dept=dept,
                    batch=batch,
                    section=section,
                    course=course,
                    status="Absent"
                )
                absent_count += 1

        print(f"{absent_count} students marked as Absent.")

    # ==================== Face Recognition ====================
    # Face Recognition
    def face_recog(self):
        try:
            model = load_model("face_mobilenetv2_final.keras")
            label_map = np.load("label_map.npy", allow_pickle=True).item()
            print("LABEL MAP = ", label_map)  
            
            from mtcnn import MTCNN
            detector = MTCNN()
            video_cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
            if not video_cap.isOpened():
                raise Exception("Camera not opening!")
            from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

            dept_gui = self.var_department.get()
            batch_gui = self.var_batch.get().strip()
            section_gui = self.var_section.get()
            course_gui = self.var_course.get()

            while True:
                if getattr(self, 'stop_detection', False):
                    break

                ret, frame = video_cap.read()
                if not ret: break
                faces = detector.detect_faces(frame)

                for face in faces:
                    x, y, w, h = face['box']
                    x, y = max(0, x), max(0, y)
                    margin_w = int(0.3 * w)
                    margin_h = int(0.3 * h)
                    x1 = max(0, x - margin_w)
                    y1 = max(0, y - margin_h)
                    x2 = min(frame.shape[1], x + w + margin_w)
                    y2 = min(frame.shape[0], y + h + margin_h)
                    face_roi = frame[y1:y2, x1:x2]

                    face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
                    face_resized = cv2.resize(face_rgb, (224, 224))
                    face_array = img_to_array(face_resized)
                    face_array = preprocess_input(face_array)
                    face_array = np.expand_dims(face_array, axis=0)

                    preds = model.predict(face_array, verbose=0)[0]
                    class_id = np.argmax(preds)
                    confidence = preds[class_id] * 100

                    pred_id = "Unknown"
                    name = "Unknown"
                    color = (0, 0, 255)

                    if confidence > 75:
                        potential_id = label_map.get(class_id, None)
                        if potential_id and potential_id != "Unknown":
                            try:
                                conn = sqlite3.connect("face_recognation.db")
                                cursor = conn.cursor()

                                cursor.execute("""
                                    SELECT Student_ID, Student_Name 
                                    FROM face_recognizer 
                                    WHERE Student_ID = ? 
                                    AND Department = ? 
                                    AND Batch = ? 
                                    AND Class_Section = ?
                                """, (int(potential_id), dept_gui, batch_gui, section_gui))

                                data = cursor.fetchone()
                                if data:
                                    pred_id, name = data
                                    color = (0, 255, 0)

                                    if pred_id not in self.present_students:
                                        mark_attendance(
                                            student_id=pred_id,
                                            name=name,
                                            dept=dept_gui,
                                            batch=batch_gui,
                                            section=section_gui,
                                            course=course_gui
                                        )
                                        self.present_students.add(pred_id)
                                        cv2.putText(frame, f"PRESENT! ({course_gui})", (x1, y1-35),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                                    else:
                                        cv2.putText(frame, "ALREADY MARKED", (x1, y1-35),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                                conn.close()
                            except Exception as e:
                                print("DB Error:", e)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{pred_id} ({confidence:.1f}%)", (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    if confidence > 75 and pred_id != "Unknown":
                        cv2.putText(frame, f"{name}", (x1, y2+25),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                cv2.imshow("Face Recognition", frame)
                if cv2.waitKey(1) == 13:
                    break

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            video_cap.release()
            cv2.destroyAllWindows()














# its use for LBPH

#     # ================== Face Recognition ==================
#     def face_recog(self):
#         base_path = r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation"

#         modelFile = os.path.join(base_path, "res10_300x300_ssd_iter_140000.caffemodel")
#         configFile = os.path.join(base_path, "deploy.prototxt")
#         classifierFile = os.path.join(base_path, "classifier.xml")
#         dbFile = os.path.join(base_path, "face_recognation.db")

#         # Load DNN Face Detector
#         net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

#         # Load trained recognizer
#         clf = cv2.face.LBPHFaceRecognizer_create()
#         clf.read(classifierFile)

#         # Load database info
#         conn = sqlite3.connect(dbFile)
#         cursor = conn.cursor()
#         cursor.execute("SELECT Student_ID, Student_Name, Department FROM face_recognizer")
#         data_rows = cursor.fetchall()
#         conn.close()
#         db_dict = {str(row[0]): {"name": row[1], "dept": row[2]} for row in data_rows}

#         # Initialize camera
#         video_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#         # Helper function: check overlap
#         def overlap(b1, b2):
#             xa = max(b1[0], b2[0])
#             ya = max(b1[1], b2[1])
#             xb = min(b1[2], b2[2])
#             yb = min(b1[3], b2[3])
#             inter_area = max(0, xb - xa) * max(0, yb - ya)
#             box1_area = (b1[2] - b1[0]) * (b1[3] - b1[1])
#             box2_area = (b2[2] - b2[0]) * (b2[3] - b2[1])
#             union = box1_area + box2_area - inter_area
#             return inter_area / union > 0.4 if union > 0 else False

#         # Start face recognition loop
#         while True:
#             if self.stop_detection:
#                 break

#             ret, img = video_cap.read()
#             if not ret:
#                 break

#             h, w = img.shape[:2]

#             blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
#                                         (300, 300), (104.0, 177.0, 123.0))
#             net.setInput(blob)
#             detections = net.forward()

#             processed_boxes = []

#             for i in range(detections.shape[2]):
#                 confidence = detections[0, 0, i, 2]
#                 if confidence < 0.45:
#                     continue

#                 box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                 (x1, y1, x2, y2) = box.astype("int")

#                 x1, y1 = max(0, x1), max(0, y1)
#                 x2, y2 = min(w - 1, x2), min(h - 1, y2)

#                 if any(overlap((x1, y1, x2, y2), pb) for pb in processed_boxes):
#                     continue

#                 roi_gray = cv2.cvtColor(img[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)

#                 try:
#                     id, predict = clf.predict(roi_gray)
#                     acc = int((100 * (1 - predict / 300)))
#                 except:
#                     continue

#                 info = db_dict.get(str(id), {"name": "Unknown", "dept": ""})
#                 name, dept = info["name"], info["dept"]

#                 if acc > 75:
#                     cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                     cv2.putText(img, f"ID: {id}", (x1, y1 - 55),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
#                     cv2.putText(img, f"Name: {name}", (x1, y1 - 30),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
#                     cv2.putText(img, f"Department: {dept}", (x1, y1 - 5),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
#                 else:
#                     cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
#                     cv2.putText(img, "Unknown", (x1, y1 - 10),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

#                 processed_boxes.append((x1, y1, x2, y2))

#             cv2.imshow("Face Recognition (DNN)", img)

#             if cv2.waitKey(1) == 13:
#                 break

#         video_cap.release()
#         cv2.destroyAllWindows()





if __name__ == "__main__":
    root = Tk()
    app = FaceDetectorGUI(root)
    root.mainloop()
