import socket
from concurrent.futures import ThreadPoolExecutor

from app.dispatcher import Dispatcher
from app.request import Request


class WebServerApp:
    def __init__(
        self,
        host: str = None,
        port: int = None,
        app_name: str = "WebServer",
        threads: int = 10,
    ):
        self.host = host if host else "localhost"
        self.port = port if port else 4221
        self.threads = threads
        self.app_name = app_name

    def run(self):
        print(f"Starting server {self.app_name} on {self.host}:{self.port}")
        server_socket = socket.create_server((self.host, self.port), reuse_port=True)
        print("Server socket initialized")
        with ThreadPoolExecutor(max_workers=10) as executor:
            request_futures = [
                executor.submit(self.request_processor, server_socket)
                for _ in range(self.threads)
            ]

    def request_processor(self, server_socket):
        while True:
            connection, address = server_socket.accept()  # wait for client
            request = Request(connection)
            print(
                f"Accept connection from {address=} with {request.request_line}\nHeaders: {request.headers}"
            )
            Dispatcher.dispatch(request)
