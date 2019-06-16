from flask import json

from .builder import Builder
from .encoders import JsonEncoder


class JsonBuilder(Builder):
    def __init__(self, mimetype: str, response_class=None, encoder=None, **kwargs):
        """

        :param mimetype:
        :param response_class:
        :param encoder:
        :param kwargs:
        """
        super().__init__(mimetype, response_class, **kwargs)
        self._encoder = encoder or JsonEncoder

    def _build(self, data, **kwargs):
        """

        :param data:
        :return:
        """
        if self.conf.get('DEBUG'):
            kwargs.setdefault('indent', self.conf.get('RB_DEFAULT_DUMP_INDENT'))
            kwargs.setdefault('separators', (', ', ': '))
        else:
            kwargs.setdefault('indent', None)
            kwargs.setdefault('separators', (',', ':'))

        kwargs.setdefault('cls', self._encoder)
        return self.to_json(
            data or {},
            **kwargs
        )

    @staticmethod
    def to_me(data: dict, **kwargs):
        """

        :param data:
        :return:
        """
        kwargs.setdefault('cls', JsonEncoder)
        return json.dumps(data, **kwargs)

    @staticmethod
    def to_json(data, **kwargs):
        """

        :param data:
        :return:
        """
        return JsonBuilder.to_me(data, **kwargs)

    @staticmethod
    def to_dict(data, **kwargs):
        """

        :param data:
        :return:
        """
        return json.loads(data, **kwargs)
