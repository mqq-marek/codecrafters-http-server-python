from socket import socket


class Request:
    def __init__(self, connection: socket):
        self.connection = connection
        self.rfile = connection.makefile("r")
        self.request_line = self.rfile.readline()[:-1]
        print(f"{self.request_line=}")
        self.cmd, self.path, self.query, self.version = self.parse_command()
        self.headers = self.read_headers()
        self.body = self.rfile.read(int(self.headers.get("content-length",0)))

    def read_headers(self):
        headers = {}
        while header_line := self.rfile.readline()[:-1]:
            print(f"{header_line=}")
            if ": " in header_line:
                key, value = header_line.split(": ", maxsplit=1)
                headers[key.lower()] = value
        return headers

    def parse_command(self):
        cmd, rest = self.request_line[:-2].split(" ", maxsplit=1)
        path, rest = rest.strip().split(" ", maxsplit=1)
        version = rest.strip()
        return cmd, path, "", version