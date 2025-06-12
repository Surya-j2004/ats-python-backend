import os

def save_uploaded_file(uploaded_file, save_dir="uploads"):
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, uploaded_file.filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.file.read())
    return file_path

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
