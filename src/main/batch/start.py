import sys, os
import time

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from batch.proc.JobFactory import JobFactory
from batch.proc.Scheduler import BatchScheduler


def start_daemon():
    print('start daemon')
    process()


def start_test():
    print("start : batchDaemon Test")
    sched = BatchScheduler()
    sched.start()
    sched.addCronJob("Job_Account")
    while(True):
        time.sleep(1000)


def process():
    print('processing')


def main():
    try:
        if sys.argv[1] == 'start':
            start_daemon()
        elif sys.argv[1] == 'test':
            start_test()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
