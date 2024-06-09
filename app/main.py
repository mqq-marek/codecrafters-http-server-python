import socket
from app.routes import app_name
from app.dispatcher import Dispatcher
from app.request import Request





def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        connection, address = server_socket.accept()  # wait for client
        print(f"Accept {connection=}, {address=}")
        request = Request(connection)
        Dispatcher.dispatch(request)
        # if request.path == "/":
        #     connection.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
        # elif request.path.startswith("/echo/"):
        #     headers = ''
        #     echo_str = request.path.replace("/echo/", "")
        #     response = 'HTTP/1.1 200 OK\r\n' + headers + echo_str
        #     connection.makefile('w').write(response)
        #
        # else:
        #     connection.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')


if __name__ == "__main__":
    print("Starting server", app_name)
    main()
