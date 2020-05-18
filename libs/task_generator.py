from libs.postgres_db import DbPg
from libs.rabbit_wrapper import RabbitQueue
from settings import CRAWLER_QUEUE_NAME, CRAWLER_EXCHANGE_NAME, MAX_QUEUE_SIZE, PAGE_URL, MAX_PAGES


class ShipsGenerator:
    def __init__(self, exit_event):
        self.exit_event = exit_event
        self.was_pages = {}
        self.db = DbPg(logger=None)
        self.rqueue = RabbitQueue(CRAWLER_EXCHANGE_NAME, CRAWLER_QUEUE_NAME)
        self.wait_queue()
        self.init_progress_table()
        self.get_ready_tasks()

    def wait_queue(self):
        while self.rqueue.count() > 0:

            if self.exit_event.wait(10):
                break

    def get_ready_tasks(self):
        query = '''SELECT * FROM pages'''
        for row in self.db.get_query(query):
            self.was_pages[row[0]] = True


    def run(self):
        for i in range(MAX_PAGES):
            if self.exit_event.is_set():
                break
            if self.was_pages.get(i):
                continue
            msg = {'url': PAGE_URL.format(num=i), 'num': i}

            while self.rqueue.count() > MAX_QUEUE_SIZE:
                if self.exit_event.wait(5):
                    return
            self.rqueue.publish(msg)


    def init_progress_table(self):
        query = '''CREATE TABLE IF NOT EXISTS pages (page_num integer UNIQUE )'''
        self.db.exec_query(query)