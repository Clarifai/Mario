import kfp.dsl as dsl
from typing import *


class Node:

    repr_indent: int = 4
    _volume_registry: Dict[str, dsl.PipelineVolume]

    def __init__(self) -> None:
        self._volume_registry = {}

    def flow(self):
        raise NotImplementedError(f"Method `flow` is not implemented.")

    def __setattr__(self, key: str, value: Any) -> None:
        if isinstance(value, dsl.PipelineVolume):
            if hasattr(self, "_volume_registry"):
                object.__setattr__(self, key, value)
                self._volume_registry[key] = value
            else:
                raise AttributeError("Volumes must be added in `__init__`.")
        else:
            object.__setattr__(self, key, value)

    def __delattr__(self, key) -> None:
        if key in self._volume_registry:
            del self._volume_registry[key]
        object.__delattr__(self, key)

    def __call__(self, *args, **kwargs) -> Any:
        return self.flow(*args, **kwargs)

    def extra_repr(self) -> List[str]:
        return []

    def __repr__(self) -> str:
        lines = []
        lines.append(f"{self.__class__.__name__}:")
        lines.append(" " * self.repr_indent + f"registered volumes:")
        for key, value in self._volume_registry.items():
            lines.append(" " * 2 * self.repr_indent + f"* {key}")
        for key, value in self.__dict__.items():
            if key.startswith("_") or key in self._volume_registry:
                continue
            lines.append(" " * self.repr_indent + f"{key}: {value}")
        lines.extend(self.extra_repr)

        return "\n".join(lines)
