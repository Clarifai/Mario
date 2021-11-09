from enum import Enum
from typing import *

import kfp.dsl as dsl

__all__ = ["VolumeMode", "claim", "load"]


class VolumeMode(Enum):
    ReadOnlyMany = "r"
    ReadWriteMany = "rw"
    ReadWriteOnce = "rw1"


_enum_to_dsl_volume_mode = {
    VolumeMode.ReadOnlyMany: dsl.VOLUME_MODE_ROM,
    VolumeMode.ReadWriteMany: dsl.VOLUME_MODE_RWM,
    VolumeMode.ReadWriteOnce: dsl.VOLUME_MODE_RWO,
}


def claim(
    name: str, size: str, mode: Union[str, VolumeMode] = "rw", **kwargs
) -> dsl.PipelineVolume:

    if isinstance(mode, str):
        mode = VolumeMode(mode)
    assert isinstance(
        mode, VolumeMode
    ), "Argument `mode` must be an instance of `VolumeMode`."

    human_name = display_name = name
    resource_name = f"pvc-{name}-{size}"

    vop = dsl.VolumeOp(
        name=human_name,
        resource_name=resource_name,
        size=size,
        modes=_enum_to_dsl_volume_mode[mode],
        **kwargs,
    )

    vop.set_display_name(display_name)

    return vop.volume


def load(name: str, **kwargs) -> dsl.PipelineVolume:
    return dsl.PipelineVolume(pvc=name, **kwargs)
