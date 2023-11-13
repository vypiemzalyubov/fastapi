from fastapi import FastAPI
from app.models.feedback import Feedback

app = FastAPI()


@app.post("/feedback")
async def add_feedback(feedback: Feedback):
    save_feedback(feedback)
    return {
        "message": f"Feedback received. Thank you, {feedback.name}!"
    }


def save_feedback(feedback: Feedback):
    feedback_storage = {}
    feedback_storage.update(
        {"name": f"{feedback.name}", "message": f"{feedback.message}"})
    print(feedback_storage)
