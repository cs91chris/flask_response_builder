from collections import MutableMapping


def rename_keys(data, trans=None, **kwargs):
    """

    :param data:
    :param trans:
    :param kwargs:
    """
    if trans is None:
        for k, v in kwargs.items():
            data[v] = data.pop(k)
    else:
        for k in list(data.keys()):
            data[trans(k)] = data.pop(k)


def to_flatten(data, to_dict=None, **kwargs):
    """

    :param data:
    :param to_dict:
    :return:
    """
    def _flatten_dict(d, parent_key='', sep='_'):
        """

        :param d:
        :param parent_key:
        :param sep:
        :return:
        """
        items = []

        for k, v in d.items():
            nk = (parent_key + sep + k) if parent_key else k

            if isinstance(v, MutableMapping):
                fdict = _flatten_dict(v, nk, sep=sep)
                items.extend(fdict.items())
            else:
                items.append((nk, v))
        return dict(items)

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
