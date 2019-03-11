from erund.utils import ssh, cmd
from erund import utils
from .platform import LinuxPlatform

DOCKER = ['docker']


class Docker(LinuxPlatform):
    async def __init__(self, id_, hostuser, host, image, command):
        await super().__init__(id_, hostuser)
        self.host = host
        self.image = image
        self.command = command

    async def check_docker(self):
        proc = await ssh(self.host, DOCKER + ['-v'])
        await proc.communicate()
        if proc.returncode != 0:
            self.logger.ERROR("Docker not installed")
            return False

        return True

    async def check_image(self):
        proc = await ssh(self.host, DOCKER + ['images', '-q', self.image])
        stdout, stderr = await proc.communicate()
        if stdout == "":
            self.logger.INFO("Docker image not downloaded")

            proc = await ssh(self.host, DOCKER + ['pull', self.image])
            await proc.communicate()
            if proc.returncode != 0:
                self.logger.ERROR("Could not download docker image")
                return False
        return True

    async def run(self):
        r = await ssh(self.host, DOCKER + ['run', '--name', self.id, self.image, self.command], rcwd=self.rcwd)
        print(await r.communicate())

    async def kill(self):
        await ssh(self.host, DOCKER + ['kill', self.id])

    async def deploy(self):
        print("Deploy")
        if await self.check_docker():
            self.upload()
