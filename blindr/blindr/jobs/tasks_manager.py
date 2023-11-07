from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import makeEphemerals

def start():
    print("start called")
    scheduler = BackgroundScheduler()
    scheduler.add_job(makeEphemerals, "interval", minutes=10)
    scheduler.start()