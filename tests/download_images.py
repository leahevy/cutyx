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


def download_image(url: str, filename: str | None = None) -> None:
    if not os.path.exists(DIR):
        raise ValueError("Image directory does not exist")
    if not filename:
        filename = url.rsplit("/", 1)[1]
        if ":" in filename:
            filename = filename.rsplit(":", 1)[1]
        if "?" in filename:
            filename = filename.rsplit("?", 1)[1]
        if "=" in filename:
            filename = filename.rsplit("=", 1)[1]
        if not (
            filename.lower().endswith(".jpg")
            or filename.lower().endswith(".jpeg")
        ):
            filename += ".jpg"
    print(f"Download '{url}'")
    urllib.request.urlretrieve(url, os.path.join(DIR, filename))


def clear_images() -> None:
    shutil.rmtree(DIR)
    os.mkdir(DIR)
    with open(os.path.join(DIR, ".gitignore"), "w") as f:
        f.write("*\n!.gitignore\n")


def download_images() -> None:
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg",
        "einstein1.jpg",
    )
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg",
        "einstein2.jpg",
    )
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/5/50/Albert_Einstein_%28Nobel%29.png",
        "einstein3.png",
    )
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg",
        "puurrrr.jpg",
    )
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/e/e8/Lc3_2018_%28263682303%29_%28cropped%29.jpeg",
        "linus1.jpg",
    )
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/2/28/Richard_Stallman_at_LibrePlanet_2019.jpg",
        "stallman1.jpg",
    )
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/e/e2/Guido-portrait-2014-drc.jpg",
        "guido1.jpg",
    )
    download_image(
        "https://static.wikia.nocookie.net/elfen-lied/images/6/64/Kaede_Manga.jpg/revision/latest?cb=20180922143710",
        "manga.jpg",
    )
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/8/8c/Self-portrait_at_13_by_Albrecht_D%C3%BCrer.jpg",
        "portrait1.jpg",
    )
    download_image(
        "https://upload.wikimedia.org/wikipedia/commons/c/c5/Edward_Law._Pencil_drawing_by_H._M._Raeburn%2C_1909._Wellcome_V0003431.jpg",
        "drawing1.jpg",
    )
    download_image(
        "https://cdn.arstechnica.net/wp-content/uploads/2013/02/linus-eff-you-640x363.png",
        "linus2.png",
    )


def main() -> None:
    clear_images()
    download_images()


if __name__ == "__main__":
    main()
