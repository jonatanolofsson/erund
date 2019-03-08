from asyncinit import asyncinit


@asyncinit
class Platform:
    async def __init__(self, id_):
        self.id = id_  # pylint: disable=invalid-name

    async def shutdown(self):
        pass


@asyncinit
class LinuxPlatform(Platform):
    async def __init__(self, workdir='.erund', *args, **kwargs):
        await super().__init__(*args, **kwargs)

    async def checkout(self):
        pass
