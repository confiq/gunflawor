import docker


class benchmark(object):
    GUNICORN_WORKERS = 5
    LOADS = {
        'normal':   '',
        'cpu':      '',
        'memory':   '',
        'sleep':    '',
        'slowio':   '',
    }
    TYPE_OF_WORKERS = [
        'sync',
        'eventlet',
        'gevent',
        #'gthread',
        #'gaiohttp'
    ]
    def __init__(self):
        self.results = {}
        self.docker_client = docker.from_env()
        self.main()

    def main(self):
        for worker in self.TYPE_OF_WORKERS:
            self.results[worker] = {}
            for load in self.LOADS:
                container = self.docker_client.containers.run('pwd', detach=True)
                result = self.stress_test()
                container.stop()
                self.results[worker].update({load: result})

    def stress_test(self):
        # TODO: We might use locust or Hey (in Go) but it's definitely
        return 100


if __name__ == "__main__":
    benchmark()