import docker
import logging
import requests

from time import sleep
from boom import boom

# CONFIGURATIONS:
## StressTest
BOOM_REQUESTS = 1000  # Number of request that it will send to app
BOOM_CONCURRENCY = 10

## misc
GUNICORN_WORKERS = 5  # default workers when starting gunicorn
# endregion

class Benchmark(object):

    DOCKER_IMAGE = 'gunflawor:latest'
    # overwriting default configs
    LOADS = {
        'normal': '',
        'cpu': '',
        # 'memory': '',
        # 'sleep': '',
        # 'slow_api': '',
    }
    WORKER_CLASS = {
        'sync': {
            'gunicorn_workers': GUNICORN_WORKERS * 10
        },
        'eventlet': {},
        'gevent': {},
        # 'gthread',  # python3
        # 'gaiohttp'
        # TODO: gevent.wsgi
    }

    def __init__(self):
        self.results = {}
        self.docker_client = docker.from_env()
        self.main()

    def main(self):
        for worker_class in self.WORKER_CLASS:
            self.results[worker_class] = {}
            for load in self.LOADS:
                run_string = 'gunicorn -b 0.0.0.0:9080 --workers={gunicorn_workers} app.{load}.app:app --worker-class={worker_class}'.\
                    format(gunicorn_workers=self.get_custom_config(worker_class, 'gunicorn_workers', GUNICORN_WORKERS),
                           load=load, worker_class=worker_class)
                container = self.docker_client.containers.run(self.DOCKER_IMAGE, run_string, detach=True,
                                                              ports={'9080/tcp': 9080})
                logging.debug('Running docker with command: {}'.format(run_string))
                self.is_container_alive(container)
                result = self.stress_test()  # TODO: what stresstest tool to use?
                # TODO: print last few lines from docker and also check if it's still alive
                container.stop()
                self.results[worker_class].update({load: result})

    def get_custom_config(self, worker_class, config, default=None):
        if config in self.WORKER_CLASS[worker_class]:
            return self.WORKER_CLASS[worker_class][config]
        else:
            return default

    def is_container_alive(self, container):
        container.reload()
        if container.status != 'running':
            raise RuntimeError('Docker {id} is not running. The logs of container is: {logs}'.
                               format(id=container.short_id, logs=container.logs()))
        for retries in xrange(1, 10):
            try:
                res = requests.get('http://127.0.0.1:9080/')
                if not res and not res.ok:
                    logging.error('The docker did not return OK')
                break
            except requests.exceptions.ConnectionError:
                logging.info('retrying to connect to container {id}'.format(id=container.short_id))
                continue
        else:
            raise RuntimeError('Docker {id} did not respond to request. Logs: {logs}'.
                               format(id=container.short_id, logs=container.logs()))

    def stress_test(self):
        res = boom.load('http://127.0.0.1:9080/', BOOM_REQUESTS, BOOM_CONCURRENCY, None, 'GET', '', ct='text/plain',
                        auth=None, quiet=True)
        res = boom.calc_stats(res)
        return round(res.rps, 2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    Benchmark()
