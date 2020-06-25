import redis
import time
from rq import Queue, Connection
from addons.wa_automation.models.config import BaseConfig
from addons.wa_automation.models.sender import Send_Whatsapp

def create_task(message, interval, no_wa):
    #send message based interval
    pass

def sender_task(message, interval, no_wa):
    url = BaseConfig.REDIS_URL
    with Connection(redis.from_url(url)):
        q = Queue()
        q.enqueue(create_task, message, interval, no_wa)
