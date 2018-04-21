import docker
import logging

class benchmark(object):
    GUNICORN_WORKERS = 5
    DOCKER_IMAGE = 'gunflawor:latest'
    LOADS = {
        'normal':   '',
        'cpu':      '',
        'memory':   '',
        'sleep':    '',
        'slowio':   '',
    }
    WORKER_CLASS = {
        'sync':     {
            'gunicorn_workers': GUNICORN_WORKERS * 10
        },
        'eventlet': {},
        'gevent':   {},
        # 'gthread',  # python3
        # 'gaiohttp'
    }

    def __init__(self):
        self.results = {}
        self.docker_client = docker.from_env()
        self.main()

    def main(self):
        for worker_class in self.WORKER_CLASS:
            self.results[worker_class] = {}
            for load in self.LOADS:
                run_string = 'gunicorn --workers={gunicorn_workers} app.{load}.app:app --worker-class={worker_class}'.\
                    format(gunicorn_workers=self.get_custom_config(worker_class, 'gunicorn_workers', self.GUNICORN_WORKERS),
                           load=load, worker_class=worker_class)
                container = self.docker_client.containers.run(self.DOCKER_IMAGE, run_string, detach=True)
                logging.debug('Running docker with command: {}'.format(run_string))
                result = self.stress_test()
                container.stop()
                self.results[worker_class].update({load: result})

    def get_custom_config(self, worker_class, config, default=None):
        if config in self.WORKER_CLASS[worker_class]:
            return self.WORKER_CLASS[worker_class][config]
        else:
            return default

    def stress_test(self):
        # TODO: We might use locust or Hey (in Go) but it's definitely
        return 100


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    benchmark()