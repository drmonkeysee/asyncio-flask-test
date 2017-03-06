import locust


class Tasks(locust.TaskSet):
    @locust.task(1)
    def serial(self):
        self.client.get('/serial')

    @locust.task(2)
    def serial_with_timeout(self):
        self.client.get('/serial?timeout=1.2')

    @locust.task(3)
    def gather(self):
        self.client.get('/gather')

    @locust.task(4)
    def gather_with_timeout(self):
        self.client.get('/gather?timeout=1.2')

    @locust.task(3)
    def async(self):
        self.client.get('/async')

    @locust.task(4)
    def async_with_timeout(self):
        self.client.get('/async?timeout=1.2')


class User(locust.HttpLocust):
    task_set = Tasks
