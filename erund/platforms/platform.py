from asyncinit import asyncinit


@asyncinit
class Platform:
    async def __init__(self, id_):
        self.id = id_  # pylint: disable=invalid-name

    async def shutdown(self):
        pass
