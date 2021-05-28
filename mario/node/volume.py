from ..volume import *
from .base import Node
from typing import *


class VolumeNode(Node):
    """VolumeNode: Wrapper of VolumeOp"""

    def __init__(
        self, name: str, size: str, mode: Union[str, VolumeMode] = "rw", **kwargs
    ) -> None:
        super().__init__()
        self.name = name
        self.size = size
        self.mode = mode
        self._kwargs = kwargs
        self.volume = load("future_vol_placeholder")

    def flow(self) -> None:

        self.volume = claim(self.name, self.size, self.mode, **self._kwargs)
