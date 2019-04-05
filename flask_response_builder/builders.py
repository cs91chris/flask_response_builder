from functools import wraps

from flask import abort
from flask import request
from flask import Response
from flask import render_template

from flask.json import dumps

from flask_response_builder import Transformer
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

    def on_format(self, default=None):
        """

        :param default:
        :return:
        """
        def response(fun):
            @wraps(fun)
            def wrapper(*args, **kwargs):
                fmt = request.args.get('format')
                if fmt not in BUILDERS.keys():
                    fmt = default or 'json'

                builder = getattr(self, fmt)
                resp = fun(*args, **kwargs)
                return builder(resp)

            return wrapper
        return response

    def on_accept(self, default=None):
        """

        :param default:
        :return:
        """
        def response(fun):
            @wraps(fun)
            def wrapper(*args, **kwargs):
                builder = None
                accept = request.headers.get('Accept')

                if accept == '*/*':
                    accept = default or self._app.config['RB_DEFAULT_RESPONSE_FORMAT']

                for k, v in BUILDERS.items():
                    if accept == v:
                        builder = getattr(self, k)
                        break

                if not builder:
                    abort(406, "Not Acceptable")

                resp = fun(*args, **kwargs)
                return builder(resp)

            return wrapper
        return response

    def template_or_json(self, template: str):
        """

        :param template:
        :return:
        """
        def response(fun):
            @wraps(fun)
            def wrapper(*args, **kwargs):
                resp = fun(*args, **kwargs)

                if request.is_xhr:
                    return self.json(resp)
                else:
                    return self.html(resp, template)
            return wrapper
        return response

    def base64(self, data, enc=None, ct=None, headers=None):
        """

        :param data:
        :param enc:
        :param ct:
        :param headers:
        :return:
        """
        return Response(
            Transformer.to_base64(
                str(data or ''),
                enc or self._app.config['RB_DEFAULT_ENCODE']
            ),
            mimetype=BUILDERS['base64'],
            headers={
                'Content-Type': ct or BUILDERS['base64'],
                **(headers or {})
            }
        )

    def csv(self, data: list, filename=None, headers=None):
        """

        :param data:
        :param filename:
        :param headers:
        :return:
        """
        return Response(
            Transformer.list_to_csv(
                data or [],
                quoting=self._app.config['RB_CSV_QUOTING'],
                delimiter=self._app.config['RB_CSV_DELIMITER'],
                qc=self._app.config['RB_CSV_QUOTING_CHAR'],
                dialect=self._app.config['RB_CSV_DIALECT']
            ),
            mimetype=BUILDERS['csv'],
            headers={
                'Content-Type': BUILDERS['csv'],
                'Content-Disposition': 'attachment; filename=%s.csv' % (
                    filename or self._app.config['RB_CSV_DEFAULT_NAME'],
                ),
                **(headers or {})
            }
        )

    def xml(self, data: dict, root=None, headers=None):
        """

        :param data:
        :param root:
        :param headers:
        :return:
        """
        return Response(
            Transformer.dict_to_xml(
                data or {},
                root or self._app.config['RB_XML_ROOT'],
                cdata=self._app.config['RB_XML_CDATA']
            ),
            mimetype=BUILDERS['xml'],
            headers={
                'Content-Type': BUILDERS['xml'],
                **(headers or {})
            }
        )

    def json(self, data: dict, headers=None):
        """

        :param data:
        :param headers:
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
                separators=separators
            ),
            mimetype=BUILDERS['json'],
            headers={
                'Content-Type': BUILDERS['json'],
                **(headers or {})
            }
        )

    def yaml(self, data: dict, unicode=None, headers=None):
        """

        :param data:
        :param unicode:
        :param headers:
        :return:
        """
        indent = self._app.config['RB_DEFAULT_DUMP_INDENT'] if self._app.debug else None
        unicode = unicode or self._app.config['RB_YAML_ALLOW_UNICODE']

        return Response(
            Transformer.dict_to_yaml(
                data or {},
                indent=indent,
                allow_unicode=unicode
            ),
            mimetype=BUILDERS['yaml'],
            headers={
                'Content-Type': BUILDERS['yaml'],
                **(headers or {})
            }
        )

    def html(self, data: list, template=None, **kwargs):
        """

        :param data:
        :param template:
        :return:
        """
        return Response(
            render_template(
                template or self._app.config['RB_HTML_DEFAULT_TEMPLATE'],
                data=data, **kwargs
            )
        )

    def response(self, fmt: str, **kwargs):
        """
        :param fmt:
        :return:
        """
        builder_list = [k for k in BUILDERS.keys()]
        if fmt not in builder_list:
            raise NameError("Builder not found: using one of: {}".format(builder_list))

        def _response(f):
            @wraps(f)
            def wrapper(*args, **kw):
                resp = f(*args, **kw)
                builder = getattr(self, fmt)
                return builder(resp, **kwargs)
            return wrapper
        return _response
