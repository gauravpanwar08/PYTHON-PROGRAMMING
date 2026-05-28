# Email Background Task
# Simulates sending email in the background.


import time

from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


def send_email(email: str):

    time.sleep(3)

    print(f"Email sent to {email}")


@app.post("/send-email")
def email_task(
    email: str,
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(send_email, email)

    return {
        "message": "Email sending started"
    }