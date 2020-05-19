import uuid
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum

from flask import json

try:
    # noinspection PyUnresolvedReferences
    from bson import ObjectId
    object_id = ObjectId
except ImportError:
    object_id = str


class SetsEncoderMixin(json.JSONEncoder):
    """
        Encoders for: set, frozenset
    """
    def default(self, o, *args, **kwargs):
        if isinstance(o, (set, frozenset)):
            return list(o)

        return super().default(o)


class BytesEncoderMixin(json.JSONEncoder):
    """
    Encoders for: bytes, bytearray
    """
    def default(self, o, *args, **kwargs):
        if isinstance(o, (bytes, bytearray)):
            return o.decode()

        return super().default(o)


class BuiltinEncoderMixin(BytesEncoderMixin, SetsEncoderMixin):
    """
        Encoders for: Enum, Decimal
        Extends: BytesEncoderMixin, SetsEncoderMixin
    """
    def default(self, o, *args, **kwargs):
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, Decimal):
            return float(o)

        return super().default(o)


class DateTimeEncoderMixin(json.JSONEncoder):
    """
    Encoders for: datetime, date, time, timedelta
    """
    def default(self, o, *args, **kwargs):
        if isinstance(o, (datetime, date, time)):
            return o.isoformat()
        if isinstance(o, timedelta):
            return o.total_seconds()

        return super().default(o)


class ExtraEncoderMixin(json.JSONEncoder):
    """
    Encoders for: UUID, ObjectId
    """
    def default(self, o, *args, **kwargs):
        if isinstance(o, uuid.UUID):
            return o.hex
        if isinstance(o, object_id):
            return str(o)

        return super().default(o)


class JsonEncoder(
    BuiltinEncoderMixin,
    DateTimeEncoderMixin,
    ExtraEncoderMixin
):
    """
    Extends all encoders provided with this module
    """
    def default(self, o, *args, **kwargs):
        return super().default(o)
