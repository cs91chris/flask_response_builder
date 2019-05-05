from flask import Response

from flask_response_builder.dictutils import to_flatten

from . import Builder
from . import Transformer


class CsvBuilder(Builder):
    def build(self, data, headers=None, status=None, **kwargs):
        """

        :param data:
        :param headers:
        :param status:
        :return:
        """
        filename = kwargs.get('filename')

        data = to_flatten(
            data or [],
            to_dict=kwargs.get('to_dict'),
            parent_key=self._conf.get('RB_FLATTEN_PREFIX'),
            sep=self._conf.get('RB_FLATTEN_SEPARATOR')
        )

        return Response(
            Transformer.list_to_csv(
                data or [],
                delimiter=self._conf.get('RB_CSV_DELIMITER'),
                quotechar=self._conf.get('RB_CSV_QUOTING_CHAR'),
                dialect=self._conf.get('RB_CSV_DIALECT'),
                **kwargs
            ),
            mimetype=self.mimetype,
            status=status or 200,
            headers={
                'Content-Type': self.mimetype,
                'Total-Rows': len(data),
                'Total-Columns': len(data[0].keys()),
                'Content-Disposition': 'attachment; filename=%s.csv' % (
                    filename or self._conf.get('RB_CSV_DEFAULT_NAME'),
                ),
                **(headers or {})
            }
        )
