import os

files_to_delete = [
    "face_mobilenetv2_best.keras",   # best checkpoint
    "face_mobilenetv2_final.keras",  # final fine-tuned model
    "label_map.npy"                  # label mapping
]

for file in files_to_delete:
    if os.path.exists(file):
        os.remove(file)
        print(f"✅ Deleted: {file}")
    else:
        print(f"⚠️ File not found: {file}")

