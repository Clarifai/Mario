from .compute import Compute

__all__ = ["Component"]


class Component(Compute):
    @classmethod
    def from_component_yaml(cls, path_to_file):
        pass
