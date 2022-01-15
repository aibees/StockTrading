from batch.proc.job.FirstJob import *
from batch.proc.job.AccountJob import *


def JobFactory(id):
    print("Welcome to Job Factory")

    if type(id) is not str:
        print("wrong type : not str")
        return None
    else:
        if id == "Job_Account":
            return Job_Account()
        elif id == "":
            return FirstJob()
        else:
            return None
