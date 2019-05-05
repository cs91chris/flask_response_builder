from flask import Response

from . import Builder
from . import Transformer


class Base64Builder(Builder):
    def build(self, data, headers=None, status=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :return:
        """
        encoding = kwargs.pop('enc') or self._conf.get('RB_DEFAULT_ENCODE')

        return Response(
            Transformer.to_base64(
                str(data or ''),
                encoding,
                **kwargs
            ),
            mimetype="{};{}".format(self.mimetype, encoding),
            status=status or 200,
            headers={
                'Content-Type': self.mimetype,
                **(headers or {})
            }
        )
