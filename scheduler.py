from apscheduler.schedulers.background import BackgroundScheduler
from notification_service import process_hourly_notifications
from database import get_users, get_forecast_for_user

scheduler = BackgroundScheduler()

def hourly_job():
    users = get_users()  # db’den kullanıcılar

    for user in users:
        forecast = get_forecast_for_user(user["id"])
        process_hourly_notifications(user, forecast)

def start_scheduler():
    scheduler.add_job(hourly_job, "cron", minute=0)
    scheduler.start()
