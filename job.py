import time

import schedule as schedule

from job import cleandata


def job():
    cleandata.run()


schedule.every(2).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
