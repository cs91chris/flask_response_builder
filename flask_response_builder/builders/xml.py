from flask import Response

from . import Builder
from . import Transformer


class XmlBuilder(Builder):
    def build(self, data, headers=None, status=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :return:
        """
        root = kwargs.get('root')

        return Response(
            Transformer.dict_to_xml(
                data or {},
                custom_root=root or self._conf.get('RB_XML_ROOT'),
                cdata=self._conf.get('RB_XML_CDATA'),
                **kwargs
            ),
            mimetype=self.mimetype,
            status=status or 200,
            headers={
                'Content-Type': self.mimetype,
                **(headers or {})
            }
        )
