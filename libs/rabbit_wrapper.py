import threading
import multiprocessing as mp
import rabbitpy
from settings import RABITMQ_URL

class RabbitQueue:
    def __init__(self, exchange_name, queue_name):
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.routing_key = queue_name

        self.connection = rabbitpy.Connection(RABITMQ_URL)
        self.channel = self.connection.channel()

        self.exchange = rabbitpy.Exchange(
            self.channel, self.exchange_name, durable=True)
        self.exchange.declare()

        self.queue = rabbitpy.Queue(
            self.channel, self.queue_name, durable=True)
        self.queue.declare()

        self.queue.bind(self.exchange_name, routing_key=self.routing_key)

    def publish(self, msg: dict):
        m = rabbitpy.Message(self.channel, msg)
        m.publish(self.exchange_name, routing_key=self.routing_key)

    def consume_generator(self, threads=1):
        for msg in self.queue.consume(prefetch=threads):
            data = msg.json()
            if not data:
                msg.ack()
                break
            yield data


    def get_generator(self, exit_event):
        while not exit_event.is_set():
            msg = self.queue.get(acknowledge=True)
            yield msg

    def count(self):
        return len(self.queue)

    def close(self):
        self.channel.close()
        self.connection.close()

def function_publish(num):
    for i in range(num):
        print("published")
        rq.publish({i: "i am {0} message".format(i)})

def function_read():
    ex_ev = mp.Event()
    for raw_msg in rq.get_generator(ex_ev):
        if not raw_msg:
            break
        print(raw_msg.json())
        raw_msg.nack(requeue=False)
    rq.close()

if __name__ == '__main__':
    rq = RabbitQueue('test-exchange', 'test-queue')

    thr1 = threading.Thread(target=function_publish, args=(100,))
    thr2 = threading.Thread(target=function_read, args=())

    thr1.start()
    thr2.start()

    thr1.join()
    thr2.join()


