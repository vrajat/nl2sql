"""nl2sql CLI."""

import typer

from rich import print
from typing_extensions import Annotated
from nl2sql.dbagent import DBAgent

from nl2sql.typer_shell import make_typer_shell

app = typer.Typer()
make_typer_shell(app, prompt="nl2sql: ")

default = lambda x: print(f"Inner Default, args: {x}")

@app.command()
def tellme(ctx: typer.Context, message: Annotated[str, typer.Argument()]) -> None:
    """Say a message."""
    dbagent: DBAgent = ctx.obj["db_agent"]
    dbagent.agent.run(message)
