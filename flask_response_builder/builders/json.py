from flask import Response
from flask.json import dumps

from . import Builder


class JsonBuilder(Builder):
    def build(self, data, headers=None, status=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :return:
        """
        if self._conf.get('DEBUG'):
            indent = self._conf.get('RB_DEFAULT_DUMP_INDENT')
            separators = (', ', ': ')
        else:
            indent = None
            separators = (',', ':')

        return Response(
            dumps(
                data or {},
                indent=indent,
                separators=separators,
                **kwargs
            ),
            mimetype=self.mimetype,
            status=status or 200,
            headers={
                'Content-Type': self.mimetype,
                **(headers or {})
            }
        )
