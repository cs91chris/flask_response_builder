from functools import wraps

from flask import request
from flask import Response
from flask import render_template

from flask.json import dumps

from flask_response_builder import Transformer


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

        self._app.config.setdefault('RB_DEFAULT_ENCODE', 'utf-8')
        self._app.config.setdefault('RB_DEFAULT_DUMP_INDENT', None)
        self._app.config.setdefault('RB_BASE64_ALTCHARS', None)
        self._app.config.setdefault('RB_BASE64_CONTENT_TYPE', 'text/plain')
        self._app.config.setdefault('RB_HTML_DEFAULT_TEMPLATE', None)
        self._app.config.setdefault('RB_YAML_ALLOW_UNICODE', True)
        self._app.config.setdefault('RB_CSV_DEFAULT_NAME', 'filename')
        self._app.config.setdefault('RB_CSV_QUOTING', False)
        self._app.config.setdefault('RB_CSV_DELIMITER', ';')
        self._app.config.setdefault('RB_CSV_QUOTING_CHAR', '"')
        self._app.config.setdefault('RB_CSV_DIALECT', 'excel-tab')
        self._app.config.setdefault('RB_XML_CDATA', False)
        self._app.config.setdefault('RB_XML_ROOT', 'root')

        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        app.extensions['response_builder'] = self

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
                str(data),
                enc or self._app.config['RB_DEFAULT_ENCODE']
            ),
            mimetype='application/base64',
            headers={
                'Content-Type': ct or self._app.config['RB_BASE64_CONTENT_TYPE'],
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
                data,
                quoting=self._app.config['RB_CSV_QUOTING'],
                delimiter=self._app.config['RB_CSV_DELIMITER'],
                qc=self._app.config['RB_CSV_QUOTING_CHAR'],
                dialect=self._app.config['RB_CSV_DIALECT']
            ),
            mimetype='text/csv',
            headers={
                'Content-Type': 'text/csv',
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
                data,
                root or self._app.config['RB_XML_ROOT'],
                cdata=self._app.config['RB_XML_CDATA']
            ),
            mimetype='application/xml',
            headers={
                'Content-Type': 'application/xml',
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
                data,
                indent=indent,
                separators=separators
            ),
            mimetype='application/json',
            headers={
                'Content-Type': 'application/json',
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
                data,
                indent=indent,
                allow_unicode=unicode
            ),
            mimetype='application/base64',
            headers={
                'Content-Type': 'application/yaml',
                **(headers or {})
            }
        )

    def html(self, data: list, template=None, **kwargs):
        """

        :param template:
        :param data:
        :return:
        """
        return Response(
            render_template(
                template or self._app.config['RB_HTML_DEFAULT_TEMPLATE'],
                data=data, **kwargs
            )
        )
