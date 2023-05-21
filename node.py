import os
from fifo import fifo
import asyncio

async def main():
    node = os.getenv('NODE', 'test')
    print(f'Currnet Node Name : {node}')
    ff = fifo('./shared/' + node)
    while True:
        cmd = await ff.recv_req()
        result = os.popen(cmd).read()
        await ff.send_res(result)

asyncio.run(main())
