# Copyright (C) 2022 Leah Lackner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This is the main module docstring.

Some description comes here.
"""

import os
import os.path
import sys
from typing import Optional

import typer
from rich import print

# Allow running the main python script without installing the package
if __name__ == "__main__":
    import os as _os
    import sys as _sys

    _sys.path.append(_os.path.join(_os.path.dirname(__file__), ".."))

from cutyx.__version__ import __version__

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="""
Organises your image gallery using machine learning.

You can check the individual --help option on the commands for more information.

To run the main utility try the 'run' command.
""",
)


def version_callback(value: bool) -> None:
    """
    Prints the version.
    """
    if value:
        print(
            f"[green]{os.path.basename(sys.argv[0])}:[/green]"
            f" [blue]v{__version__}[/blue]"
        )
        raise typer.Exit()


@app.command()
def clear_cache(
    root_dir: str = typer.Option(
        os.getcwd(), "-r", "--root-dir", help="Root dir containing the cache."
    )
) -> None:
    """Clears the local cache."""
    from cutyx import lib

    lib.clear_cache(root_dir=root_dir)


@app.command()
def run(
    root_dir: str = typer.Option(
        os.getcwd(),
        "-r",
        "--root-dir",
        help="Root dir containing the images to be processed.",
    ),
    dry_run: bool = typer.Option(
        False, "-n", "--dry-run", help="Only pretend to do anything."
    ),
    albums_root_dir: str = typer.Option(
        os.getcwd(),
        "--albums-root-dir",
        help="Root albums dir.",
    ),
    delete_old: bool = typer.Option(
        True,
        "-d",
        "--delete-old",
        help="Delete previously classified images found in album directories (images outside of a trained album dir are not removed).",
    ),
    symlink: bool = typer.Option(
        False,
        "-s",
        "--symlink",
        help="Do not copy the images to the album directories. Instead create a smylink.",
    ),
    no_cache: bool = typer.Option(
        False, "-c", "--no-cache", help="Disables the cache."
    ),
) -> None:
    """Process images anywhere in a directory hierarchy."""
    from cutyx import lib

    lib.process_directory(
        root_dir=root_dir,
        dry_run=dry_run,
        albums_root_dir=albums_root_dir,
        delete_old=delete_old,
        symlink=symlink,
        use_cache=not no_cache,
    )


@app.command()
def process_image(
    image_to_process_path: str = typer.Argument(..., help="Image to process."),
    dry_run: bool = typer.Option(
        False, "-n", "--dry-run", help="Only pretend to do anything."
    ),
    albums_root_dir: str = typer.Option(
        os.getcwd(),
        "--albums-root-dir",
        help="Root albums dir.",
    ),
    delete_old: bool = typer.Option(
        True,
        "-d",
        "--delete-old",
        help="Delete instances of the previously classified image found in album directories (images outside of a trained album dir are not removed).",
    ),
    symlink: bool = typer.Option(
        False,
        "-s",
        "--symlink",
        help="Do not copy the images to the album directories. Instead create a smylink.",
    ),
    no_cache: bool = typer.Option(
        False, "-c", "--no-cache", help="Disables the cache."
    ),
) -> None:
    """Process a single image."""
    from cutyx import lib

    lib.process_image(
        image_to_process_path,
        albums_root_dir,
        dry_run=dry_run,
        delete_old=delete_old,
        symlink=symlink,
        use_cache=not no_cache,
    )


@app.command()
def add_persons(
    training_image_path: str = typer.Argument(
        ..., help="Training image containing the persons."
    ),
    album_dir: str = typer.Argument(
        ...,
        help="The album directory which should be configured to match the persons in the training image.",
    ),
    dry_run: bool = typer.Option(
        False, "-n", "--dry-run", help="Only pretend to do anything."
    ),
    training_data_prefix: Optional[str] = typer.Option(
        None,
        "-p",
        "--training-prefix",
        help="Prefix for the training sample (default: no prefix).",
    ),
) -> None:
    """Add training data for persons found in a training image to the target album directory."""
    from cutyx import lib

    lib.add_persons(
        album_dir,
        training_image_path,
        dry_run=dry_run,
        training_data_prefix=training_data_prefix,
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
