import cv2
import os

# ====== Input & Output Folder ======
input_folder = r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\collectded_image"      # আপনার ছবিগুলোর ফোল্ডার
output_folder = r"C:\Users\Asus\OneDrive\Desktop\Acadamic\Final Project\Face Recognation\sample_image_data"  # processed ছবি save হবে এখানে
os.makedirs(output_folder, exist_ok=True)

# ====== Haarcascade Classifiers ======
face_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
profile_cascade_path = cv2.data.haarcascades + "haarcascade_profileface.xml"

face_classifier = cv2.CascadeClassifier(face_cascade_path)
profile_cascade = cv2.CascadeClassifier(profile_cascade_path)

def face_cropped_best(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Front faces
    faces_f = face_classifier.detectMultiScale(gray, 1.1, 5, minSize=(40, 40))
    # Right profile
    faces_r = profile_cascade.detectMultiScale(gray, 1.1, 5, minSize=(40, 40))
    # Left profile
    gray_flipped = cv2.flip(gray, 1)
    faces_l = profile_cascade.detectMultiScale(gray_flipped, 1.1, 5, minSize=(40, 40))
    width = gray.shape[1]
    faces_l_corrected = [(width - x - w, y, w, h) for (x, y, w, h) in faces_l]

    candidates = list(faces_f) + list(faces_r) + faces_l_corrected
    if not candidates:
        return None

    # Largest face
    x, y, w, h = max(candidates, key=lambda r: r[2]*r[3])
    if w < 60 or h < 60:
        return None

    # Add margin
    h_margin = int(0.2 * w)
    v_margin = int(0.2 * h)
    x1 = max(0, x - h_margin)
    y1 = max(0, y - v_margin)
    x2 = min(img.shape[1], x + w + h_margin)
    y2 = min(img.shape[0], y + h + v_margin)

    crop = img[y1:y2, x1:x2]
    face_resized = cv2.resize(crop, (400, 400), interpolation=cv2.INTER_AREA)
    return face_resized

# ====== Process All Images in Folder ======
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

for idx, file_name in enumerate(image_files, start=1):
    img_path = os.path.join(input_folder, file_name)
    img = cv2.imread(img_path)

    if img is None:
        print(f"Failed to read {file_name}")
        continue

    face = face_cropped_best(img)
    if face is not None:
        save_path = os.path.join(output_folder, f"face_{idx}.jpg")
        cv2.imwrite(save_path, face)
        print(f"Saved {save_path}")
    else:
        print(f"No face detected in {file_name}")

print("Processing completed!")
