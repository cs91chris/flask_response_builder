from .builder import Builder
from .transformers import Transformer

from .json import JsonBuilder
from .xml import XmlBuilder
from .csv import CsvBuilder
from .yaml import YamlBuilder
from .html import HtmlBuilder
from .base64 import Base64Builder


DEFAULT_BUILDERS = {
    'json': JsonBuilder,
    'xml': XmlBuilder,
    'csv': CsvBuilder,
    'yaml': YamlBuilder,
    'html': HtmlBuilder,
    'base64': Base64Builder,
}
