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
    rule_prefix: Optional[str] = typer.Option(
        None,
        "-p",
        "--rule-prefix",
        help="Prefix for the rule (default: no prefix).",
    ),
) -> None:
    """Matches registered faces in images."""
    from cutyx import lib

    lib.match_faces(
        album_dir,
        training_image_path,
        dry_run=dry_run,
        training_data_prefix=rule_prefix,
    )


@app.command()
def name(
    text: str = typer.Argument(..., help="Text to match the file names to."),
    album_dir: str = typer.Argument(
        ...,
        help="The album directory which should be configured to match the persons in the training image.",
    ),
    use_regex: bool = typer.Option(
        False,
        "-r",
        "--regex",
        help="Use regular expressions for matching (not combinable with fuzzy).",
    ),
    use_fuzzy: bool = typer.Option(
        False,
        "-f",
        "--fuzzy",
        help="Allows fuzzy matching (not combinable with regex).",
    ),
    fuzzy_min_ratio: int = typer.Option(
        60,
        "-i",
        "--fuzzy-min-ratio",
        help="Sets the minimum ratio to score a fuzzy match.",
    ),
    dry_run: bool = typer.Option(
        False, "-n", "--dry-run", help="Only pretend to do anything."
    ),
    rule_name: Optional[str] = typer.Option(
        None,
        "-p",
        "--rule-name",
        help="Name for the rule (default: auto-generated rule name).",
    ),
) -> None:
    """Matches registered faces in images."""
    from cutyx import lib

    lib.match_names(
        album_dir,
        text,
        dry_run=dry_run,
        use_regex=use_regex,
        use_fuzzy=use_fuzzy,
        fuzzy_min_ratio=fuzzy_min_ratio,
        rule_name=rule_name,
    )
