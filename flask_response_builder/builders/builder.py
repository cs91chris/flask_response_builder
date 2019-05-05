from abc import ABC
from abc import abstractmethod


class Builder(ABC):
    def __init__(self, mimetype: str, conf=None):
        """

        :param mimetype:
        :param conf:
        """
        self._conf = conf
        self._mimetype = mimetype

    @property
    def mimetype(self):
        """

        :return:
        """
        return self._mimetype

    @abstractmethod
    def build(self, data, **kwargs):
        """

        :param data:
        """
        pass
