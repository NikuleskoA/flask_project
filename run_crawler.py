import signal
import threading
from libs.crawler_lxml import VesselCrawlerLxml


if __name__ == '__main__':
    exit_event = threading.Event()

    def call_stop(*args):
        exit_event.set()

    signal.signal(signal.SIGINT, call_stop)

    sg = VesselCrawlerLxml(exit_event)
    sg.run()