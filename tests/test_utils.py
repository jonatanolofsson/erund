import aiounittest
from erund import utils


class TestUtils(aiounittest.AsyncTestCase):

    async def test_iw_interfaces(self):
        ifaces = await utils.iw_interfaces()
        self.assertGreaterEqual(len(ifaces), 1)

    async def test_myip(self):
        ip = await utils.myip()
        self.assertNotEqual(ip, None)

    async def test_whoami(self):
        user = await utils.whoami()
        self.assertNotEqual(user, None)
