from flask.json import dumps
from flask.json import loads

from . import Builder


class JsonBuilder(Builder):
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
        return dumps(data, **kwargs)

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
        return loads(data, **kwargs)
