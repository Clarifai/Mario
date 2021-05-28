from .base import Node
from typing import *
import kfp.dsl as dsl


def _kwargs_to_arglist(
    arg_names: Union[List[str], Tuple[str]], arg_values: Dict[str, Any]
) -> List[Any]:
    arglist = []
    for name in arg_names:
        if name in arg_values:
            arglist.append(f"--{name}")
            value = arg_values[name]
            if isinstance(value, (list, tuple)):
                arglist.extend([v for v in value])
            else:
                arglist.append(value)
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
        self.arg_names = arg_names
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

        arglist = _kwargs_to_arglist(self.arg_names, kwargs) if self.arg_names else None

        self._container_op = dsl.ContainerOp(
            name=self.name,
            image=self.image,
            command=self.command,
            arguments=arglist,
            pvolumes=self._mnt_to_vol,
        )

        return self._container_op

    def __getitem__(self, mount_point: str) -> dsl.PipelineVolume:
        if not hasattr(self, "_container_op"):
            raise AttributeError(f"Mount point {mount_point} has not been mounted.")

        return self._container_op.pvolumes[mount_point]

    def __setitem__(self, mount_point: str, volume: dsl.PipelineVolume) -> None:

        self._add_volume({mount_point: volume})

    def __len__(self):
        return len(self.volumes)
