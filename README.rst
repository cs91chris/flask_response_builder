Flask-ResponseBuilder
=====================

Implementations of flask response in many formats: base64, csv, json, xml, html, yaml.

Based on PyYAML, xmltodict, dicttoxml. See their documentation for other options.

- Decorator for http response status ``204 NO_CONTENT``
- Response based on ``Accept`` header of request
- Response based on format parameter (query string)
- template_or_json: response based on xhr request
- Support for case notation checker and converter. See ``Case`` class

Quickstart
~~~~~~~~~~

Install ``flask_response_builder`` using ``pip``:

::

   $ pip install Flask-ResponseBuilder

Then import it into your project:

::

   $ from flask_response_builder import FlaskResponseBuilder


.. _section-1:

Example usage
^^^^^^^^^^^^^

For example usage see ``test.py`` file.

.. _section-2:

Configuration
^^^^^^^^^^^^^
    1.  ``RB_DEFAULT_RESPONSE_FORMAT``: *(default: application/json)*
    2.  ``RB_DEFAULT_ENCODE``: *(default: utf-8)*
    3.  ``RB_DEFAULT_DUMP_INDENT``: *(default: None)*
    4.  ``RB_BASE64_ALTCHARS``: *(default: None)*
    5.  ``RB_HTML_DEFAULT_TEMPLATE``: *(default: None)*
    6.  ``RB_YAML_ALLOW_UNICODE``: *(default: True)*
    7.  ``RB_CSV_DEFAULT_NAME``: *(default: filename)*
    8.  ``RB_CSV_QUOTING``: *(default: False)*
    9.  ``RB_CSV_DELIMITER``: *(default: ;)*
    10. ``RB_CSV_QUOTING_CHAR``: *(default: ")*
    11. ``RB_CSV_DIALECT``: *(default: excel-tab)*
    12. ``RB_XML_CDATA``: *(default: False)*
    13. ``RB_XML_ROOT``: *(default: ROOT)*
    14. ``RB_FLATTEN_PREFIX``: *(default: '')*
    15. ``RB_FLATTEN_SEPARATOR``: *(default: '_')*


License MIT
