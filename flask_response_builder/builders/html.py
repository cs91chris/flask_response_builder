from flask import render_template

from .builder import Builder
from flask_response_builder.dictutils import to_flatten


class HtmlBuilder(Builder):
    def _build(self, data, **kwargs):
        """

        :param data:
        :return:
        """
        as_table = kwargs.pop('as_table', self.conf.get('RB_HTML_AS_TABLE'))

        parent_key = self.conf.get('RB_FLATTEN_PREFIX')
        if parent_key:
            kwargs.update(dict(parent_key=parent_key))

        sep = self.conf.get('RB_FLATTEN_SEPARATOR')
        if sep:
            kwargs.update(dict(sep=sep))

        if as_table is True:
            data = to_flatten(
                data or [],
                to_dict=kwargs.pop('to_dict', None)
            )

        kwargs.update(data=data)

        return render_template(
            kwargs.pop('template', self.conf.get('RB_HTML_DEFAULT_TEMPLATE')),
            **kwargs
        )

    @staticmethod
    def to_me(data, **kwargs):
        """

        :param data:
        :param kwargs:
        :return:
        """
        return None

    @staticmethod
    def to_dict(data, **kwargs):
        """

        :param data:
        :param kwargs:
        :return:
        """
        return None
