from flask import Response
from flask import render_template

from flask_response_builder import to_flatten

from . import Builder


class HtmlBuilder(Builder):
    def build(self, data, headers=None, status=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :return:
        """
        as_table = kwargs.get('as_table')
        template = kwargs.get('template')

        if as_table is None:
            as_table = self._conf.get('RB_HTML_AS_TABLE')

        if as_table is True:
            data = to_flatten(
                data or [],
                to_dict=kwargs.get('to_dict'),
                parent_key=self._conf.get('RB_FLATTEN_PREFIX'),
                sep=self._conf.get('RB_FLATTEN_SEPARATOR')
            )

        return Response(
            render_template(
                template or self._conf.get('RB_HTML_DEFAULT_TEMPLATE'),
                data=data or {},
                **kwargs
            ),
            status=status,
            headers=headers
        )
