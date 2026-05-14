import time
from loguru import logger

def send_welcome_email(email: str, name: str):
    logger.info(f"[EMAIL TASK] Starting - sending welcome email to {email}")
    
    #Simulation of email
    time.sleep(2)
    logger.info(f"[EMAIL TASK] Done - welcome email sent to {email}")

def send_account_deletion_email(email: str, name: str):
    logger.info(f"[EMAIL TASK] Starting - sending deletion email to {email}")

    time.sleep(1)

    logger.info(f"[EMAIL TASK] Done - deletion email sent to {email}")

def send_password_change_notification(email: str):
    logger.info(f"[EMAIL TASK] Starting - password change notification sent to {email}")
    time.sleep(1)
    logger.info(f"[EMAIL TASK] Done - password change notification sent to {email}")
    