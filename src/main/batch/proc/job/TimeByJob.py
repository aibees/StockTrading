import pythoncom

class TimeByJob:
    def __init__(self):
        self.id = "Job_TimeBy"
        self.cron = {

        }

    def getId(self):
        return self.id

    def getJob(self):
        return self.process

    def process(self):
        print("TimeBy Job Batch Started")
        print("########################")
        pythoncom.CoInitialize()
        
        pythoncom.CoUnitialize()