import kfp
import kfp.dsl as dsl
from typing import *

__all__ = ["Node"]


class Node:

    repr_indent: int = 2
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
                raise AttributeError("Volumes can be added after `__init__()`.")
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
            if isinstance(value, Node):
                lines.append(" " * self.repr_indent + f"{key}:")
                for l in repr(value).split("\n"):
                    lines.append(" " * 2 * self.repr_indent + l)
            else:
                lines.append(" " * self.repr_indent + f"{key}: {value}")
        lines.extend(self.extra_repr())

        return "\n".join(lines)

    @classmethod
    def script(cls, **kwargs) -> Callable:
        if "name" not in kwargs:
            kwargs["name"] = cls.__class__.__name__

        if "description" not in kwargs:
            kwargs["description"] = cls.__doc__

        return kfp.dsl.pipeline(**kwargs)(cls)

    @classmethod
    def save(cls, filename, **kwargs) -> None:
        kfp.compiler.Compiler().compile(cls, filename, **kwargs)
