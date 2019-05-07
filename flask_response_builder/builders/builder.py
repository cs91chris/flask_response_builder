from abc import ABC
from abc import abstractmethod

from flask import Response


class Builder(ABC):
    def __init__(self, mimetype: str, response_class=None, **kwargs):
        """

        :param mimetype:
        :param response_class:
        """
        if not isinstance(mimetype, str):
            raise TypeError('Invalid mimetype: {}'.format(mimetype))

        if response_class and not isinstance(response_class, Response):
            raise TypeError('Invalid response_class: {}'.format(response_class))

        self.conf = kwargs
        self._mimetype = mimetype
        self._response_class = response_class or Response

        if not issubclass(self._response_class, Response):
            raise TypeError(
                "invalid '{}' class. You must extend flask Response class".format(str(self._response_class))
            )

        self._data = None
        self._headers = {
            'Content-Type': self.mimetype
        }

    @property
    def mimetype(self):
        """

        :return:
        """
        return self._mimetype

    @property
    def data(self):
        """

        :return:
        """
        return self._data

    @staticmethod
    @abstractmethod
    def to_dict(data, **kwargs):
        """

        :param data:
        :param kwargs:
        """
        pass

    @staticmethod
    @abstractmethod
    def to_me(data, **kwargs):
        """

        :param data:
        :param kwargs:
        """
        pass

    @abstractmethod
    def _build(self, data, **kwargs):
        """

        :param data:
        """
        pass

    def build(self, data, **kwargs):
        """

        :param data:
        :param kwargs:
        :return:
        """
        self._data = self._build(data, **kwargs)
        return self.data

    def response(self, status=None, headers=None):
        """

        :param status:
        :param headers:
        :return:
        """
        return self._response_class(
            self.data,
            mimetype=self.mimetype,
            status=status or 200,
            headers={
                **self._headers,
                **(headers or {})
            }
        )

    def transform(self, data, builder, inargs=None, outargs=None):
        """

        :param data:
        :param builder:
        :param inargs:
        :param outargs:
        :return:
        """
        _dict = builder.to_dict(data, **inargs)
        return self.build(_dict, **outargs)
