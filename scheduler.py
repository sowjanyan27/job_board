import os

from apscheduler.schedulers.background import BackgroundScheduler
import requests
import logging

from dotenv import load_dotenv
from pytz import timezone

load_dotenv()
BASE_API_URL = os.getenv("BASE_API_URL")

def call_user_filter_api():
    try:
        url = f"{BASE_API_URL}/users/filter?skip=0&limit=10"
        response = requests.get(url)
        logging.info(f"Scheduled call result: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Error calling /users/filter: {str(e)}")
#
# def call_user_filter_api():
#     try:
#         # Adjust query parameters as needed
#         response = requests.get("http://127.0.0.1:8025/users/filter?skip=0&limit=10")
#         logging.info(f"Scheduled call result: {response.status_code} - {response.text}")
#     except Exception as e:
#         logging.error(f"Error calling /users/filter: {str(e)}")

def start_scheduler():
    india_tz = timezone('Asia/Kolkata')
    scheduler = BackgroundScheduler(timezone=india_tz)
    # Trigger every day at 12:00 AM (midnight) IST hour=0, minute=0 means 00:00 hours = midnight

    # scheduler.add_job(call_user_filter_api, 'cron', hour=0, minute=0)

    scheduler.add_job(call_user_filter_api, 'cron', hour=11, minute=40)
    scheduler.start()
