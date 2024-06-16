import os
import socket
from concurrent.futures import ThreadPoolExecutor

from app import arguments
from app.response import Response
from app.dispatcher import route
from app.web_server import WebServerApp


@route("GET /")
def root(request, *params):
    response = Response(request.connection, response_code=200)
    return response


@route('GET /echo/([a-zA-Z0-9]+)/?')
def echo(request, *params):
    print(f"Starting /echo, {params=}")
    response = Response(request.connection, response_code=200, headers={"Content-Type": "text/plain"}, body=params[0])
    return response


@route('GET /user-agent/?')
def user_agent(request, *params):
    agent = request.headers.get("user-agent")
    print(f"Starting /user-agent, {agent=}")
    response = Response(request.connection, response_code=200, headers={"Content-Type": "text/plain"}, body=agent)
    return response


@route(r'GET /files/([\-._a-zA-Z0-9]+)/?')
def files(request, *params):
    print(f"Starting /files, {params=}")
    folder = arguments.values["directory"]
    if params:
        file_name = params[0]
        path_to_file = os.path.join(folder, file_name)
        if os.path.exists(path_to_file):
            with open(path_to_file, "rb") as f:
                content = f.read()
            response = Response(request.connection,
                                response_code=200,
                                headers={"Content-Type": "application/octet-stream",
                                         "Content-Length": len(content)}, body=content)
        else:
            response = Response(request.connection, response_code=404)
    return response


if __name__ == "__main__":
    app = WebServerApp()
    app.run()
