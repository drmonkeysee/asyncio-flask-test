import locust


class Tasks(locust.TaskSet):
    @locust.task(1)
    def concurrent(self):
        self.client.get('/concurrent')

    @locust.task(2)
    def with_timeout(self):
        self.client.get('/concurrent?timeout=1.2')

    @locust.task(3)
    def serial(self):
        self.client.get('/serial')


class User(locust.HttpLocust):
    task_set = Tasks
