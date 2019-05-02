from decimal import Decimal
from datetime import datetime

from collections import MutableMapping


def _flatten_dict(d, parent_key='', sep='_'):
    """

    :param d:
    :param parent_key:
    :param sep:
    :return:
    """
    items = []

    for k, v in d.items():
        key = (parent_key + sep + k) if parent_key else k

        if isinstance(v, MutableMapping):
            items.extend(_flatten_dict(v, key, sep=sep).items())
        else:
            if isinstance(v, Decimal):
                v = float(v)
            elif isinstance(v, datetime):
                v = v.isoformat()

            items.append((key, v))
    return dict(items)


def to_flatten(data, to_dict=None, **kwargs):
    """

    :param data:
    :param to_dict:
    :return:
    """
    response = []
    to_dict = to_dict or (lambda x: dict(x))

    if not isinstance(data, (list, tuple)):
        data = (data,)

    for item in data:
        zipkeys = {}
        try:
            item = _flatten_dict(to_dict(item), **kwargs)
        except TypeError:
            raise TypeError("Could not convert '{}' into dict object, please provide a to_dict function")

        for key in list(item.keys()):
            if isinstance(item.get(key), list):
                if len(item.get(key)) > 0:
                    zipkeys.update({key: item.get(key)})
                    del item[key]

        for zk, value in zipkeys.items():
            for i in value:
                response.append({
                    **item,
                    **{"{}_{}".format(zk, k): v for k, v in i.items()}
                })

        if len(zipkeys.keys()) == 0:
            response.append(item)
    return response
