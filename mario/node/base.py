import warnings
from typing import *

import kfp.dsl as dsl

__all__ = ["Node"]


class Node:
    """Node: Base class for all kubeflow pipeline components"""

    repr_indent: int = 2
    _volume_registry: Dict[str, dsl.PipelineVolume]

    def __init__(self) -> None:
        self._volume_registry = {}
        self.__name__ = self.__class__.__name__

    def flow(self, **kwargs) -> Any:
        raise NotImplementedError("Method `flow` is not implemented.")

    def __call__(self, *args, **kwargs) -> Any:
        assert (
            len(args) == 0
        ), f"Only keyword args allowed in `__call__` but get args {args}."
        with warnings.catch_warnings():
            warnings.simplefilter(action="ignore", category=FutureWarning)
            return self.flow(**kwargs)

    def __setattr__(self, key: str, value: Any) -> None:
        if isinstance(value, dsl.PipelineVolume):
            if hasattr(self, "_volume_registry"):
                object.__setattr__(self, key, value)
                self._volume_registry[key] = value
            else:
                raise AttributeError("Volumes can be added after `__init__()`.")
        else:
            object.__setattr__(self, key, value)

    def __delattr__(self, key) -> None:
        if key in self._volume_registry:
            del self._volume_registry[key]
        object.__delattr__(self, key)

    def extra_repr(self) -> List[str]:
        return []

    def __repr__(self) -> str:
        lines = []
        lines.append(f"{self.__class__.__name__}:")
        lines.append(" " * self.repr_indent + "registered volumes:")
        for key, value in self._volume_registry.items():
            lines.append(" " * 2 * self.repr_indent + f"* {key}")
        for key, value in self.__dict__.items():
            if key.startswith("_") or key in self._volume_registry:
                continue
            if isinstance(value, Node):
                lines.append(" " * self.repr_indent + f"{key}:")
                for l in repr(value).split("\n"):
                    lines.append(" " * 2 * self.repr_indent + l)
            else:
                lines.append(" " * self.repr_indent + f"{key}: {value}")
        lines.extend(self.extra_repr())

        return "\n".join(lines)
