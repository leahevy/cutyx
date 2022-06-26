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

from cutyx.exceptions import FacesException

FACES_DIR_NAME = ".cutyx-faces.d"
CACHE_BASE_NAME = ".cutyx-cache.d"
FACES_CACHE_DIR_NAME = os.path.join(CACHE_BASE_NAME, "faces")
TRAINING_IMAGE_FILE_PART = ".trainingimage"
TRAINING_IMAGE_DIR_EXT = TRAINING_IMAGE_FILE_PART + ".d"
TRAINING_IMAGE_SRC_EXT = TRAINING_IMAGE_FILE_PART + ".src"


def update_cache(
    root_dir: str = ".",
    only_process_files: list[str] | None = None,
    quiet: bool = False,
) -> None:
    root_dir = os.path.abspath(root_dir)
    if not os.path.exists(root_dir):
        raise FacesException(f"Root directory ({root_dir}) does not exist.")
    if not os.path.isdir(root_dir):
        raise FacesException(f"Path ({root_dir}) is not a directory.")
    pass

    if not quiet:
        print("[green]++ Update cache ++[/green]")

    image_files_root = find_image_files(root_dir, for_albums=False)

    for image in image_files_root:
        generate_cache_for_file = True
        if only_process_files:
            generate_cache_for_file = False
            basename = os.path.basename(image)
            for file in only_process_files:
                basename2 = os.path.basename(file)
                if basename == basename2:
                    generate_cache_for_file = True
                    break

        if not generate_cache_for_file:
            continue

        with open(image, "rb") as f:
            image_hash = hashlib.md5(f.read()).hexdigest()

        encodings_dir = os.path.join(
            root_dir, FACES_CACHE_DIR_NAME, image_hash
        )
        if not os.path.exists(encodings_dir):
            pathlib.Path(encodings_dir).mkdir(parents=True, exist_ok=True)
            if not quiet:
                print(
                    f"  [blue]++ Calculating image '{os.path.basename(image)}'"
                    " face encodings ++[/blue]"
                )
            encodings_data = get_face_encodings(image, quiet=quiet)

            for idx, encoding in enumerate(encodings_data):
                if not quiet:
                    print(
                        f"    [blue]++ Writing image '{os.path.basename(image)}'"
                        f" face encoding {idx + 1}/{len(encodings_data)} ++[/blue]"
                    )
                serialized_as_json = json.dumps(
                    pickle.dumps(encoding).decode("latin-1")
                )
                md5 = str(
                    hashlib.md5(serialized_as_json.encode("utf-8")).hexdigest()
                )
                output_file = os.path.join(encodings_dir, md5 + ".encoding")
                with open(output_file, "w") as f:
                    f.write(serialized_as_json)


def clear_cache(root_dir: str = ".", quiet: bool = False) -> None:
    root_dir = os.path.abspath(root_dir)
    if not os.path.exists(root_dir):
        raise FacesException(f"Root directory ({root_dir}) does not exist.")
    if not os.path.isdir(root_dir):
        raise FacesException(f"Path ({root_dir}) is not a directory.")
    try:
        shutil.rmtree(os.path.join(root_dir, CACHE_BASE_NAME))
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
    handle_dry_run(dry_run)

    if only_process_files:
        only_process_files = [os.path.abspath(f) for f in only_process_files]
        for f in only_process_files:
            check_valid_image(f)

    if not dry_run and use_cache:
        update_cache(root_dir, only_process_files=only_process_files)

    root_dir = os.path.abspath(root_dir)

    image_files_root = find_image_files(root_dir, for_albums=False)
    album_dirs = find_album_dirs(albums_root_dir)

    if not quiet:
        if not image_files_root:
            print("[red]++ Found no images ++[/red]")
        else:
            print(f"[green]++ Found {len(image_files_root)} images ++[/green]")

    if delete_old:
        if not quiet:
            print("[green]++ Check for old files to remove ++[/green]")
        if only_process_files:
            image_files_albums = find_image_files(
                albums_root_dir, for_albums=True
            )
            for file in only_process_files:
                basename = os.path.basename(file)
                for file2 in image_files_albums:
                    basename2 = os.path.basename(file2)
                    if basename == basename2:
                        if not quiet:
                            print(
                                f"  [blue]++ Remove previously classified image '{file}' ++[/blue]"
                            )
                        if not dry_run:
                            os.remove(file2)
        else:
            for album_dir in album_dirs:
                album_dir_files = [
                    file
                    for file in os.listdir(album_dir)
                    if not file.startswith(".")
                ]
                for album_dir_file in album_dir_files:
                    if not quiet:
                        print(
                            "  [blue]++ Remove previously classified image "
                            f"'{album_dir_file}' ({os.path.basename(album_dir)}) ++[/blue]"
                        )
                    if not dry_run:
                        os.remove(os.path.join(album_dir, album_dir_file))

    for album_dir in album_dirs:
        if not quiet:
            print(
                f"[green]++ Process album directory '{os.path.basename(album_dir)} ++[/green]"
            )
        for file in image_files_root:
            do_process = True
            if only_process_files:
                if file not in only_process_files:
                    do_process = False
            cache_root_dir: str | None = root_dir
            if not use_cache:
                cache_root_dir = None
            if do_process and person_matches(
                file, album_dir, cache_root_dir=cache_root_dir, quiet=quiet
            ):
                if symlink:
                    if not quiet:
                        print(
                            f"  [blue]++ Symlink '{os.path.basename(file)}' -> "
                            f"'{os.path.basename(album_dir)}/' ++[/blue]"
                        )
                    if not dry_run:
                        os.symlink(
                            file,
                            os.path.join(album_dir, os.path.basename(file)),
                        )
                else:
                    if not quiet:
                        print(
                            f"  [blue]++ Copy '{os.path.basename(file)}' -> "
                            f"'{os.path.basename(album_dir)}/' ++[/blue]"
                        )
                    if not dry_run:
                        shutil.copyfile(
                            file,
                            os.path.join(album_dir, os.path.basename(file)),
                        )
                        shutil.copystat(
                            file,
                            os.path.join(album_dir, os.path.basename(file)),
                        )


