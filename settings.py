DB_URL = 'postgres://postgres:123456@localhost:5432/ships'

PROXY_FILE_PATH = "static/proxies.txt"

RABITMQ_URL = 'amqp://pojnsheq:uK8vO6MmHd-E6R2Y6--OCs5JvpffhAiA@buck.rmq.cloudamqp.com/pojnsheq'

CRAWLER_QUEUE_NAME = "crawl_pages"
CRAWLER_EXCHANGE_NAME = "ex_crawl_pages"
MAX_QUEUE_SIZE = 100
PAGE_URL = "https://www.vesselfinder.com/vessels?page={num}"
MAX_PAGES = 1 #20_000

DRIVER_PATH = "bin/chromedriver"
IS_HEADLESS = False
NUM_WORKERS = 4
USE_PROXY = False


