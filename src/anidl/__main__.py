import click

from anidl.ui.app import Anidl


@click.command()
def main():
    """Anime downloader"""
    app = Anidl()
    app.run()


if __name__ == "__main__":
    main()
