import asyncio
import socket
import re
import sh

SSH = ['ssh']
SCP = ['scp']


async def cmd(command, *args, **kwargs):
    if isinstance(command, list):
        command = ' '.join(command)
    print("Running command: ", command)
    return await asyncio.create_subprocess_shell(
        command, *args, **kwargs,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)


async def ssh(host, command, *args, user='root', rcwd=None, **kwargs):
    if isinstance(command, list):
        command = ' '.join(command)
    if rcwd is not None:
        command = f'cd {rcwd}; ' + command
    return await cmd(SSH + [f"{user}@{host}", f"'{command}'"], *args, **kwargs)


async def scp(fr, to, *args, **kwargs):
    return await cmd(SCP + [fr, to], *args, **kwargs)


async def iw_interfaces():
    stdout, _ = await (await cmd(['iw', 'dev'])).communicate()
    return [i.group(1) for i in (re.search(' *Interface (.*)', line) for line in stdout.decode('utf-8').splitlines()) if i]


async def myip(interface=None):
    if not interface:
        interface = (await iw_interfaces())[0]

    stdout, _ = await (await cmd(['ip', 'addr', 'show', interface])).communicate()
    ips = [i.group(1) for i in (re.search(' *inet ([^/ ]*)', line) for line in stdout.decode('utf-8').splitlines()) if i]
    return ips[0]

async def whoami():
    return (await (await cmd('whoami')).communicate())[0].decode('utf-8').strip()
