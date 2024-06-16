import gzip

from app.request import Request

responses = {200: "OK", 201: "Created", 404: "Not Found", 503: "Service Unavailable"}


class Response:
    def __init__(
        self,
        request: Request,
        response_code: int,
        headers: dict[str, str] = None,
        body: bytes = "",
    ):
        self.response_line = (
            "HTTP/1.1 " + str(response_code) + " " + responses[response_code] + "\r\n"
        )
        self.request = request
        self.connection = request.connection
        self.headers = headers or {}
        self.body = body

    def send(self):
        if isinstance(self.body, str):
            self.body = self.body.encode("utf-8")
        if self.request.accept_encoding and "gzip" in self.request.accept_encoding:
            print("gzip")
            self.headers["Content-Encoding"] = "gzip"
            self.body = gzip.compress(self.body)
            print(f"gzip {self.body.hex()}")
        if isinstance(self.body, str):
            self.body = self.body.encode("utf-8")
        self.headers["Content-Length"] = str(len(self.body))
        header_lines = "\r\n".join(
            key + ": " + value for key, value in self.headers.items()
        )
        print(self.response_line + header_lines)
        print(self.body)
        output = (self.response_line + header_lines + "\r\n\r\n").encode('ascii') + self.body
        print(output)
        self.connection.sendall(output)


    def __str__(self):
        return f"Response {self.response_line},  headers: {self.headers},  body: {self.body}"

