import json
import pathlib
import sys
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from service_a import ServiceAHandler


class ServiceATest(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), ServiceAHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def test_root_returns_service_status(self):
        connection = HTTPConnection("127.0.0.1", self.server.server_port)
        connection.request("GET", "/")
        response = connection.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(
            json.loads(response.read()),
            {"service": "service-a", "version": "0.1.0", "status": "running"},
        )

    def test_other_paths_return_not_found(self):
        connection = HTTPConnection("127.0.0.1", self.server.server_port)
        connection.request("GET", "/missing")
        self.assertEqual(connection.getresponse().status, 404)


if __name__ == "__main__":
    unittest.main()
