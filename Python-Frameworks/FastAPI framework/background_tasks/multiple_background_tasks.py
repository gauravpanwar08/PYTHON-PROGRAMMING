# Multiple Background Tasks
# Executes multiple tasks in background.


import time

from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


def task_one():

    time.sleep(2)

    print("Task One Completed")


def task_two():

    time.sleep(3)

    print("Task Two Completed")


@app.get("/")
def home(background_tasks: BackgroundTasks):

    background_tasks.add_task(task_one)

    background_tasks.add_task(task_two)

    return {
        "message": "Multiple tasks started"
    }