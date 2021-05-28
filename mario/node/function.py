from .base import Node
from typing import *
import kfp.dsl as dsl


class FunctionNode(Node):
    def __init__(
        self,
        name: str,
        image: str,
        mount_point_to_volumes: Optional[Dict[str, dsl.PipelineVolume]] = None,
        command: Optional[Union[str, List[str]]] = None,
    ):
        super().__init__()
        self.name = name
        self.image = image
        self.command = command
        self.volume_name_to_mount_point = {}
        self._mnt_to_vol = {}
        if mount_point_to_volumes:
            self._add_volume(mount_point_to_volumes)

    def _add_volume(self, mount_point_to_volumes: Dict[str, dsl.PipelineVolume]):

        for mount_point, pvc in mount_point_to_volumes.items():
            self.volume_name_to_mount_point[pvc.name] = mount_point
            self._mnt_to_vol[mount_point] = pvc
            setattr(self, pvc.name, pvc)

    def __call__(self, **kwargs):

        arglist = []
        for key, value in kwargs.items():
            arglist.append(f"--{key}")
            arglist.append(value)

        self._container_op = dsl.ContainerOp(
            name=self.name,
            image=self.image,
            command=self.command,
            arguments=arglist,
            pvolumes=self._mnt_to_vol,
        )

    def __getitem__(self, mount_point: str) -> dsl.PipelineVolume:
        if not hasattr(self, "_container_op"):
            raise AttributeError(f"Mount point {mount_point} has not been mounted.")

        return self._container_op.pvolumes[mount_point]

    def __setitem__(self, mount_point: str, volume: dsl.PipelineVolume) -> None:

        self._add_volume({mount_point: volume})

    def __len__(self):
        return len(self.volumes)
