from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import handleEphemerals

def start():
    print("start called")
    scheduler = BackgroundScheduler()
    scheduler.add_job(handleEphemerals, "interval", hours=24)
    scheduler.start()