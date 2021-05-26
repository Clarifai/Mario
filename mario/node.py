import abc


class Node(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def __call__(self, **kwargs):
        pass
