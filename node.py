import os
import sys
from fifo import fifo
import subprocess

if __name__ == '__main__':
    node = os.getenv('NODE', 'test')
    print(f'Currnet Node Name : {node}')
    ff = fifo('./shared/' + node)
    while True:
        cmd = ff.recv_req()
        result = os.popen(cmd).read()
        ff.send_res(result)
