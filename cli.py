import click
import uvicorn
# import socket
from IPython.core.ultratb import VerboseTB
import os
import sys
import IPython
from IPython.terminal.ipapp import load_default_config
from database.db_session import db
from IPython.core.profiledir import ProfileDir

@click.group()
def custom_cli():
    os.environ['PYTHONBREAKPOINT'] = 'IPython.terminal.debugger.set_trace'


@custom_cli.group("server")
def custom_server():
    pass


@custom_server.command("shell")
@click.argument("ipython_args", nargs=-1, type=click.UNPROCESSED)
@click.option("--nolog", is_flag=True, default=False)
def shell(ipython_args, nolog):
    profile_name = "custom_cli"
    ProfileDir.create_profile_dir_by_name(name=profile_name, path="./")
    config = load_default_config()
    config.TerminalInteractiveShell.banner1 = (
        f"""Python {sys.version} on {sys.platform} IPython: {IPython.__version__}"""
    )
    config.TerminalInteractiveShell.autoindent = True
    config.InteractiveShellApp.exec_lines = [
        "%load_ext autoreload",
        "%autoreload 2",
    ]
    config.TerminalInteractiveShell.autoformatter = "black"
    VerboseTB._tb_highlight = "bg:#4C5656"
    config.InteractiveShell.ast_node_interactivity = "all"
    config.InteractiveShell.debug = True
    config.TerminalInteractiveShell.highlighting_style = "paraiso-dark"
    config.TerminalIPythonApp.profile = profile_name
    user_ns = {"database": db}
    with db.connection_context():
        IPython.start_ipython(argv=ipython_args, user_ns=user_ns, config=config)


custom_server.add_command(uvicorn.main, name="start")


def entrypoint():
    try:
        custom_cli()
    except Exception as e:
        click.secho(f"ERROR: {e}", bold=True, fg="red")


if __name__ == "__main__":
    entrypoint()
