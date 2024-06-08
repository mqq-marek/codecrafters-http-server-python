import socket


class Request:
    def __init__(self, content: bytes):
        self.content = content.decode("utf-8")
        self.command, self.headers, self.body = self.parse_all()
        self.cmd, self.path, self.version = self.parse_command()

    def parse_all(self):
        items = self.content.split("\r\n")
        command = items[0]
        headers = {}
        parse_headers = True
        body_parts = []
        for item in items[1:]:
            if parse_headers:
                if item:
                    key, value = item.split(": ", maxsplit=1)
                    headers[key] = value
                else:
                    parse_headers = False
            else:
                body_parts.append(item)
        return command, headers, "\r\n".join(body_parts)

    def parse_command(self):
        cmd, rest = self.command.split(" ", maxsplit=1)
        path, rest = rest.strip().split(" ", maxsplit=1)
        version = rest.strip()
        return cmd, path, version


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    connection, address = server_socket.accept()  # wait for client
    print(f"Accept {connection=}, {address=}")
    request = Request(connection.recv(1024))
    print(request.command, request.cmd, request.path, request.version, request.headers, request.body)
    if request.path == "/":
        connection.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
    else:
        connection.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')


if __name__ == "__main__":
    main()
