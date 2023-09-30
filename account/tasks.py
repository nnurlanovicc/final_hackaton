from .utils import send_activation_code_to_recruiter,send_activation_code_to_user

from config.celery import app

@app.task
def send_activation_code_celery_to_recruiter(email, activation_code):
    send_activation_code_to_recruiter(email, activation_code)


@app.task
def send_activation_code_celery_to_user(email, activation_code):
    send_activation_code_to_user(email, activation_code)