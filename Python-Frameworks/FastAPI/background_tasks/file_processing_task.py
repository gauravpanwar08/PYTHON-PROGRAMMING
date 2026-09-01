# File Processing Background Task
# Simulates processing uploaded files in background.


import time

from fastapi import FastAPI, BackgroundTasks, UploadFile, File

app = FastAPI()


def process_file(filename: str):

    time.sleep(5)

    print(f"Processed File: {filename}")


@app.post("/upload")
def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File()
):

    background_tasks.add_task(
        process_file,
        file.filename
    )

    return {
        "filename": file.filename,
        "message": "File uploaded and processing started"
    }