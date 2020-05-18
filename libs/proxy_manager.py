import heapq
import time
import logging
from threading import Lock
import requests
from settings import PROXY_FILE_PATH

class Proxy:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.can_use_time = time.time()
        self.counter = 0
        self.status = 'n/a'

    def __lt__(self, other):
        return self.can_use_time < other.can_use_time

    def __repr__(self):
        return '{}:{} [{} - {} - {}]'.format(
            self.ip, self.port, self.counter, self.can_use_time, self.status
        )

    def __str__(self):
        return '{}:{}'.format(self.ip, self.port)

    def check_proxy(self):
        proxies = {
            'http': f'http://{self.ip}:{self.port}',
            'https': f'https://{self.ip}:{self.port}'
        }

        data = requests.get(
            url='https://httpbin.org/anything',
            proxies=proxies,
            timeout=5).json()
        return data['origin']


class ProxyManager:
    def __init__(self, log, ok_timeout=1, ban_timeout=10):
        self.log = log
        self.proxies = self.read_file()
        self.ok_proxies = [Proxy(ip, port) for ip, port in self.proxies]
        heapq.heapify(self.ok_proxies)
        self.ban_proxies = []
        heapq.heapify(self.ban_proxies)
        self.ban_timeout = ban_timeout
        self.ok_timeout = ok_timeout
        self.locker = Lock()


    def read_file(self):
        with open(PROXY_FILE_PATH, 'r') as f:
            proxies = [s.strip().split(':') for s in f.readlines()]
        return proxies

    def next_proxy(self):
        cur_time = time.time()
        can_use_time = cur_time * 10
        new_proxy = None

        with self.locker:
            if self.ok_proxies:
                new_proxy: Proxy = heapq.heappop(self.ok_proxies)
                can_use_time = new_proxy.can_use_time
            elif self.ban_proxies:
                new_proxy = heapq.heappop(self.ban_proxies)
                can_use_time = new_proxy.can_use_time
            else:
                self.log.debug('ok and ban are empty!')

            if can_use_time < cur_time:
                return new_proxy

        raise IndexError('no proxies left')

    def back_proxy(self, proxy: Proxy, response: str):
        proxy.counter += 1
        proxy.status = response
        with self.locker:
            if response == 'ok':
                proxy.can_use_time = time.time() + self.ok_timeout
                heapq.heappush(self.ok_proxies, proxy)
            else:
                proxy.can_use_time = time.time() + self.ban_timeout
                heapq.heappush(self.ban_proxies, proxy)


    def proxy_generator(self):
        while True:
            try:
                yield self.next_proxy()
            except GeneratorExit:
                break
            except:
                time.sleep(0.1)


if __name__ == '__main__':
    PROXY_FILE_PATH = '../' + PROXY_FILE_PATH
    p = ProxyManager(logging)
    logging.debug('some message')
    pg = p.proxy_generator()
    for i in range(10):
        print(i)
        np = next(pg)
        print(np)
        p.back_proxy(np, 'ok' if i % 2 == 0 else 'ban')

    for p in p.ok_proxies + p.ban_proxies:
        print(repr(p))

    print('finish')