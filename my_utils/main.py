import typer
import utils

app = typer.Typer()


@app.command()
def main():
    typer.echo(f"Welcome!")


@app.command()
def start_up():
    """Start up normal applications"""
    typer.echo(f"Welcome! Starting up...")

    typer.echo(f"Opening System Applications...")
    utils.open_system_apps()

    typer.echo(f"Opening Installed Applications...")
    utils.open_installed_apps()


if __name__ == "__main__":
    app()
