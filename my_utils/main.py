import typer
import utils

app = typer.Typer()


@app.command()
def main():
    typer.echo(f"Welcome!")


@app.command()
def start_up(apps: str = "default"):
    """Start up applications
    
    Args:
        apps (str): Type of applications to open based on my-apps.json key values.
    """
    typer.echo(f"Welcome! Starting up Applications...")
    match apps:
        case "default":
            typer.echo(f"Opening System Applications...")
            utils.open_apps("installed")

            typer.echo(f"Opening Installed Applications...")
            utils.open_apps("system")
        case "music":
            typer.echo(f"Opening Music Applications...")
            utils.open_apps("music")


if __name__ == "__main__":
    app()
