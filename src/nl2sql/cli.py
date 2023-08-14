"""nl2sql CLI."""

import typer

from rich import print

from nl2sql.typer_shell import make_typer_shell

app = typer.Typer()
make_typer_shell(app, prompt="🔥: ")

default = lambda x: print(f"Inner Default, args: {x}")

@app.command()
def say(message: str = "") -> None:
    """Say a message."""
    typer.echo(message)
