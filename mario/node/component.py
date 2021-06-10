import yaml

from .compute import Compute

__all__ = ["Component"]


class Component(Compute):
    @classmethod
    def from_component_yaml(cls, path_to_file):
        comp = yaml.safe_load(open(path_to_file, "r").read())
        name = comp["name"]
        imag = comp["image"]
        args = [d["name"] for d in comp["inputs"]]
        cmnd = comp["implementation"]["command"]

        return cls(name=name, image=imag, command=cmnd, arg_names=args)