def find_album_dirs(root_dir: str) -> list[str]:
    dirs: list[str] = []
    for root, _, _ in os.walk(
        root_dir, topdown=True, onerror=None, followlinks=True
    ):
        dpath = os.path.join(root_dir, root)
        faces_path = os.path.join(dpath, FACES_DIR_NAME)
        if os.path.exists(faces_path):
            dirs.append(dpath)
    return dirs


def find_image_files(root_dir: str, for_albums: bool = False) -> list[str]:
    images: list[str] = []
    for root, _, fnames in os.walk(
        root_dir, topdown=True, onerror=None, followlinks=True
    ):
        for fname in fnames:
            dpath = os.path.join(root_dir, root)
            faces_path = os.path.join(dpath, FACES_DIR_NAME)
            include_file = False
            if os.path.exists(faces_path):
                if for_albums:
                    include_file = True
            else:
                if not for_albums:
                    include_file = True
            if include_file:
                fpath = os.path.join(dpath, fname)
                if is_valid_image(fpath):
                    images.append(fpath)
    return images


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
        print("[red]++ DRY RUN ++[/red]")


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
    encodings = get_face_encodings(training_image_path, quiet=quiet)

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
            f"  [blue]++ Create training data directory '{output_dir}' ++[/blue]"
        )
    try:
        shutil.rmtree(output_dir)
    except FileNotFoundError:
        pass
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    for idx, encoding in enumerate(encodings):
        if not quiet:
            print(
                f"  [blue]++ Writing face encoding {idx + 1}/{len(encodings)} ++[/blue]"
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
        print("  [blue]++ Create symlink to training image ++[/blue]")
    if not dry_run:
        try:
            os.remove(symlink_path)
        except FileNotFoundError:
            pass
        os.symlink(os.path.abspath(training_image_path), symlink_path)


def is_valid_image(image_path: str) -> bool:
    if not os.path.exists(image_path):
        return False
    if not os.path.isfile(image_path):
        return False
    if not (
        image_path.lower().endswith(".jpg")
        or image_path.lower().endswith(".jpeg")
    ):
        return False
    return True


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


def get_face_encodings(
    image_path: str, cache_root_dir: str | None = None, quiet: bool = False
) -> Any:
    from cutyx import faces

    check_valid_image(image_path)

    from_cache = False
    if cache_root_dir:
        if os.path.exists(os.path.join(cache_root_dir, CACHE_BASE_NAME)):
            from_cache = True
        else:
            if not quiet:
                print("[red]++ Cache not found ++[/red]")

    if from_cache:
        with open(image_path, "rb") as f:
            image_hash = hashlib.md5(f.read()).hexdigest()

        assert cache_root_dir is not None
        encodings_dir = os.path.join(
            cache_root_dir, FACES_CACHE_DIR_NAME, image_hash
        )
        if os.path.exists(encodings_dir):
            encoding_files = os.listdir(encodings_dir)
            encodings = []
            for file in encoding_files:
                filepath = os.path.join(encodings_dir, file)

                with open(filepath, "rb") as f:
                    deserialized_from_json = pickle.loads(
                        json.loads(f.read()).encode("latin-1")
                    )
                    encodings.append(deserialized_from_json)
            return encodings
        else:
            return []
    else:
        image = faces.load_image_file(image_path)
        encodings = faces.face_encodings(image)
        return encodings


def person_matches(
    image_path: str,
    album_dir: str,
    cache_root_dir: str | None = None,
    quiet: bool = False,
) -> bool:
    from cutyx import faces

    query_encodings = get_face_encodings(
        image_path, cache_root_dir=cache_root_dir, quiet=quiet
    )

    faces_dir = os.path.join(album_dir, FACES_DIR_NAME)
    if os.path.exists(faces_dir):
        trainingdirs = [
            f
            for f in os.listdir(faces_dir)
            if f.endswith(TRAINING_IMAGE_DIR_EXT)
        ]
        for trainingdir in trainingdirs:
            trainingdirpath = os.path.join(faces_dir, trainingdir)
            encodings = os.listdir(trainingdirpath)
            for encoding in encodings:
                encodingpath = os.path.join(trainingdirpath, encoding)
                with open(encodingpath, "r") as f:
                    deserialized_from_json = pickle.loads(
                        json.loads(f.read()).encode("latin-1")
                    )
                    for query_encoding in query_encodings:
                        results = faces.compare_faces(
                            [deserialized_from_json], query_encoding
                        )
                        if True in results:
                            return True
    return False
