"""Docker-related actions available to`bigtree`."""
from dataclasses import dataclass
import os
from pathlib import Path

import docker

# from docker.context import
from docker.client import ImageCollection

# from docker import DockerClient

from _bigtree.subtree import Subtree


@dataclass
class SubtreeDockData:
    images: ImageCollection


class SubtreeDock:
    """"""

    def __init__(self, subtree: Subtree) -> None:
        os.chdir(subtree.local_directory())
        client = docker.from_env()
        self._data = SubtreeDockData(
            images=client.images.list(),
        )

    @property
    def images(self):
        return self._data.images

    @property
    def tags(self):
        return self._data

    def image(self, name: str):
        return self._data.images.get(name)
