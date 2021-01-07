Flask-ResponseBuilder
=====================

|download| |version|

Implementations of flask response in many formats: base64, csv, json, xml, html, yaml.
You can create your own builder extending ``Builder`` class and registering it with ``register_builder`` method.

Every builders are registered as attribute of ``ResponseBuilder`` class so you can invoke method from this class
with builder's name and it automatically create a response with that builder.

Also you can used ``Builder`` without response by invoking static methods: ``to_me``, ``to_dict``.

Based on PyYAML, xmltodict, dicttoxml. See their documentation for other options.

- Decorator for http response status ``204 NO_CONTENT``
- Response based on ``Accept`` header of request
- Response based on format parameter (query string)
- template_or_json: response based on xhr request (deprecated: works only with old js library)
- Support for case notation checker and converter, see ``Case`` utility class.
- ``Transformer``: utility class for data notation conversion

**NOTE**: From 2.1.11 the ``dicttoxml`` package seems to be abandoned, so a copy of module ``dicttoxml``
is ported in this package to fix deprecation warning, but if ``dicttoxml`` is installed it has priority.
In future will be removed and the internal module will be improved.

Quickstart
~~~~~~~~~~

Install ``flask_response_builder`` using ``pip``:

::

   $ pip install Flask-ResponseBuilder

Then import it into your project:

::

   $ from flask_response_builder import ResponseBuilder


.. _section-1:

Example usage
^^^^^^^^^^^^^

.. code:: python

    app = Flask(__name__)
    app.config['RB_HTML_DEFAULT_TEMPLATE'] = 'response.html'
    rb = ResponseBuilder(app)

    @app.route('/nocontent')
    @rb.no_content
    def nocontent():
        pass

    @app.route('/xhr')
    @rb.template_or_json('response.html')
    def test_xhr():
        return data

    @app.route('/onaccept')
    @rb.on_accept(acceptable=['application/json', 'application/xml'])
    def test_accept():
        return data

    @app.route('/format')
    @rb.on_format()
    def test_format():
        return data


For every registered builder you can explicitly use them in two ways:

.. code:: python

    @app.route('/decorator')
    @rb.response('json')
    def test_decorator():
        return data, 200, {'header': 'header'}

    @_app.route('/csv')
    def index_csv():
        builder = rb.csv(filename='file.csv')
        return builder((data, 200))


.. _section-2:

Configuration
^^^^^^^^^^^^^

    1.  ``RB_DEFAULT_RESPONSE_FORMAT``: *(default: 'application/json')*
    2.  ``RB_DEFAULT_ACCEPTABLE_MIMETYPES``: *(default: a list of all supported mimetypes)*
    3.  ``RB_DEFAULT_ENCODE``: *(default: 'utf-8')*
    4.  ``RB_DEFAULT_DUMP_INDENT``: *(default: None)*
    5.  ``RB_FORMAT_KEY``: *(default: 'format')*
    6.  ``RB_BASE64_ALTCHARS``: *(default: None)*
    7.  ``RB_HTML_DEFAULT_TEMPLATE``: *(default: None)*
    8.  ``RB_HTML_AS_TABLE``: *(default: True)*
    9.  ``RB_YAML_ALLOW_UNICODE``: *(default: True)*
    10. ``RB_CSV_DEFAULT_NAME``: *(default: 'filename')*
    11. ``RB_CSV_DELIMITER``: *(default: ';')*
    12. ``RB_CSV_QUOTING_CHAR``: *(default: '"')*
    13. ``RB_CSV_DIALECT``: *(default: 'excel-tab')*
    14. ``RB_XML_CDATA``: *(default: False)*
    15. ``RB_XML_ROOT``: *(default: 'ROOT')*
    16. ``RB_FLATTEN_PREFIX``: *(default: '')*
    17. ``RB_FLATTEN_SEPARATOR``: *(default: '_')*
    18. ``RB_JSONP_PARAM``: *(default: 'callback')* if empty or None jsonp is disabled

License MIT

.. |download| image:: https://pypip.in/download/flask_responsebuilder/badge.png
.. |version| image:: https://pypip.in/version/flask_responsebuilder/badge.png
