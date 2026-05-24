# Forms & File Uploads: It uses "python-multipart" module to parse form data.
# It is used to receive form fields and uploaded files from clients.
# FastAPI provides the Form and File classes to handle form data and file uploads.
#
# Common Uses:
# - Login forms
# - Signup forms
# - Profile image uploads
# - Resume/PDF uploads
# ------------------------------------------------------------------------------------

from fastapi import FastAPI, Form, File, UploadFile
from typing import List

app = FastAPI()


# Form Data Example
@app.post("/login")
def login(
    username: str = Form(),
    password: str = Form()
):

    return {
        "username": username,
        "password": password
    }


# File Upload Example
@app.post("/upload")
def upload_file(
    file: UploadFile = File()
):

    return {
        "filename": file.filename,
        "content_type": file.content_type
    }
    

# Multiple File Upload Example
@app.post("/multiple-files")
def upload_multiple_files(
    files: List[UploadFile] = File()
):

    return {
        "filenames": [file.filename for file in files]
    }
    

# Form + File Together
@app.post("/profile")
def create_profile(
    name: str = Form(),
    age: int = Form(),
    image: UploadFile = File()
):

    return {
        "name": name,
        "age": age,
        "image_name": image.filename
    }