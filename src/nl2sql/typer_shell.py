from pathlib import Path
from typing_extensions import Annotated
from typing import Optional, Callable

from click_shell import make_click_shell
from typer import Context, Typer, Argument

from rich import print

from nl2sql.dbagent import DBAgent


def make_typer_shell(
        app: Typer,
        prompt: str = ">> ",
        intro: str = "\n Welcome to nl2sql-shell! Type help to see commands.\n",
        default: Optional[Callable] = None
) -> None:
    @app.command(hidden=True)
    def help(ctx: Context, command: Annotated[Optional[str], Argument()] = None):
        print("\n Type 'command --help' or 'help <command>' for help on a specific command.")
        if not command:
            ctx.parent.get_help()
            return
        ctx.parent.command.get_command(ctx, command).get_help(ctx)

    @app.command(hidden=True)
    def _default(ctx: Context, args: Annotated[Optional[str], Argument()] = None):
        """Default command"""
        if default:
            default(args)
        else:
            print("Command not found. Type 'help' to see commands.")

    @app.callback(invoke_without_command=True)
    def launch(ctx: Context,
               open_ai_key: Annotated[Path, Argument()],
               db_path: Annotated[Path, Argument()]):
        if ctx.invoked_subcommand is None:
            ctx.obj = {
                "db_agent": DBAgent(open_ai_key, db_path),
            }
            shell = make_click_shell(ctx, prompt=prompt, intro=intro)
            shell.default = _default
            shell.cmdloop()
