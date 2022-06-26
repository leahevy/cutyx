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

import hashlib
import json
import os
import os.path
import pathlib
import pickle
import shutil
from typing import Any

from rich import print

from cutyx import cache
from cutyx.exceptions import FacesException

FACES_DIR_NAME = ".faces.d"
TRAINING_IMAGE_FILE_PART = ".trainingimage"
TRAINING_IMAGE_DIR_EXT = TRAINING_IMAGE_FILE_PART + ".d"
TRAINING_IMAGE_SRC_EXT = TRAINING_IMAGE_FILE_PART + ".src"


def clear_cache(root_dir: str = ".", quiet: bool = False) -> None:
    root_dir = os.path.abspath(root_dir)
    if not os.path.exists(root_dir):
        raise FacesException(f"Root directory ({root_dir}) does not exist.")
    if not os.path.isdir(root_dir):
        raise FacesException(f"Path ({root_dir}) is not a directory.")
    try:
        shutil.rmtree(os.path.join(root_dir, cache.Cache.CACHE_DIR_NAME))
        if not quiet:
            print(f"[green]++ Cleared cache directory ({root_dir}) ++[/green]")
    except FileNotFoundError:
        if not quiet:
            print(f"[red]++ No previous cache found ({root_dir}) ++[/red]")


def process_directory(
    root_dir: str = ".",
    albums_root_dir: str = ".",
    dry_run: bool = False,
    delete_old: bool = True,
    symlink: bool = True,
    use_cache: bool = True,
    quiet: bool = False,
    only_process_files: list[str] | None = None,
) -> None:
    root_dir = os.path.abspath(root_dir)
    if only_process_files:
        only_process_files = [os.path.abspath(f) for f in only_process_files]
        for f in only_process_files:
            check_valid_image(f)


def process_image(
    image_to_process_path: str,
    albums_root_dir: str = ".",
    dry_run: bool = False,
    delete_old: bool = True,
    symlink: bool = False,
    use_cache: bool = True,
    quiet: bool = False,
) -> None:
    check_valid_image(image_to_process_path)
    dirname = os.path.dirname(image_to_process_path)
    process_directory(
        dirname,
        albums_root_dir=albums_root_dir,
        dry_run=dry_run,
        delete_old=delete_old,
        symlink=symlink,
        use_cache=use_cache,
        quiet=quiet,
        only_process_files=[image_to_process_path],
    )


def handle_dry_run(dry_run: bool) -> None:
    if dry_run:
        print("[blue]++ DRY RUN ++[/blue]")


def add_persons(
    album_dir: str,
    training_image_path: str,
    dry_run: bool = False,
    training_data_prefix: str | None = None,
    quiet: bool = False,
) -> None:
    handle_dry_run(dry_run)
    check_valid_image(training_image_path)

    if not quiet:
        print(
            f"[green]++ Calculate face encodings '{training_image_path}' ++[/green]"
        )
    encodings = get_face_encodings(training_image_path)

    if len(encodings) == 0:
        raise FacesException(
            f"No face recognised in image '{training_image_path}."
        )

    with open(training_image_path, "rb") as f:
        image_hash = hashlib.md5(f.read()).hexdigest()

    output_training_dir_name = image_hash + TRAINING_IMAGE_DIR_EXT
    if training_data_prefix:
        output_training_dir_name = (
            training_data_prefix + "-" + output_training_dir_name
        )

    output_dir = os.path.join(
        album_dir, FACES_DIR_NAME, output_training_dir_name
    )
    if not quiet:
        print(
            f"[green]++ Create training data directory '{output_dir}' ++[/green]"
        )
    try:
        shutil.rmtree(output_dir)
    except FileNotFoundError:
        pass
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    for idx, encoding in enumerate(encodings):
        if not quiet:
            print(
                f"[green]++ Writing face encoding {idx + 1}/{len(encodings)} ++[/green]"
            )
        serialized_as_json = json.dumps(
            pickle.dumps(encoding).decode("latin-1")
        )
        md5 = str(hashlib.md5(serialized_as_json.encode("utf-8")).hexdigest())
        output_file = os.path.join(output_dir, md5 + ".encoding")
        if not dry_run:
            with open(output_file, "w") as f:
                f.write(serialized_as_json)
    symlink_path = image_hash + TRAINING_IMAGE_SRC_EXT
    if training_data_prefix:
        symlink_path = training_data_prefix + "-" + symlink_path
    symlink_path = os.path.join(album_dir, FACES_DIR_NAME, symlink_path)
    if not quiet:
        print("[green]++ Create symlink to training file ++[/green]")
    if not dry_run:
        try:
            os.remove(symlink_path)
        except FileNotFoundError:
            pass
        os.symlink(os.path.abspath(training_image_path), symlink_path)


def check_valid_image(image_path: str) -> None:
    if not os.path.exists(image_path):
        raise FacesException(f"Path '{image_path}' does not exist.")
    if not os.path.isfile(image_path):
        raise FacesException(f"Path '{image_path}' is no file.")
    if not (
        image_path.lower().endswith(".jpg")
        or image_path.lower().endswith(".jpeg")
    ):
        raise FacesException(
            f"File '{image_path}' has an invalid file type (only JPEGs are supported)."
        )


def get_face_encodings(image_path: str) -> Any:
    from cutyx import faces

    if not os.path.exists(image_path):
        raise ValueError(f"Image '{image_path}' does not exist.")
    if not (
        image_path.lower().endswith(".jpeg")
        or image_path.lower().endswith(".jpg")
    ):
        raise ValueError(
            f"File extension of image '{image_path}' not supported."
        )
    image = faces.load_image_file(image_path)
    encodings = faces.face_encodings(image)

    return encodings


def person_matches(image_path: str) -> None:
    raise NotImplementedError("person_matches")
    from cutyx import faces

    encodings = get_face_encodings(image_path)
    paths = os.listdir(".")
    for path in paths:
        if os.path.isdir(path) and path not in [".", ".."]:
            encoding_path = os.path.join(path, ".faces.d")
            if os.path.exists(encoding_path):
                facesfiles = os.listdir(encoding_path)
                for face in facesfiles:
                    facepath = os.path.join(encoding_path, face)
                    with open(facepath, "r") as f:
                        deserialized_from_json = pickle.loads(
                            json.loads(f.read()).encode("latin-1")
                        )
                        for encoding in encodings:
                            results = faces.compare_faces(
                                [deserialized_from_json], encoding
                            )
                            if True in results:
                                print(path)
