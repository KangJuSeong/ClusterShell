import os
import asyncio


class fifo:
    def __init__(self, name):
        self.req = name + '_req'
        self.res = name + '_res'
        if not os.path.exists(self.req):
            os.mkfifo(self.req)
        if not os.path.exists(self.res):
            os.mkfifo(self.res)
    
    async def send_req(self, cmd):
        with open(self.req, 'w') as f:
            f.write(cmd)

    def recv_req(self):
        with open(self.req, 'r') as f:
            data = f.read()
            return data

    def send_res(self, result):
        with open(self.res, 'w') as f:
            f.write(result)

    async def recv_res(self):
        with open(self.res, 'r') as f:
            result = f.read()
            return result
        
