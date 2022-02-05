import pika

from module.util.Config import Config


class Publisher:
    def __init__(self):
        self.conf = Config()
        self.conn = None

    def connection(self):
        url = self.conf.getConfig('rabbit_dev', 'MQ_HOST')
        port = 9098
        vhost = self.conf.getConfig('rabbit_dev', 'MQ_VHOST')
        user = self.conf.getConfig('rabbit_dev', 'MQ_USER')
        pswd = self.conf.getConfig('rabbit_dev', 'MQ_PSWD')
        cred = pika.PlainCredentials(user, pswd)
        return pika.BlockingConnection(pika.ConnectionParameters(
            host=url,
            port=port,
            virtual_host=vhost,
            credentials=cred
        ))

    def publish(self, queue, msg):
        channel = self.connection().channel()

        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=msg
        )
