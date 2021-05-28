import kfp
from typing import *

__all__ = ["script"]


def script(function: Callable, filename: str, **kwargs) -> None:
    """Turn node Callable class to pipeline function."""
    name = function.__name__
    description = function.__doc__

    tmp = kfp.dsl.pipeline(name=name, description=description)(function)

    kfp.compiler.Compiler().compile(tmp, filename, **kwargs)
