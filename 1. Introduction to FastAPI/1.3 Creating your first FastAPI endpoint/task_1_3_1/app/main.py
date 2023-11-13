from fastapi import FastAPI
from app.models.feedback import Feedback

app = FastAPI()

feedback_storage = {}


@app.post("/feedback")
async def send_feedback(feedback: Feedback):
    add_feedback(feedback)
    return {
        "message": f"Feedback received. Thank you, {feedback.name}!"
    }


def add_feedback(feedback: Feedback):
    name = feedback.name
    message = feedback.message
    if name not in feedback_storage:
        feedback_storage[name] = [message]
    else:
        feedback_storage.get(name).append(message)
