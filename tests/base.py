import moco
import unittest


class MocoTestCase(unittest.TestCase):

    databases = [
        {"host": "localhost",
         "user": "playhaven",
         "passwd": "password",
         "db": "test",
         "use_unicode": True},
        {"host": "localhost",
         "user": "playhaven",
         "passwd": "password",
         "db": "test"}
    ]

    def setUp(self):
        self.connections = []
        for params in self.databases:
            self.connections.append(moco.connect(**params))

    def tearDown(self):
        for connection in self.connections:
            connection.close()
