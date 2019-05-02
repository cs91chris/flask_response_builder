import io
import csv
import yaml
import json
import base64
import xmltodict

from dicttoxml import dicttoxml

from yaml.parser import ParserError
from yaml.scanner import ScannerError


class Transformer:
    @staticmethod
    def to_base64(data, enc=None, altchars=None):
        """

        :param data:
        :param enc:
        :param altchars:
        :return:
        """
        return base64.b64encode(
            data.encode(enc),
            altchars=altchars
        ).decode()

    @staticmethod
    def from_base64(data: str, altchars=None):
        """

        :param data:
        :param altchars:
        :return:
        """
        return base64.b64decode(
            data,
            altchars=altchars
        )

    @staticmethod
    def list_to_csv(data: list, delimiter=';', quoting=True, qc='"', dialect='excel-tab'):
        """

        :param data:
        :param delimiter:
        :param quoting:
        :param qc:
        :param dialect:
        :return:
        """
        q = csv.QUOTE_ALL if quoting else csv.QUOTE_NONE
        output = io.StringIO()

        w = csv.DictWriter(
            output,
            data[0].keys() if data else '',
            dialect=dialect,
            delimiter=delimiter,
            quotechar=qc,
            quoting=q
        )
        w.writeheader()
        w.writerows(data)

        return output.getvalue()

    @staticmethod
    def csv_to_list(data: str):
        """

        :param data:
        :return:
        """
        return [
            dict(row) for row in csv.DictReader(io.StringIO(data))
        ]

    @staticmethod
    def dict_to_xml(data: dict, root='root', row='row', at=True, isup=True, cdata=False):
        """

        :param data:
        :param root:
        :param row:
        :param at:
        :param isup:
        :param cdata:
        :return:
        """
        return dicttoxml(
                data,
                custom_root=root.upper() if isup else root,
                item_func=lambda x: row.upper() if isup else row,
                attr_type=at,
                cdata=cdata
            )

    @staticmethod
    def xml_to_dict(data: str, pn=False):
        """

        :param data:
        :param pn:
        :return:
        """
        return xmltodict.parse(
            data,
            process_namespaces=pn
        )

    @staticmethod
    def dict_to_json(data: dict):
        """

        :param data:
        :return:
        """
        return json.dumps(data)

    @staticmethod
    def json_to_dict(data: str):
        """

        :param data:
        :return:
        """
        return json.loads(data)

    @staticmethod
    def dict_to_yaml(data: dict, indent=4, allow_unicode=True, **kwargs):
        """

        :param data:
        :param indent:
        :param allow_unicode:
        :param kwargs:
        :return:
        """
        return yaml.safe_dump(
            data,
            indent=indent,
            allow_unicode=allow_unicode,
            default_flow_style=False,
            **kwargs
        )

    @staticmethod
    def yaml_to_dict(data: str):
        """

        :param data:
        :return:
        """
        try:
            if isinstance(data, io.IOBase):
                return yaml.safe_load(data), ''
            else:
                return yaml.safe_load(io.StringIO(data)), ''
        except (ParserError, ScannerError) as exc:
            return None, str(exc)

    @staticmethod
    def json_to_xml(data: str):
        """

        :param data:
        :return:
        """
        return Transformer.dict_to_xml(
            Transformer.json_to_dict(str(data)) if isinstance(data, type(str)) else data
        )

    @staticmethod
    def xml_to_json(data: str):
        """

        :param data:
        :return:
        """
        return json.dumps(Transformer.xml_to_dict(data))

    @staticmethod
    def json_to_yaml(data):
        """

        :param data:
        :return:
        """
        return Transformer.dict_to_yaml(Transformer.json_to_dict(data))

    @staticmethod
    def yaml_to_json(data: str):
        """

        :param data:
        :return:
        """
        dictionary, error = Transformer.yaml_to_dict(data)
        return Transformer.dict_to_json(dictionary), error
