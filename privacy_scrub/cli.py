import click

@click.group()
def main():
    """CLI for your_project"""
    pass

@main.command()
@click.argument("name")
def greet(name):
    """Print a greeting"""
    click.echo(f"Hello, {name}!")
