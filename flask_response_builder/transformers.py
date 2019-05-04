import io
import csv
import yaml
import json
import base64
import xmltodict

from dicttoxml import dicttoxml


class Transformer:
    @staticmethod
    def to_base64(data, enc=None, dec=True, **kwargs):
        """

        :param data:
        :param enc:
        :param dec:
        :return:
        """
        d = base64.b64encode(data.encode(enc), **kwargs)
        return d.decode() if dec is True else d

    @staticmethod
    def from_base64(data: str, **kwargs):
        """

        :param data:
        :return:
        """
        return base64.b64decode(data, **kwargs)

    @staticmethod
    def list_to_csv(data: list, **kwargs):
        """

        :param data:
        :return:
        """
        kwargs.setdefault('dialect', 'excel-tab')
        kwargs.setdefault('delimiter', ';')
        kwargs.setdefault('quotechar', '"')
        kwargs.setdefault('quoting', csv.QUOTE_ALL)

        output = io.StringIO()
        w = csv.DictWriter(output, data[0].keys() if data else '', **kwargs)
        w.writeheader()
        w.writerows(data)

        return output.getvalue()

    @staticmethod
    def csv_to_list(data: str, **kwargs):
        """

        :param data:
        :return:
        """
        return [
            dict(row) for row in csv.DictReader(io.StringIO(data), **kwargs)
        ]

    @staticmethod
    def dict_to_xml(data: dict, **kwargs):
        """

        :param data:
        :return:
        """
        kwargs.setdefault('item_func', lambda x: 'ROW')
        return dicttoxml(data, **kwargs)

    @staticmethod
    def xml_to_dict(data: str, **kwargs):
        """

        :param data:
        :return:
        """
        return xmltodict.parse(data, **kwargs)

    @staticmethod
    def dict_to_json(data: dict, **kwargs):
        """

        :param data:
        :return:
        """
        return json.dumps(data, **kwargs)

    @staticmethod
    def json_to_dict(data: str, **kwargs):
        """

        :param data:
        :return:
        """
        return json.loads(data, **kwargs)

    @staticmethod
    def dict_to_yaml(data: dict, **kwargs):
        """

        :param data:
        :param kwargs:
        :return:
        """
        kwargs.setdefault('indent', 4)
        kwargs.setdefault('allow_unicode', True)
        kwargs.setdefault('default_flow_style', False)

        return yaml.safe_dump(data, **kwargs)

    @staticmethod
    def yaml_to_dict(data: str, **kwargs):
        """

        :param data:
        :return:
        """
        if isinstance(data, io.IOBase):
            return yaml.safe_load(data)
        else:
            return yaml.safe_load(io.StringIO(data))

    @staticmethod
    def json_to_xml(data: str, json_args=None, xml_args=None):
        """

        :param data:
        :param json_args:
        :param xml_args:
        :return:
        """
        _dict = Transformer.json_to_dict(data, **(json_args or {}))
        return Transformer.dict_to_xml(_dict, **(xml_args or {}))

    @staticmethod
    def xml_to_json(data: str, xml_args=None, json_args=None):
        """

        :param data:
        :param xml_args:
        :param json_args:
        :return:
        """
        _dict = Transformer.xml_to_dict(data, **(xml_args or {}))
        return json.dumps(_dict, **(json_args or {}))

    @staticmethod
    def json_to_yaml(data: str, json_args=None, yaml_args=None):
        """

        :param data:
        :param json_args:
        :param yaml_args:
        :return:
        """
        _dict = Transformer.json_to_dict(data, **(json_args or {}))
        return Transformer.dict_to_yaml(_dict, **(yaml_args or {}))

    @staticmethod
    def yaml_to_json(data: str, yaml_args=None, json_args=None):
        """

        :param data:
        :param yaml_args:
        :param json_args:
        :return:
        """
        _dict = Transformer.yaml_to_dict(data, **(yaml_args or {}))
        return Transformer.dict_to_json(_dict, **(json_args or {}))

    @staticmethod
    def xml_to_yaml(data: str, xml_args=None, yaml_args=None):
        """

        :param data:
        :param xml_args:
        :param yaml_args:
        :return:
        """
        _dict = Transformer.xml_to_dict(data, **(xml_args or {}))
        return Transformer.dict_to_yaml(_dict, **(yaml_args or {}))

    @staticmethod
    def yaml_to_xml(data: str, yaml_args=None, xml_args=None):
        """

        :param data:
        :param yaml_args:
        :param xml_args:
        :return:
        """
        _dict = Transformer.yaml_to_dict(data, **(yaml_args or {}))
        return Transformer.dict_to_xml(_dict, **(xml_args or {}))
