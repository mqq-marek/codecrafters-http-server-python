import re

from app.dispatcher import route
from app.response import Response


app_name = "name"

@route("GET /")
def root(request, *params):
    response = Response(request.connection, response_code=200)
    return response


@route('GET /echo/([a-zA-Z0-9]+)/?')
def echo(request, *params):
    response = Response(request.connection, response_code=200, headers={"Content-Type": "text/plain"}, body=params[0])
    return response


@route('GET /user-agent/?')
def user_agent(request, *params):
    agent = request.headers["user-agent"]
    response = Response(request.connection, response_code=200, headers={"Content-Type": "text/plain"}, body=agent)
    return response

get_root = "GET /"
get_echo = "GET /echo/([a-zA-Z0-9]+)/"

if __name__ == "__main__":
    match = re.fullmatch(get_root, "GET /")
    print(f"{match=} match.groups()={match.groups()}")
    match = re.fullmatch(get_echo, "GET /echo/123456/")
    print(f"{match=}, match.groups()={match.groups()}")
