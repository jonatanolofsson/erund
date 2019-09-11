from erund.utils import ssh, cmd
from erund import utils
from .linux import Linux

DOCKER = ['docker']


class Docker(Linux):
    async def __init__(self, id_, hostuser, host, command, image):
        await super().__init__(id_, hostuser, host, command)
        self.image = image

    async def check_docker(self):
        proc = await ssh(self.host, self.hostuser, DOCKER + ['-v'])
        await proc.communicate()
        if proc.returncode != 0:
            self.logger.ERROR("Docker not installed")
            return False

        return True

    async def check_image(self):
        proc = await ssh(self.host, self.hostuser, DOCKER + ['images', '-q', self.image])
        stdout, stderr = await proc.communicate()
        if stdout == "":
            self.logger.INFO("Docker image not downloaded")

            proc = await ssh(self.host, self.hostuser, DOCKER + ['pull', self.image])
            await proc.communicate()
            if proc.returncode != 0:
                self.logger.ERROR("Could not download docker image")
                return False
        return True

    async def run(self):
        await self.stop()
        return await ssh(
            self.host, self.hostuser,
            DOCKER + ['run', '--name', self.id,  # Name container
                      '-v', f'{self.rcwd}:{self.rcwd}',  # Mount workdir
                      f'-w="{self.rcwd}"',  # Set workdir
                      self.image, self.command], rcwd=self.rcwd)

    async def stop(self):
        await (await ssh(self.host, self.hostuser, DOCKER + ['stop', self.id])).communicate()

    async def deploy(self):
        if await self.check_docker():
            await self.upload()
        await self.run()
