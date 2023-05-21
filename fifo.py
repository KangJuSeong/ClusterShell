import os
import aiofiles


class fifo:
    def __init__(self, name):
        self.req = name + '_req'
        self.res = name + '_res'
        if not os.path.exists(self.req):
            os.mkfifo(self.req)
        if not os.path.exists(self.res):
            os.mkfifo(self.res)
    
    async def send_req(self, cmd):
        f = await aiofiles.open(self.req, 'w')
        await f.write(cmd)
        await f.close()

    async def recv_req(self):
        f = await aiofiles.open(self.req, 'r')
        data = await f.read()
        await f.close()
        return data

    async def send_res(self, result):
        f = await aiofiles.open(self.res, 'w')
        await f.write(result)
        await f.close()

    async def recv_res(self):
        f = await aiofiles.open(self.res, 'r')
        result = await f.read()
        await f.close()
        return result
