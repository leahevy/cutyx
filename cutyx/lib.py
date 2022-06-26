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
from cutyx.utils import copyfile, mksymlink

FACES_DIR_NAME = ".cutyx-faces.d"
CACHE_BASE_NAME = ".cutyx-cache.d"
FACES_CACHE_DIR_NAME = os.path.join(CACHE_BASE_NAME, "faces")
TRAINING_IMAGE_FILE_PART = ".trainingimage"
TRAINING_IMAGE_DIR_EXT = TRAINING_IMAGE_FILE_PART + ".d"
TRAINING_IMAGE_SRC_EXT = TRAINING_IMAGE_FILE_PART + ".src"


def is_included(
    path: str,
    only_process_files: set[str] | None = None,
) -> bool:
    """Checks if a file is excluded by not being mentioned in
    the only process files list. Matches only the basename of
    the files.

    :param path: The path to be checked.

    :param only_process_files: The include file list to check the path for.
        If `None`, the file will be included. Defaults to `None`.

    :return: `True` if the path should be included, `False` otherwise.
    """
    if only_process_files:
        # Only compares the basename.
        basename = os.path.basename(path)
        for file in only_process_files:
            basename2 = os.path.basename(file)
            if basename == basename2:
                return True
        return False
    else:
        # Always include the file if no set was given.
        return True


def update_cache(
    root_dir: str = ".",
    only_process_files: set[str] | None = None,
    quiet: bool = False,
) -> None:
    """Updates the cache.

    :param root_dir: The root path. In this directory, the cache directory will be located,
        and it should also be the root of all images to be analysed.

    :param only_process_files: A set of image paths to be processed. If `None`, all found images
    will be classified.

    :param quiet: Whether additional verbose output should be generated.
    """
    # Checks for correct parameters
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
        # Only process files which are not excluded
        if not is_included(image, only_process_files):
            continue

        # Generate an MD5 hash, as this is used for the cache file name
        with open(image, "rb") as f:
            image_hash = hashlib.md5(f.read()).hexdigest()

        encodings_dir = os.path.join(
            root_dir, FACES_CACHE_DIR_NAME, image_hash
        )
        # Only re-calculates the encodings for images which were not classified
        # in an earlier run.
        if not os.path.exists(encodings_dir):
            pathlib.Path(encodings_dir).mkdir(parents=True, exist_ok=True)
            if not quiet:
                print(
                    f"  [blue]++ Calculating image '{os.path.basename(image)}'"
                    " face encodings ++[/blue]"
                )

            # Calculate the face encodings
            encodings_data = get_face_encodings(image, quiet=quiet)

            # Serialise the face encodings
            for idx, encoding in enumerate(encodings_data):
                if not quiet:
                    print(
                        f"    [blue]++ Writing image '{os.path.basename(image)}'"
                        f" face encoding {idx + 1}/{len(encodings_data)} ++[/blue]"
                    )
                serialized_as_json = json.dumps(
                    pickle.dumps(encoding).decode("latin-1")
                )
                # Store the individual encoding in a filename that is the MD5 hash of the
                # encoding itself.
                md5 = str(
                    hashlib.md5(serialized_as_json.encode("utf-8")).hexdigest()
                )
                output_file = os.path.join(encodings_dir, md5 + ".encoding")
                with open(output_file, "w") as f:
                    f.write(serialized_as_json)


def clear_cache(root_dir: str = ".", quiet: bool = False) -> None:
    """Clears the cache.

    :param root_dir: The root path. In this directory, the cache directory will be searched.

    :param quiet: Whether additional verbose output should be generated.
    """
    # Check the parameters
    root_dir = os.path.abspath(root_dir)
    if not os.path.exists(root_dir):
        raise FacesException(f"Root directory ({root_dir}) does not exist.")
    if not os.path.isdir(root_dir):
        raise FacesException(f"Path ({root_dir}) is not a directory.")
    try:
        # Remove the cache directory recursively if it exists
        shutil.rmtree(os.path.join(root_dir, CACHE_BASE_NAME))
        if not quiet:
            print(f"[green]++ Cleared cache directory ({root_dir}) ++[/green]")
    except FileNotFoundError:
        if not quiet:
            print(f"[red]++ No previous cache found ({root_dir}) ++[/red]")


