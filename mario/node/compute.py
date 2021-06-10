from typing import *

import kfp.dsl as dsl
import yaml

from .base import Node

__all__ = ["Compute"]


def _kwargs_to_arglist(
    arg_names: Union[List[str], Tuple[str]], arg_values: Dict[str, Any]
) -> List[Any]:
    arglist = []
    for name in arg_names:
        if name in arg_values:
            arglist.append(f"--{name}")
            value = arg_values.pop(name)
            if isinstance(value, (list, tuple)):
                arglist.extend([v for v in value])
            else:
                arglist.append(value)
    if len(arg_values) > 0:
        raise KeyError(
            f"Keyword(s) `{', '.join(key for key in arg_values)}` "
            f"did not match any given args `{', '.join(arg_names)}`"
        )
    return arglist


class Compute(Node):
    def __init__(
        self,
        name: str,
        image: str,
        mount_point_to_volumes: Optional[Dict[str, dsl.PipelineVolume]] = None,
        command: Optional[Union[str, List[str]]] = None,
        arg_names: Optional[Union[List[str], Tuple[str]]] = None,
    ):
        super().__init__()
        self.name = name
        self.image = image
        self.command = command
        self.arg_names = [] if arg_names is None else arg_names
        self.volume_name_to_mount_point = {}
        self._mnt_to_vol = {}
        if mount_point_to_volumes:
            self._add_volume(mount_point_to_volumes)

    def _add_volume(self, mount_point_to_volumes: Dict[str, dsl.PipelineVolume]):

        for mount_point, pvc in mount_point_to_volumes.items():
            self.volume_name_to_mount_point[pvc.name] = mount_point
            self._mnt_to_vol[mount_point] = pvc
            setattr(self, pvc.name, pvc)

    def flow(self, **kwargs):

        arglist = _kwargs_to_arglist(self.arg_names, kwargs)

        self._container_op = dsl.ContainerOp(
            name=self.name,
            image=self.image,
            command=self.command,
            arguments=arglist,
            pvolumes=self._mnt_to_vol,
        )

        return self._container_op

    @property
    def config(self):
        try:
            return self._container_op
        except AttributeError as e:
            raise RuntimeError(
                "Config handle has not been created. Please call the compute node first."
            ) from e

    def __getitem__(self, mount_point: str) -> dsl.PipelineVolume:
        if not hasattr(self, "_container_op"):
            raise AttributeError(f"Mount point {mount_point} has not been mounted.")

        return self._container_op.pvolumes[mount_point]

    def __setitem__(self, mount_point: str, volume: dsl.PipelineVolume) -> None:

        self._add_volume({mount_point: volume})

    def __len__(self):
        return len(self.volumes)

    @classmethod
    def from_component_yaml(cls, path_to_file: str) -> Node:
        comp = yaml.safe_load(open(path_to_file, "r").read())
        name = comp["name"]
        imag = comp["implementation"]["container"]["image"]
        args = [d["name"] for d in comp["inputs"]]
        cmnd = comp["implementation"]["container"]["command"]

        return cls(name=name, image=imag, command=cmnd, arg_names=args)

    def to_component_yaml(self, path_to_file: str):
        name = self.name
        image = self.image
        command = self.command
        arg_names = self.arg_names
        inputs = [{"name": a} for a in arg_names]
        args = _kwargs_to_arglist(arg_names, {a: {"inputValue": a} for a in arg_names})

        comp = {
            "name": name,
            "inputs": inputs,
            "implementation": {
                "container": {"image": image, "command": command, "args": args}
            },
        }

        yaml.safe_dump(comp, open(path_to_file, "w"))
