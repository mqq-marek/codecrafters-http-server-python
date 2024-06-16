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
        for key, value in cls.routes.items():
            match = re.fullmatch(key, cmd_path)
            if match:
                args = list(match.groups())
                try:
                    result = value(request, *args)
                except Exception as ex:
                    result = Response(request, response_code=503)
                result.send()
                return
        result = Response(request, response_code=404)
        result.send()


def route(path):

    def route_func_wit_path(func):
        def handler(*args, **kwargs):
            return func(*args, **kwargs)

        Dispatcher.add_route(path, handler)
        return handler

    return route_func_wit_path
