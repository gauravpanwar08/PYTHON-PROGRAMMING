# Logging Background Task
# Saves logs without delaying API response.


import time

from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


def save_log(message: str):

    time.sleep(2)

    with open("log.txt", "a") as file:

        file.write(message + "\n")


@app.get("/")
def home(background_tasks: BackgroundTasks):

    background_tasks.add_task(
        save_log,
        "Home endpoint accessed"
    )

    return {
        "message": "Log task started"
    }