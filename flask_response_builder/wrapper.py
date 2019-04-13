from functools import wraps

from flask import Response
from flask import make_response

from .transformers import Transformer


def no_content():
    """

    :return:
    """
    resp = make_response('', 204)
    del resp.headers['Content-Type']
    del resp.headers['Content-Length']
    return resp


def no_content_response(func):
    """

    :param func:
    :return:
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        func(*args, **kwargs)
        return no_content()
    return wrapped


def created(data: dict, headers=None):
    """

    :param data:
    :param headers:
    :return:
    """
    return Response(
        Transformer.dict_to_json(data),
        status=201,
        mimetype='application/json',
        headers={
            'Content-Type': 'application/json',
            **(headers or {})
        }
    )


def created_response(func):
    """

    :param func:
    :return:
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        data, headers = func(*args, **kwargs)
        return created(data, headers)
    return wrapped
