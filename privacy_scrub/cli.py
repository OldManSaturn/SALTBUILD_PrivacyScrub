import click
from PIL import Image
import hashlib
import os

VERSION = "0.1.0"

def print_welcome():
    click.secho("Welcome to privacy_scrub interactive mode", fg="cyan", bold=True)
    click.echo("Type 'help' for available commands. Type 'exit' to quit.\n")

@click.group(invoke_without_command=True)
@click.version_option(VERSION)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@main.command(
    help="Greet someone by name.\n\nExample: greet Alice"
)
@click.argument("name")
def greet(name):
    click.secho(f"Hello, {name}!", fg="green")

@main.command(
    help="Load, validate, and hash an image file.\n\nExample: load ./path/to/image.jpg"
)
@click.argument("filepath", type=click.Path(exists=True, readable=True))
def load(filepath):
    try:
        with Image.open(filepath) as img:
            img.verify()  # Check image is valid

        # Compute hash
        with open(filepath, "rb") as f:
            data = f.read()
            sha256 = hashlib.sha256(data).hexdigest()

        click.secho(f"Loaded image: {os.path.basename(filepath)}", fg="green")
        click.secho(f"SHA-256: {sha256}", fg="cyan")

    except Exception as e:
        click.secho(f"Failed to load image: {e}", fg="red", bold=True)

@main.command(
    help="Start an interactive shell for entering commands."
)
def repl():
    print_welcome()
    while True:
        try:
            user_input = input("privacy_scrub > ").strip()
            if user_input in ("exit", "quit"):
                break
            elif user_input in ("help", "?"):
                click.echo(
                    "\nAvailable commands:\n"
                    "  greet NAME   - Greet someone by name\n"
                    "  load PATH    - Load and hash an image file\n"
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