def handle_delete_old(
    albums_root_dir: str,
    only_process_files: set[str] | None = None,
    quiet: bool = False,
    dry_run: bool = False,
) -> None:
    """Internal function to handle the deletion of old files in albums.

    :param albums_root_dir: The root path containing the albums.
        Albums will be searched in the whole hierarchy.

    :param only_process_files: A set of image paths to be processed. If `None`, all found images
    will be considered for deletion.

    :param quiet: Whether additional verbose output should be generated.

    :param dry_run: Whether to only print the actions which would be executed.
    """
    if not quiet:
        print("[green]++ Check for old files to remove ++[/green]")

    # Find all directories which are configured to be used with `CutyX`
    album_dirs = find_album_dirs(albums_root_dir)

    if only_process_files:
        # Do a matching on the base name to check, whether the file should be removed
        image_files_albums = find_image_files(albums_root_dir, for_albums=True)
        for image_album_file in image_files_albums:
            if is_included(image_album_file, only_process_files):
                if not os.path.isdir(image_album_file):
                    if not quiet:
                        print(
                            "  [blue]++ Remove previously classified image "
                            f"'{os.path.basename(image_album_file)}' ++[/blue]"
                        )
                    if not dry_run:
                        os.remove(image_album_file)
    else:
        # Remove all non-hidden files in a found album directory
        for album_dir in album_dirs:
            album_dir_files = [
                file
                for file in os.listdir(album_dir)
                if not file.startswith(".")
            ]
            for album_dir_file in album_dir_files:
                file_to_remove = os.path.join(album_dir, album_dir_file)
                if not os.path.isdir(file_to_remove):
                    if not quiet:
                        print(
                            "  [blue]++ Remove previously classified image "
                            f"'{album_dir_file}' ({os.path.basename(album_dir)}) ++[/blue]"
                        )
                    if not dry_run:
                        os.remove(file_to_remove)


def process_directory(
    root_dir: str = ".",
    albums_root_dir: str = ".",
    dry_run: bool = False,
    delete_old: bool = True,
    symlink: bool = True,
    use_cache: bool = True,
    quiet: bool = False,
    only_process_files: set[str] | None = None,
) -> None:
    """The main logic of **CutyX**.

    This function will process the files, classify them, and write the results to the
    album directories.

    :param root_dir: The root path containing the images to be organised.
        Images will be searched in the whole hierarchy.

    :param albums_root_dir: The root path containing the albums.
        Albums will be searched in the whole hierarchy.

    :param dry_run: Whether to only print the actions which would be executed.

    :param delete_old: Whether to delete old images in the album directories,
        before processing the new ones.

    :param symlink: Whether to symlink from the album folder instead of copying it.

    :param use_cache: Whether the cache should be used.

    :param quiet: Whether additional verbose output should be generated.

    :param only_process_files: A set of image paths to be processed. If `None`, all found images
    will be considered for processing.
    """
    handle_dry_run(dry_run)

    # Check only-process files for validity
    if only_process_files:
        only_process_files = {os.path.abspath(f) for f in only_process_files}
        for f in only_process_files:
            check_valid_image(f)

    # Update the cache if the cache should be used
    if not dry_run and use_cache:
        update_cache(root_dir, only_process_files=only_process_files)

    root_dir = os.path.abspath(root_dir)

    # Handle deletion of old files
    if delete_old:
        handle_delete_old(
            albums_root_dir,
            only_process_files=only_process_files,
            quiet=quiet,
            dry_run=dry_run,
        )

    # Run the actual processing
    handle_process_files(
        root_dir,
        albums_root_dir,
        only_process_files=only_process_files,
        quiet=quiet,
        use_cache=use_cache,
        symlink=symlink,
        dry_run=dry_run,
    )


