from flask import Response

from . import Builder
from . import Transformer


class YamlBuilder(Builder):
    def build(self, data, headers=None, status=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :return:
        """
        if self._conf.get('DEBUG'):
            kwargs.setdefault('indent', self._conf.get('RB_DEFAULT_DUMP_INDENT'))
        kwargs.setdefault('allow_unicode', self._conf.get('RB_YAML_ALLOW_UNICODE'))

        return Response(
            Transformer.dict_to_yaml(
                data or {},
                **kwargs
            ),
            mimetype=self.mimetype,
            status=status or 200,
            headers={
                'Content-Type': self.mimetype,
                **(headers or {})
            }
        )
