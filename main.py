import docker


class DockerHelper(object):
    def __init__(self):
        pass

    def run(self, command):
        return 'TODO'

    def stop(self, container_id):
        return 'TODO'

    def get_client(self):
        return docker.from_env()


class benchmark(object):
    GUNICORN_WORKERS = 5
    LOADS = {
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
        self.main()

    def main(self):
        for worker in self.TYPE_OF_WORKERS:
            self.results[worker] = {}
            for load in self.LOADS:
                container_id = DockerHelper.run()
                result = self.stress_test()
                DockerHelper.stop(container_id)
                self.results[worker].update({load: result})

    def stress_test(self):
        pass


if __name__ == "__main__":
    benchmark()