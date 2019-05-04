from functools import wraps

from flask import request
from flask import Response
from flask import make_response
from flask import render_template

from flask.json import dumps

from werkzeug.exceptions import NotAcceptable

from flask_response_builder import Transformer
from flask_response_builder.dictutils import to_flatten

from flask_response_builder.config import BUILDERS
from flask_response_builder.config import set_default_config


class FlaskResponseBuilder:
    def __init__(self, app=None):
        """

        :param app:
        """
        self._app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """

        :param app:
        """
        self._app = app
        set_default_config(app)

        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        app.extensions['response_builder'] = self

    @staticmethod
    def _build_response(data, resp, **kwargs):
        """

        :param data:
        :param resp:
        :return:
        """
        if isinstance(data, tuple):
            v = data + (None,) * (3 - len(data))
            data, status, headers = v if isinstance(v[1], int) else (v[0], v[2], v[1])
            return resp(data, headers=headers, status=status, **kwargs)
        else:
            return resp(data, **kwargs)

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
                fmt = request.args.get('format')

                if fmt not in (acceptable or BUILDERS.keys()):
                    fmt = default or 'json'

                builder = getattr(self, fmt)
                resp = fun(*args, **kwargs)
                return self._build_response(resp, builder)

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
                builder = None

                if request.accept_mimetypes is None or str(request.accept_mimetypes) == '*/*':
                    accept = default or self._app.config['RB_DEFAULT_RESPONSE_FORMAT']
                else:
                    mimetypes_list = acceptable or self._app.config['RB_DEFAULT_ACCEPTABLE_MIMETYPES']
                    accept = request.accept_mimetypes.best_match(mimetypes_list)

                for k, v in BUILDERS.items():
                    if accept == v:
                        builder = getattr(self, k)
                        break

                if not builder:
                    raise NotAcceptable('Not Acceptable: {}'.format(request.accept_mimetypes))

                resp = fun(*args, **kwargs)
                return self._build_response(resp, builder)
            return wrapper
        return response

    def response(self, fmt: str, **kwargs):
        """
        :param fmt:
        :return:
        """
        if fmt not in BUILDERS.keys():
            raise NameError("Builder not found: using one of: {}".format(BUILDERS.keys()))

        def _response(f):
            @wraps(f)
            def wrapper(*args, **kw):
                resp = f(*args, **kw)
                builder = getattr(self, fmt)
                return self._build_response(resp, builder, **kwargs)
            return wrapper
        return _response

    def template_or_json(self, template: str, as_table=False):
        """

        :param template:
        :param as_table:
        :return:
        """
        def response(fun):
            @wraps(fun)
            def wrapper(*args, **kwargs):
                resp = fun(*args, **kwargs)
                if request.is_xhr:
                    return self._build_response(resp, self.html, template=template, as_table=as_table)
                else:
                    return self._build_response(resp, self.json)
            return wrapper
        return response

    def base64(self, data, headers=None, status=None, enc=None, ct=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :param enc:
        :param ct:
        :return:
        """
        encoding = enc or self._app.config['RB_DEFAULT_ENCODE']
        return Response(
            Transformer.to_base64(str(data or ''), encoding, **kwargs),
            mimetype="{};{}".format(BUILDERS['base64'], encoding),
            status=status or 200,
            headers={
                'Content-Type': ct or BUILDERS['base64'],
                **(headers or {})
            }
        )

    def csv(self, data, headers=None, status=None, filename=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :param filename:
        :return:
        """
        data = to_flatten(
            data or [],
            parent_key=self._app.config['RB_FLATTEN_PREFIX'],
            sep=self._app.config['RB_FLATTEN_SEPARATOR']
        )

        return Response(
            Transformer.list_to_csv(
                data or [],
                delimiter=self._app.config['RB_CSV_DELIMITER'],
                quotechar=self._app.config['RB_CSV_QUOTING_CHAR'],
                dialect=self._app.config['RB_CSV_DIALECT'],
                **kwargs
            ),
            mimetype=BUILDERS['csv'],
            status=status or 200,
            headers={
                'Content-Type': BUILDERS['csv'],
                'Total-Rows': len(data),
                'Total-Columns': len(data[0].keys()),
                'Content-Disposition': 'attachment; filename=%s.csv' % (
                    filename or self._app.config['RB_CSV_DEFAULT_NAME'],
                ),
                **(headers or {})
            }
        )

    def xml(self, data, headers=None, status=None, root=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :param root:
        :return:
        """
        return Response(
            Transformer.dict_to_xml(
                data or {},
                custom_root=root or self._app.config['RB_XML_ROOT'],
                cdata=self._app.config['RB_XML_CDATA'],
                **kwargs
            ),
            mimetype=BUILDERS['xml'],
            status=status or 200,
            headers={
                'Content-Type': BUILDERS['xml'],
                **(headers or {})
            }
        )

    def json(self, data, headers=None, status=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :return:
        """
        if self._app.debug:
            indent = self._app.config['RB_DEFAULT_DUMP_INDENT']
            separators = (', ', ': ')
        else:
            indent = None
            separators = (',', ':')

        return Response(
            dumps(
                data or {},
                indent=indent,
                separators=separators,
                **kwargs
            ),
            mimetype=BUILDERS['json'],
            status=status or 200,
            headers={
                'Content-Type': BUILDERS['json'],
                **(headers or {})
            }
        )

    def yaml(self, data, headers=None, status=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :return:
        """
        kwargs.setdefault('indent', self._app.config['RB_DEFAULT_DUMP_INDENT'] if self._app.debug else None)
        kwargs.setdefault('allow_unicode', self._app.config['RB_YAML_ALLOW_UNICODE'])

        return Response(
            Transformer.dict_to_yaml(
                data or {},
                **kwargs
            ),
            mimetype=BUILDERS['yaml'],
            headers={
                'Content-Type': BUILDERS['yaml'],
                **(headers or {})
            },
            status=status or 200
        )

    def html(self, data, headers=None, status=None, template=None, as_table=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :param template:
        :param as_table:
        :return:
        """
        if as_table is None:
            as_table = self._app.config['RB_HTML_AS_TABLE']

        if as_table is True:
            data = to_flatten(
                data or [],
                parent_key=self._app.config['RB_FLATTEN_PREFIX'],
                sep=self._app.config['RB_FLATTEN_SEPARATOR']
            )

        return Response(
            render_template(
                template or self._app.config['RB_HTML_DEFAULT_TEMPLATE'],
                data=data or {},
                **kwargs
            ),
            status=status,
            headers=headers
        )
