import kfp.dsl as dsl
import kubernetes as k8s
from .base import Node
from typing import *

__all__ = ["PullSecrets", "set_pull_secrets"]


def set_pull_secrets(pull_secrets: List[str]) -> None:
    """Sets pull secrets of the pipeline."""
    dsl.get_pipeline_conf().set_image_pull_secrets(
        [k8s.client.V1LocalObjectReference(name=secret) for secret in pull_secrets]
    )


class PullSecrets(Node):
    """Pull Secrets: Set pull secrets of the pipeline."""

    def __init__(self, *pull_secrets: str):
        super().__init__()
        self.pull_secrets = pull_secrets

    def flow(self) -> None:
        set_pull_secrets(self.pull_secrets)
