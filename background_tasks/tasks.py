import time
import random
from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger("tasks")


def send_msg_by_fcm(device_token):
    logger.info(f"sent using fcm {device_token}")
    return True


@shared_task(bind=True)
def send_notification(self, device_token: str):
    try:
        logger.info("starting background task")
        time.sleep(2)  # simulates slow network call
        if random.choice([0, 1]):
            raise Exception()
    except Exception as e:
        raise self.retry(exc=e, countdown=10, max_retries=3)
