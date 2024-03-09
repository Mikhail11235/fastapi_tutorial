import os
import logging
from fastapi import FastAPI
from celery import Celery
from celery.signals import after_setup_logger
from config import settings
from tasks import send_notification


if not os.path.exists("logs"):
    os.makedirs("logs")


logging.basicConfig(filename="logs/app.log", level=logging.INFO , format="%(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


app = FastAPI()


celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)


@after_setup_logger.connect
def setup_celery_logger(logger, *args, **kwargs):
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("tasks")
    fh = logging.FileHandler("logs/tasks.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)


@app.get("/push/{device_token}")
async def notify(device_token: str):
    logger.info("sending notification in background")
    send_notification.delay(device_token)
    return {"message": "Notification sent"}


@app.get("/status/{task_id}")
async def task_status(task_id: str):
    task = celery.AsyncResult(task_id)
    if task.state == "SUCCESS":
        return {"status": "done", "result": task.result}
    elif task.state == "PENDING":
        return {"status": "pending"}
    else:
        return {"status": "failed"}
