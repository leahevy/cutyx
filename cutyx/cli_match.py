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

"""This is the CLI of `CutyX`.

For the implementation of the commands the `typer` library is used. This
CLI only contains stubs. All the logic is implemented in the `lib` module.
"""
from typing import Optional

import typer

app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="""
Commands to configure album directories to match certain images.
""",
)


@app.command()
def faces(
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
    """Matches registered faces in images."""
    from cutyx import lib

    lib.match_faces(
        album_dir,
        training_image_path,
        dry_run=dry_run,
        training_data_prefix=training_data_prefix,
    )
