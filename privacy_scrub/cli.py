import click
from PIL import Image
import os

VERSION = "0.1.0"

def print_welcome():
    click.secho("Welcome to your_project interactive mode", fg="cyan", bold=True)
    click.echo("Type 'help' for available commands. Type 'exit' to quit.\n")

@click.group(invoke_without_command=True)
@click.version_option(VERSION)
@click.pass_context
def main(ctx):
    """
    🚀 your_project CLI

    Available Commands:
      greet  👋 Print a greeting
      load   📷 Load and validate an image file
      repl   🧪 Start an interactive shell
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@main.command(
    help="Greet someone by name.\n\nExample: greet Alice"
)
@click.argument("name")
def greet(name):
    """👋 Print a greeting"""
    click.secho(f"Hello, {name}!", fg="green")

@main.command(
    help="Load and validate an image file.\n\nExample: load ./path/to/image.jpg"
)
@click.argument("filepath", type=click.Path(exists=True, readable=True))
def load(filepath):
    """📷 Load an image file from disk"""
    try:
        with Image.open(filepath) as img:
            img.verify()
        click.secho(f"Loaded image: {os.path.basename(filepath)}", fg="green")
    except Exception as e:
        click.secho(f"Failed to load image: {e}", fg="red", bold=True)

@main.command(
    help="Start an interactive shell for entering commands."
)
def repl():
    """🧪 Start an interactive shell"""
    print_welcome()
    while True:
        try:
            user_input = input("your-project > ").strip()
            if user_input in ("exit", "quit"):
                break
            elif user_input in ("help", "?"):
                click.echo(
                    "\nAvailable commands:\n"
                    "  greet NAME   - Greet someone by name\n"
                    "  load PATH    - Load an image file\n"
                    "  exit         - Exit interactive mode\n"
                )
            elif user_input.startswith("greet "):
                name = user_input.split(" ", 1)[1].strip()
                if name:
                    greet.callback(name)
                else:
                    click.secho("Usage: greet NAME", fg="yellow")
            elif user_input.startswith("load "):
                path = user_input.split(" ", 1)[1].strip()
                if os.path.isfile(path):
                    load.callback(path)
                else:
                    click.secho("File not found or unreadable.", fg="yellow")
            elif not user_input:
                continue
            else:
                click.secho("Unknown command. Type 'help' for options.", fg="red")
        except KeyboardInterrupt:
            click.echo("\nExiting...")
            break
        except Exception as e:
            click.secho(f"Error: {e}", fg="red", bold=True)