def handle_process_files(
    root_dir: str,
    albums_root_dir: str,
    only_process_files: set[str] | None = None,
    quiet: bool = False,
    use_cache: bool = False,
    symlink: bool = False,
    dry_run: bool = False,
) -> None:
    """The main processing and classification logic.

    :param root_dir: The root path containing the images to be organised.
        Images will be searched in the whole hierarchy.

    :param albums_root_dir: The root path containing the albums.
        Albums will be searched in the whole hierarchy.

    :param dry_run: Whether to only print the actions which would be executed.

    :param symlink: Whether to symlink from the album folder instead of copying it.

    :param use_cache: Whether the cache should be used.

    :param quiet: Whether additional verbose output should be generated.

    :param only_process_files: A set of image paths to be processed. If `None`, all found images
    will be considered for processing.
    """
    num_processed = 0

    # Search for all images
    album_dirs = find_album_dirs(albums_root_dir)
    image_files_root = find_image_files(root_dir, for_albums=False)

    if not quiet:
        if not image_files_root:
            print("[red]++ Found no images ++[/red]")
        else:
            print(f"[green]++ Found {len(image_files_root)} images ++[/green]")

    # Process the albums
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
                # We got a match => Copy or symlink the file to the albums folder
                num_processed += 1
                if symlink:
                    if not quiet:
                        print(
                            f"  [blue]++ Symlink '{os.path.basename(file)}' -> "
                            f"'{os.path.basename(album_dir)}/' ++[/blue]"
                        )
                    if not dry_run:
                        mksymlink(
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
                        copyfile(
                            file,
                            os.path.join(album_dir, os.path.basename(file)),
                        )

    # Raises an exception if albums are configured, but not a single match
    # was found.
    if num_processed == 0 and image_files_root and album_dirs:
        raise FacesException("No images were matching for any album.")


def find_album_dirs(root_dir: str) -> list[str]:
    """Searches hierarchically for all configured album directories.

    :param root_dir: The root path containing the albums.
        Albums will be searched in the whole hierarchy.

    :return: A `list` of all found album directories.
    """
    dirs: list[str] = []
    for root, dnames, _ in os.walk(
        root_dir, topdown=True, onerror=None, followlinks=True
    ):
        # Search for albums in the current and child directories
        for d in [root] + dnames:
            dpath = os.path.join(root_dir, d)
            faces_path = os.path.join(dpath, FACES_DIR_NAME)
            # If a faces dir is in the directory, it is considered as an album
            if os.path.exists(faces_path):
                dirs.append(dpath)
    return dirs


def find_image_files(root_dir: str, for_albums: bool = False) -> list[str]:
    """Searches hierarchically for all images.

    :param root_dir: The root path containing the images.
        Images will be searched in the whole hierarchy.

    :param for_albums: Whether the images should return images from albums directories
        or only from non-album directories.

    :return: A `list` of all found images.
    """
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
    """Processes only a single image file.

    :param image_to_process_path: The image to be processed.

    :param albums_root_dir: The root path containing the albums.
        Albums will be searched in the whole hierarchy.

    :param dry_run: Whether to only print the actions which would be executed.

    :param delete_old: Whether to delete instances of this image file in the album directories.

    :param symlink: Whether to symlink from the album folder instead of copying it.

    :param use_cache: Whether the cache should be used.

    :param quiet: Whether additional verbose output should be generated.
    """
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
        only_process_files={image_to_process_path},
    )


def handle_dry_run(dry_run: bool) -> None:
    """Set-up dry-run.

    :param dry_run: Whether to use dry run.
    """
    if dry_run:
        print("[red]++ DRY RUN ++[/red]")


def match_faces(
    album_dir: str,
    training_image_path: str,
    dry_run: bool = False,
    training_data_prefix: str | None = None,
    quiet: bool = False,
) -> None:
    """Adds training data for a face classification to an album.

    :param album_dir: The album to add the training data to.

    :param training_image_path: The training data image. All faces found in this image will
        be used to classify images as valid for this album.

    :param dry_run: Whether to only print the actions which would be executed.

    :param training_data_prefix: A prefix for training data of this image in the hidden
        album directory. Can be used to make it easier to remove faces from the classification
        later.

    :param quiet: Whether additional verbose output should be generated.
    """
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
    # Re-generate the training data
    try:
        shutil.rmtree(output_dir)
    except FileNotFoundError:
        pass
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Write all found face encodings
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

    # Generates a symlink to the training image to make it easier to remove it later.
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
        mksymlink(os.path.abspath(training_image_path), symlink_path)


def is_valid_image(image_path: str) -> bool:
    """Checks an image file for validity."""
    try:
        check_valid_image(image_path)
        return True
    except FacesException:
        return False


def check_valid_image(image_path: str) -> None:
    """Requires validity for an image. Throws an exception otherwise."""
    if not os.path.exists(image_path):
        raise FacesException(f"Path '{image_path}' does not exist.")
    if not os.path.isfile(image_path):
        raise FacesException(f"Path '{image_path}' is no file.")
    if not (
        image_path.lower().endswith(".jpg")
        or image_path.lower().endswith(".jpeg")
        or image_path.lower().endswith(".png")
    ):
        raise FacesException(
            f"File '{image_path}' has an invalid file type (only JPEGs are supported)."
        )


def get_face_encodings(
    image_path: str, cache_root_dir: str | None = None, quiet: bool = False
) -> Any:
    """Returns the face encodings for an image.

    Uses the cache if one is configured.
    """
    from cutyx import faces

    check_valid_image(image_path)

    # Checks whether the cache should be used for encodings
    from_cache = False
    if cache_root_dir:
        if os.path.exists(os.path.join(cache_root_dir, CACHE_BASE_NAME)):
            from_cache = True
        else:
            if not quiet:
                print("[red]++ Cache not found ++[/red]")

    # Loads the encodings from the associated cache directory
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
        # Calculates the face encodings without caching
        image = faces.load_image_file(image_path)
        encodings = faces.face_encodings(image)
        return encodings


def person_matches(
    image_path: str,
    album_dir: str,
    cache_root_dir: str | None = None,
    quiet: bool = False,
) -> bool:
    """Checks whether a person matches to one of the configured training data images
    in the given album directory.
    """
    from cutyx import faces

    # Get the face encodings for the image in question
    query_encodings = get_face_encodings(
        image_path, cache_root_dir=cache_root_dir, quiet=quiet
    )

    # If no faces directory exists, we cannot classify anything
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

                # Load the classifier from the album directory
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
