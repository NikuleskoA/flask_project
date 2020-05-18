import threading
import signal
from libs.task_generator import ShipsGenerator


if __name__ == '__main__':
    exit_event = threading.Event()

    def call_stop(*args):
        exit_event.set()

    signal.signal(signal.SIGINT, call_stop)

    sg = ShipsGenerator(exit_event)
    sg.run()