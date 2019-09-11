from asyncinit import asyncinit
from erund.utils import ssh, cmd, cmdout
from .platform import Platform
GIT = ['git']
RSYNC = ['rsync']


@asyncinit
class Linux(Platform):
    async def __init__(self, id_, hostuser, host, command):
        await super().__init__(id_)
        self.rcwd = f'/home/{hostuser}/{self.id}'
        self.hostuser = hostuser
        self.host = host
        self.command = command
        self.pidfile = f'{self.rcwd}/{self.id}.pid'

    async def upload(self):
        rootdir = await cmdout(GIT + ['rev-parse', '--show-toplevel'])
        res = await cmdout(RSYNC + ['-r', '-a', '-e', 'ssh', '--delete', '--exclude', 'build', '--exclude', 'devel', f'{rootdir}/', f'{self.hostuser}@{self.host}:{self.rcwd}/'])
        print(res)

    async def stop(self):
        res = await ssh(self.host, self.hostuser, f'if [ -f {self.pidfile} ]; then (pkill -F {self.pidfile} && rm {self.pidfile}); fi', rcwd=self.rcwd)
        print(res)
        return res

    async def run(self):
        await self.stop()
        command = self.command
        if isinstance(command, list):
            command = ' '.join(command)
        command = f"(({command}) & echo $! > {self.pidfile} &)"
        res = await ssh(self.host, self.hostuser, command, rcwd=self.rcwd)
        print(res)
        return res

