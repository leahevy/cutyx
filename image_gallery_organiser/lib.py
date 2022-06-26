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

import json
import os
import os.path
import pathlib
import pickle
import shutil
from typing import Any

from rich import print

from image_gallery_organiser import cache
from image_gallery_organiser.exceptions import FacesException


def get_face_encodings(image_path: str) -> Any:
    from image_gallery_organiser import faces

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


def clear_cache(root_dir: str = ".") -> None:
    if not os.path.exists(root_dir):
        raise FacesException(f"Root directory ({root_dir}) does not exist.")
    if not os.path.isdir(root_dir):
        raise FacesException(f"Path ({root_dir}) is not a directory.")
    try:
        shutil.rmtree(os.path.join(root_dir, cache.Cache.CACHE_DIR_NAME))
        print(f"[green]++ Cleared cache directory ({root_dir}) ++[/green]")
    except FileNotFoundError:
        print(f"[red]++ No previous cache found ({root_dir}) ++[/red]")


def process_directory(
    root_dir: str = ".",
    albums_root_dir: str = ".",
    dry_run: bool = False,
    delete_old: bool = True,
    symlink: bool = True,
    use_cache: bool = True,
) -> None:
    raise NotImplementedError()


def process_image(
    image_to_process_path: str,
    albums_root_dir: str = ".",
    dry_run: bool = False,
    delete_old: bool = True,
    symlink: bool = False,
    use_cache: bool = True,
) -> None:
    raise NotImplementedError()


def add_persons(
    training_image_path: str,
    album_dir: str,
    dry_run: bool = False,
    training_data_prefix: str | None = None,
) -> None:
    raise NotImplementedError()
    encodings = get_face_encodings(training_image_path)
    if len(encodings) == 0:
        raise ValueError("No face recognised in image")
    elif len(encodings) > 1:
        raise ValueError(
            "Multiple faces recognised. Requires image with single face."
        )

    serialized_as_json = json.dumps(
        pickle.dumps(encodings[0]).decode("latin-1")
    )

    output_dir = os.path.join(album_dir, ".faces.d")
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    import hashlib

    md5 = str(hashlib.md5(serialized_as_json.encode("utf-8")).hexdigest())
    output_file = os.path.join(output_dir, md5 + ".encoding")
    with open(output_file, "w") as f:
        f.write(serialized_as_json)


def person_matches(image_path: str) -> None:
    raise NotImplementedError()
    from image_gallery_organiser import faces

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
