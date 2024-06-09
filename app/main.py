
import socket
from concurrent.futures import ThreadPoolExecutor

from app.routes import app_name
from app.dispatcher import Dispatcher
from app.request import Request



def request_processor(server_socket):
    while True:
        connection, address = server_socket.accept()  # wait for client
        print(f"Accept {connection=}, {address=}")
        request = Request(connection)
        Dispatcher.dispatch(request)

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print(f"Starting server {app_name}")
    with ThreadPoolExecutor(max_workers=10) as executor:
        request_futures = [executor.submit(request_processor, server_socket) for _ in range(10)]


if __name__ == "__main__":
    print("Starting server", app_name)
    main()
