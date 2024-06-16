import re

from app.request import Request
from app.response import Response


class Dispatcher:
    routes = {}

    @classmethod
    def add_route(cls, path, handler):
        cls.routes[path] = handler

    @classmethod
    def dispatch(cls, request: Request):
        cmd_path = " ".join([request.cmd, request.path])
        print(f"dispatcher: ", cmd_path, cls.routes)
        for key, value in cls.routes.items():
            match = re.fullmatch(key, cmd_path)
            print(f"f{key=}, {cmd_path=}, {match=}, {type(match)=}, {value=}")
            if match:
                args = list(match.groups())
                try:
                    result = value(request, *args)
                except Exception as ex:
                    result = Response(request.connection, response_code=503)
                print(f"Result to send: {result}")
                result.send()
                return
        result = Response(request, response_code=404)
        result.send()


def route(path):
    print("route_start", path)

    def route_func_wit_path(func):
        print("decor star")

        def handler(*args, **kwargs):
            return func(*args, **kwargs)

        print("register path")
        Dispatcher.add_route(path, handler)
        print("decor end")
        return handler

    print("route_end", path)
    return route_func_wit_path
