from functools import wraps

from flask import request
from flask import make_response

from werkzeug.exceptions import NotAcceptable

from .config import DEFAULT_BUILDERS
from .config import set_default_config
from .builders import Builder


class ResponseBuilder:
    def __init__(self, app=None, builders=None):
        """

        :param app:
        :param builders:
        """
        self._builders = {}
        self._app = None
        if app is not None:
            self.init_app(app, builders)

    def init_app(self, app, builders=None):
        """

        :param app:
        :param builders:
        """
        self._app = app
        set_default_config(app)

        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        app.extensions['response_builder'] = self

        for name, builder in {**DEFAULT_BUILDERS, **(builders or {})}.items():
            self.register_builder(name, builder)

    def register_builder(self, name, builder):
        """

        :param name:
        :param builder:
        """
        if not issubclass(builder.__class__, Builder):
            raise NameError(
                "Invalid Builder: '{}'. You must extend class: '{}'".format(builder, Builder.__name__)
            )

        if builder.conf is None:
            builder.conf = self._app.config
        else:
            builder.conf.update(self._app.config)

        self._builders.update({name: builder})
        setattr(
            self, name,
            lambda d=None, b=name, **kv: self.build_response(b, d, **kv)
        )

    def build_response(self, builder, data, **kwargs):
        """

        :param builder:
        :param data:
        :return:
        """
        if isinstance(builder, str):
            builder = self._builders.get(builder)

        if builder is None:
            raise NameError("Builder not found: using one of: '{}'".format(self._builders.keys()))
        elif not issubclass(builder.__class__, Builder):
            raise NameError(
                "Invalid Builder: '{}'. You must extend class: '{}'".format(builder, Builder.__name__)
            )

        if isinstance(data, tuple):
            v = data + (None,) * (3 - len(data))
            data, status, headers = v if isinstance(v[1], int) else (v[0], v[2], v[1])
        else:
            status = headers = None

        builder.build(data, **kwargs)
        return builder.response(status=status, headers=headers)

    def get_mimetype_accept(self, default=None, acceptable=None):
        """

        :param default:
        :param acceptable:
        :return:
        """
        if not request.accept_mimetypes or str(request.accept_mimetypes) == '*/*':
            accept = default or self._app.config['RB_DEFAULT_RESPONSE_FORMAT']
        else:
            mimetypes_list = acceptable or self._app.config['RB_DEFAULT_ACCEPTABLE_MIMETYPES']
            accept = request.accept_mimetypes.best_match(mimetypes_list)

        for _, builder in self._builders.items():
            if accept == builder.mimetype:
                return accept, builder

        raise NotAcceptable('Not Acceptable: {}'.format(request.accept_mimetypes))

    @staticmethod
    def no_content(func):
        """

        :param func:
        :return:
        """
        @wraps(func)
        def wrapped(*args, **kwargs):
            func(*args, **kwargs)
            resp = make_response('', 204)
            del resp.headers['Content-Type']
            del resp.headers['Content-Length']
            return resp
        return wrapped

    def on_format(self, default=None, acceptable=None):
        """

        :param default:
        :param acceptable:
        :return:
        """
        def response(fun):
            @wraps(fun)
            def wrapper(*args, **kwargs):
                builder = request.args.get('format')
                if builder not in (acceptable or self._builders.keys()):
                    builder = default or 'json'

                return self.build_response(builder, fun(*args, **kwargs))
            return wrapper
        return response

    def on_accept(self, default=None, acceptable=None):
        """

        :param default:
        :param acceptable:
        :return:
        """
        def response(fun):
            @wraps(fun)
            def wrapper(*args, **kwargs):
                mimetype, builder = self.get_mimetype_accept(default, acceptable)
                return self.build_response(builder, fun(*args, **kwargs))
            return wrapper
        return response

    def response(self, builder, **kwargs):
        """
        :param builder:
        :return:
        """
        def _response(f):
            @wraps(f)
            def wrapper(*args, **kw):
                return self.build_response(builder, f(*args, **kw), **kwargs)
            return wrapper
        return _response

    def template_or_json(self, template: str, as_table=False, to_dict=None):
        """

        :param template:
        :param as_table:
        :param to_dict:
        :return:
        """
        def response(fun):
            @wraps(fun)
            def wrapper(*args, **kwargs):
                if request.is_xhr:
                    return self.build_response(
                        self._builders.get('html'),
                        fun(*args, **kwargs),
                        template=template,
                        as_table=as_table,
                        to_dict=to_dict
                    )
                else:
                    return self.build_response(self._builders.get('json'), fun(*args, **kwargs))
            return wrapper
        return response
