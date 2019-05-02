BUILDERS = {
    'csv': 'text/csv',
    'html': 'text/html',
    'xml': 'application/xml',
    'json': 'application/json',
    'yaml': 'application/yaml',
    'base64': 'application/base64',
}


def set_default_config(app):
    app.config.setdefault('RB_DEFAULT_RESPONSE_FORMAT', BUILDERS['json'])
    app.config.setdefault('RB_DEFAULT_ENCODE', 'utf-8')
    app.config.setdefault('RB_DEFAULT_DUMP_INDENT', None)
    app.config.setdefault('RB_BASE64_ALTCHARS', None)
    app.config.setdefault('RB_HTML_DEFAULT_TEMPLATE', None)
    app.config.setdefault('RB_YAML_ALLOW_UNICODE', True)
    app.config.setdefault('RB_CSV_DEFAULT_NAME', 'filename')
    app.config.setdefault('RB_CSV_QUOTING', False)
    app.config.setdefault('RB_CSV_DELIMITER', ';')
    app.config.setdefault('RB_CSV_QUOTING_CHAR', '"')
    app.config.setdefault('RB_CSV_DIALECT', 'excel-tab')
    app.config.setdefault('RB_XML_CDATA', False)
    app.config.setdefault('RB_XML_ROOT', 'root')
    app.config.setdefault('RB_FLATTEN_PREFIX', '')
    app.config.setdefault('RB_FLATTEN_SEPARATOR', '_')
