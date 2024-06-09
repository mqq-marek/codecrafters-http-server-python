from socket import socket

responses = {200: "OK", 404: "Not Found"}


class Response:
    def __init__(self, connection: socket, response_code: int, headers: dict[str, str]=None, body: str=""):
        self.response_line = "HTTP/1.1 " + str(response_code) + " " + responses[response_code] + "\r\n"
        self.connection = connection
        self.headers = headers or {}
        self.body = body
        self.wfile = self.connection.makefile('w')

    def send(self):
        self.headers["Content-Length"] = str(len(self.body))
        header_lines = "\r\n".join(key + ": " + value for key, value in self.headers.items())
        output = self.response_line + header_lines + "\r\n\r\n" + self.body
        print(f"Response {output=}")
        self.wfile.write(output)
        self.wfile.flush()
        self.wfile.close()


