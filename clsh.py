import click
import os
from fifo import fifo
from rich.table import Table
from rich import print
import asyncio


@click.command()
@click.option('-h')
@click.option('--hostfile')
@click.option('--out')
@click.argument('cmd', nargs=-1, type=click.Path())
def clsh(h, hostfile, out, cmd):
    nodes = list()
    data = ''
    if h:
        nodes = h.split(',')         
    if hostfile:
        with open(hostfile, 'r') as f:
            nodes = [node.strip() for node in f.readlines()]
    if not nodes:
        env1 = os.getenv('CLSH_HOSTS')
        if env1:
            print("[bold red]Note : use CLSH_HOSTS environment[bold red]")
            nodes = env1.split(':')
        env2 = os.getenv('CLSH_HOSTFILE')
        if env2 and not env1:
            print("[bold red]Note : use hostfile 'clusterfile' (CLSH_HOSTFILE env)[bold red]")
            with open(env2, 'r') as f:
                nodes = [node.strip() for node in f.readlines()]
        if not env1 and not env2 and os.path.exists('./hostfile'):
            print("[bold red]Note : use hostfile './hotfile' (default)[bold red]")
            with open('./hostfile') as f:
                nodes = [node.strip() for node in f.readlines()]
        if not env1 and not env2 and not os.path.exists('./hostfile'):
            print("[bold red]Note : No exist './hotfile'[bold red]")
            return

    print(f"[bold red]Note : Setting Nodes : {nodes}[bold red]")
    
    for c in cmd:
        data = data + c + ' '
    data = data[:-1]
    
    class async_fifo:
        def __init__(self, nodes_size):
            self.current = 0;
            self.stop = nodes_size

        def __aiter__(self):
            return self
        
        async def __anext__(self):
            if self.current < self.stop:
                ff = fifo(f'./shared/{nodes[self.current]}')
                await ff.send_req(data)
                res = await ff.recv_res()
                table = Table(show_header=True, header_style="bold red")
                table.add_column("Node", style="dim", width=12)
                table.add_column("Result", style="dim")
                table.add_row(nodes[self.current], res)
                if out:
                    with open(f"{out}/{nodes[self.current]}.out", 'w') as f:
                        f.write(res)
                print(table)
                self.current += 1
            else:
                raise StopAsyncIteration

    async def async_iter():
        async for i in async_fifo(len(nodes)):
            continue
        
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_iter())
    loop.close()
