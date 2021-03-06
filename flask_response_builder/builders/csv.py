import csv
import io

from flask_response_builder.dictutils import to_flatten
from .builder import Builder


class CsvBuilder(Builder):
    def _build(self, data, **kwargs):
        """

        :param data:
        :return:
        """
        data = to_flatten(
            data or [],
            to_dict=kwargs.pop('to_dict', None),
            parent_key=self.conf.get('RB_FLATTEN_PREFIX', ''),
            sep=self.conf.get('RB_FLATTEN_SEPARATOR', '')
        )

        self._headers.update({
            'Total-Rows':          len(data),
            'Total-Columns':       len(data[0].keys()),
            'Content-Disposition': 'attachment; filename=%s.csv' % (
                kwargs.pop('filename', self.conf.get('RB_CSV_DEFAULT_NAME')),
            )
        })

        delimiter = self.conf.get('RB_CSV_DELIMITER')
        if delimiter:
            kwargs.update(dict(delimiter=delimiter))

        quotechar = self.conf.get('RB_CSV_QUOTING_CHAR')
        if quotechar:
            kwargs.update(dict(quotechar=quotechar))

        dialect = self.conf.get('RB_CSV_DIALECT')
        if dialect:
            kwargs.update(dict(dialect=dialect))

        return self.to_csv(
            data or [],
            **kwargs
        )

    @staticmethod
    def to_me(data: list, **kwargs):
        """

        :param data:
        :return:
        """
        kwargs.setdefault('dialect', 'excel-tab')
        kwargs.setdefault('delimiter', ';')
        kwargs.setdefault('quotechar', '"')
        kwargs.setdefault('quoting', csv.QUOTE_ALL)

        output = io.StringIO()
        w = csv.DictWriter(output, data[0].keys() if data else '', **kwargs)
        w.writeheader()
        w.writerows(data)

        return output.getvalue()

    @staticmethod
    def to_csv(data, **kwargs):
        """

        :param data:
        :return:
        """
        return CsvBuilder.to_me(data, **kwargs)

    @staticmethod
    def to_dict(data, **kwargs):
        """

        :param data:
        :return:
        """
        kwargs.setdefault('dialect', 'excel-tab')
        kwargs.setdefault('delimiter', ';')
        kwargs.setdefault('quotechar', '"')
        kwargs.setdefault('quoting', csv.QUOTE_ALL)

        return [
            r for r in csv.DictReader(io.StringIO(data), **kwargs)
        ]
