import os
import kfp
from typing import *


__all__ = ["save"]


def save(
    function: Callable, root: str = ".", filename: Optional[str] = None, **kwargs
) -> None:
    """Turn annotated Callable class to pipeline function."""
    name = function.__name__
    description = function.__doc__

    tmp = kfp.dsl.pipeline(name=name, description=description)(function)

    if not filename:
        filename = name.replace("_", "-") + ".yaml"

    filename = os.path.join(root, filename)

    kfp.compiler.Compiler().compile(tmp, filename, **kwargs)
