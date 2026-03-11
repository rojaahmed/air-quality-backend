from apscheduler.schedulers.background import BackgroundScheduler
from services.notification_worker import run_notification_job

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        run_notification_job,
        "interval",
        minutes=15
    )
    scheduler.start()