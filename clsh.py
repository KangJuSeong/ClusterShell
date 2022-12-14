import click


@click.command()
@click.option('-h')
def clsh(h):
    click.echo(h)