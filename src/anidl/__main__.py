import click

from anidl import hello


@click.command()
def main():
    """Anime downloader"""
    print(hello())


if __name__ == "__main__":
    main()
