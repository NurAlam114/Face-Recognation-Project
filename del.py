import os

file_path = "classifier.xml"

if os.path.exists(file_path):
    os.remove(file_path)   # file সম্পূর্ণ remove হবে
    print("classifier.xml and all saved face data deleted successfully!")
else:
    print("File not found!")
