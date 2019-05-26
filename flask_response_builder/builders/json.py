import uuid

from enum import Enum
from decimal import Decimal

from datetime import time
from datetime import date
from datetime import datetime
from datetime import timedelta

from flask import json

from . import Builder

try:
    from bson import ObjectId
    object_id = ObjectId
except ImportError:
    object_id = str


class JsonEncoder(json.JSONEncoder):
    def default(self, o, *args, **kwargs):
        if isinstance(o, (datetime, date, time)):
            return o.isoformat()
        if isinstance(o, timedelta):
            return o.total_seconds()
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, uuid.UUID):
            return o.hex
        if isinstance(o, object_id):
            return str(o)

        return super().default(o)


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
