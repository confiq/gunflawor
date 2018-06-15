import docker
import logging
import requests

from time import sleep
from boom import boom

# CONFIGURATIONS:
## StressTest
BOOM_REQUESTS = 500  # Number of request that it will send to app
BOOM_CONCURRENCY = 50

## misc
GUNICORN_WORKERS = 5  # default workers when starting gunicorn
WORKING_PORT = 9081
# endregion

class Benchmark(object):

    DOCKER_IMAGE = 'gunflawor:latest'
    # overwriting default configs
    LOADS = {
        'normal': '',
        'cpu': '',
        'memory': '',
        'sleep': '',
        # 'slow_api': '',
    }
    WORKER_CLASS = {
        'sync': {
            'gunicorn_workers': GUNICORN_WORKERS * 10
        },
        'eventlet': {},
         'gevent': {},
        'gthread': {},
        'gaiohttp': {}
        # TODO: gevent.wsgi
    }

    def __init__(self):
        self.results = {}
        self.docker_client = docker.from_env()

    def main(self):
        for worker_class in self.WORKER_CLASS:
            self.results[worker_class] = {}
            for load in self.LOADS:
                run_string = 'gunicorn -b 0.0.0.0:{port} --workers={gunicorn_workers} app.{load}.app:app --worker-class={worker_class}'.\
                    format(port=WORKING_PORT,gunicorn_workers=self._get_custom_config(worker_class, 'gunicorn_workers', GUNICORN_WORKERS),
                           load=load, worker_class=worker_class)
                try:
                    container = self.docker_client.containers.run(self.DOCKER_IMAGE, run_string, detach=True,
                                                              ports={'{}/tcp'.format(WORKING_PORT): WORKING_PORT})
                except requests.exceptions.ConnectionError:
                    logger.error("Is docker up?")
                    raise
                logger.debug('Running docker with command: {}'.format(run_string))
                self.is_container_alive(container)
                result = self.stress_test()
                # TODO: print last few lines from docker and also check if it's still alive
                container.stop()
                self.results[worker_class].update({load: result})
        print "{}".format(self.results)

    def _get_custom_config(self, worker_class, config, default=None):
        if config in self.WORKER_CLASS[worker_class]:
            return self.WORKER_CLASS[worker_class][config]
        else:
            return default

    def is_container_alive(self, container):
        container.reload()
        if container.status != 'running':
            raise RuntimeError('Docker {id} is not running. The logs of container is: {logs}'.
                               format(id=container.short_id, logs=container.logs()))
        for retries in range(1, 10):
            try:
                res = requests.get('http://127.0.0.1:{}/'.format(WORKING_PORT))
                if not res and not res.ok:
                    logger.error('The container did not return OK code. This is probably due misconfiguration of the worker. Result: {}'.format(res.content))
                break
            except requests.exceptions.ConnectionError:
                logger.debug('retrying to connect to container {id}'.format(id=container.short_id))
                sleep(1)
                continue
        else:
            raise RuntimeError('Docker {id} did not respond to request. Logs: {logs}'.
                               format(id=container.short_id, logs=container.logs()))

    def stress_test(self):
        res = boom.load('http://127.0.0.1:/'.format(WORKING_PORT), BOOM_REQUESTS, BOOM_CONCURRENCY, None, 'GET', '', ct='text/plain',
                        auth=None, quiet=True)
        res = boom.calc_stats(res)
        return round(res.rps, 2)


if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    Benchmark().main()
