from ..volume import *
from .base import Node
from typing import *
import kfp.dsl as dsl


class VolumeClaim(Node):
    """VolumeClaim: Wrapper of VolumeOp"""

    def __init__(
        self, name: str, size: str, mode: Union[str, VolumeMode] = "rw", **kwargs
    ) -> None:
        super().__init__()
        self.name = name
        self.size = size
        self.mode = mode
        self._kwargs = kwargs
        self.volume = None

    def flow(self) -> dsl.PipelineVolume:

        self.volume = claim(self.name, self.size, self.mode, **self._kwargs)

        return self.volume


class VolumeLoad(Node):
    """VolumeLoad: load existing volume"""

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__()
        self.name = name
        self._kwargs = kwargs
        self.volume = load(name, **kwargs)

    def flow(self) -> dsl.PipelineVolume:

        return self.volume
