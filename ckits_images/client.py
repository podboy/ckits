# coding:utf-8

from os.path import exists
from typing import Optional
from typing import Union

from docker import DockerClient
from podman import PodmanClient

from ckits_images.tags import TAG
from ckits_images.tags import Tag

CLIENT = Union[DockerClient, PodmanClient]


class UnifiedClient:
    DOCKER: str = "/var/run/docker.sock"
    PODMAN: str = "/run/podman/podman.sock"

    def __init__(self, client: Optional[CLIENT] = None):
        self.__client: Optional[CLIENT] = client

    def __del__(self):
        if self.__client is not None:
            self.__client.close()

    def __enter__(self) -> "UnifiedClient":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.__client is not None:
            self.__client.close()
            self.__client = None

    @property
    def client(self) -> CLIENT:
        assert self.__client is not None, "Client is not initialized"
        return self.__client

    def retag(self, old: TAG, new: TAG) -> bool:
        return self.client.images.get(Tag.parse(old).name).tag(Tag.parse(new).name)  # noqa:E501

    def pull(self, tag: TAG):
        return self.client.images.pull(Tag.parse(tag).name, all_tags=False)

    def pull_all_tags(self, tag: TAG):
        return self.client.images.pull(Tag.parse(tag).name, all_tags=True)

    def push(self, tag: TAG):
        self.client.images.push(Tag.parse(tag).name)

    def transport(self, src_tag: TAG, dst_tag: TAG) -> bool:
        src: Tag = Tag.parse(src_tag)
        dst: Tag = Tag.parse(dst_tag)
        self.pull(src)
        if not self.retag(src, dst):
            return False
        self.push(dst)
        return True

    @classmethod
    def create_docker(cls) -> "UnifiedClient":
        assert exists(cls.DOCKER), "Docker socket not found"
        return cls(DockerClient(base_url=f"unix://{cls.DOCKER}"))

    @classmethod
    def create_podman(cls) -> "UnifiedClient":
        assert exists(cls.PODMAN), "Podman socket not found"
        return cls(PodmanClient(base_url=f"unix://{cls.PODMAN}"))

    @classmethod
    def create(cls) -> "UnifiedClient":
        if exists(cls.DOCKER):
            return cls.create_docker()

        if exists(cls.PODMAN):
            return cls.create_podman()

        raise FileNotFoundError("Docker or Podman socket not found")
