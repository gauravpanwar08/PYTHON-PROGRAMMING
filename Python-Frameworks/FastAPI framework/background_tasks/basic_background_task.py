# Basic Background Task
# Executes a task after returning the response.

from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def simple_task():
    time.sleep(5)
    print("Background Task completed")
    
@app.get("/")
def home(background_tasks: BackgroundTasks):
    background_tasks.add_task(simple_task)
    
    return {
        "message": "Response returned immediately, background task is running in the background."
    }