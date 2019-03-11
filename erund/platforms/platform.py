from asyncinit import asyncinit
from erund.utils import ssh, cmd

GIT = ['git']


@asyncinit
class Platform:
    async def __init__(self, id_):
        self.id = id_  # pylint: disable=invalid-name

    async def shutdown(self):
        pass


@asyncinit
class LinuxPlatform(Platform):
    async def __init__(self, id_, hostuser, *args, **kwargs):
        await super().__init__(id_, *args, **kwargs)
        self.rcwd = f'/home/{self.id}'
        self.hostuser = hostuser

    async def upload(self):
        mysha = (await (await cmd(GIT + ['rev-parse', 'HEAD'])).communicate())[0].decode('utf-8')
        await (await ssh(self.host, GIT + ['init', self.rcwd])).communicate()
        await (await cmd(GIT + ['push', f'ssh://{self.hostuser}@{self.host}{self.rcwd}', 'HEAD:refs/heads/{self.id}'])).communicate()
        await (await ssh(self.host, GIT + ['-C', self.rcwd, 'reset', '--hard'])).communicate()
        await (await ssh(self.host, GIT + ['-C', self.rcwd, 'clean', '-fdx', f'{self.host}/{self.rcwd}'])).communicate()
        await (await ssh(self.host, GIT + ['-C', self.rcwd, 'checkout', '--force', mysha])).communicate()
