import json

from flask import jsonify
from flask_restx import Resource, Api, Namespace
from batch.proc.Scheduler import BatchScheduler

Batch = Namespace('Batch')

@Batch.route('')
class BatchRoot(Resource):

    def get(self):
        sched = BatchScheduler()
        return {
            'jobList': sched.getJobList()
        }


@Batch.route('/add/<string:jobId>')
class BatchAdd(Resource):
    def get(self, jobId):
        sched = BatchScheduler()
        return sched.addCronJob(jobId)


@Batch.route('/rmv/<string:jobId>')
class BatchRemove(Resource):
    def get(self, jobId):
        sched = BatchScheduler()
        sched.removeCronJob(jobId)

        return {
            'jobList' : sched.getJobList()
        }
