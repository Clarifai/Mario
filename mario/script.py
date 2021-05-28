import kfp
from typing import *
from .node import Node

__all__ = ["script"]


def script(node: Node, filename: str, **kwargs) -> Callable:
    """Turn node Callable class to pipeline function."""
    name = node.__class__.__name__
    description = node.__doc__

    tmp = kfp.dsl.pipeline(name=name, description=description)(node)

    kfp.compiler.Compiler().compile(tmp, filename, **kwargs)
