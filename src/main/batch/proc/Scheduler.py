
from apscheduler.schedulers.background import BackgroundScheduler
from batch.proc.JobFactory import JobFactory


class BatchScheduler:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):  # Foo 클래스 객체에 _instance 속성이 없다면
            print("init __new__ is called\n")
            cls._instance = super().__new__(cls)  # Foo 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):  # Foo 클래스 객체에 _init 속성이 없다면
            # print("__init__ is called\n")
            cls._init = True
            self.sched = BackgroundScheduler()
            self.jobList = {}
            print("scheduler started successfully")

    def __del__(self):
        self.shutdown()

    def start(self):
        self.sched.start()

    def shutdown(self):
        self.sched.shutdown()

    def getScheduler(self):
        return self.sched

    def getJobList(self):
        return self.jobList

    # CronJob 추가
    # jobList에 있는지 먼저 확인
    #
    def addCronJob(self, jobId):
        print(self.jobList)
        if jobId in self.jobList:
            print(self.jobList[jobId])
            print(self.jobList[jobId]['status'])
        if jobId in self.jobList and self.jobList[jobId]['status']:
            return {
                'result' : '이미 활성화된 Job 입니다.'
            }
        else:
            jobs = None
            if jobId in self.jobList: # jobList 안에 있으면
                jobs = JobFactory(jobId) # factory에서 가져오고
                jobs_info = self.jobList[jobId]

                jobs_info['status'] = True # status 갱신
                jobs_info['cron'] = jobs.getCronTime() # crontab 갱신
                self.jobList[jobId] = jobs_info # 갱신한거 다시 넣기
            else: # list에 없으면
                jobs = JobFactory(jobId)
                self.jobList[jobId] = {
                    'obj': jobId,
                    'status': True,
                    'cron': jobs.getCronTime()
                }
            #print("add schedule job : ", jobs)

            cronTime = jobs.getCronTime()
            self.sched.add_job(jobs.getJob(), 'cron',
                               id    =jobId             ,
                               year  =cronTime['year']  ,
                               month =cronTime['month'] ,
                               day   =cronTime['day']   ,
                               hour  =cronTime['hour']  ,
                               minute=cronTime['minute'],
                               second=cronTime['second'])

            return {
                'result': True,
                'data': self.getJobList()
            }

    def removeCronJob(self, jobId):
        return {
            'result': True,
            'data': 'removeJob'
        }

