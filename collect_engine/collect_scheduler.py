import schedule
import time
import os
import datetime

collect_time = "16:00"
print(f'Current time: {datetime.datetime.now()}')
print(f'Scheduler set to: {collect_time}')


def job():
    os.system('python engine.py')


if __name__ == '__main__':

    schedule.every().day.at(collect_time).do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)