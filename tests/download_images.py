#!/usr/bin/env python
#
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

import os
import shutil
import urllib.request

DIR = os.path.abspath("./tests/image-gallery")


def download_image(url: str) -> None:
    if not os.path.exists(DIR):
        raise ValueError("Image directory does not exist")
    filename = url.rsplit("/", 1)[1]
    if not (
        filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg")
    ):
        filename += ".jpg"
    urllib.request.urlretrieve(url, os.path.join(DIR, filename))


def clear_images() -> None:
    shutil.rmtree(DIR)
    os.mkdir(DIR)
    with open(os.path.join(DIR, ".gitignore"), "w") as f:
        f.write("*\n!.gitignore\n")


def download_images() -> None:
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg"
    )
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg"
    )
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/5/50/Albert_Einstein_%28Nobel%29.png"
    )


def main() -> None:
    clear_images()
    download_images()


if __name__ == "__main__":
    main()
