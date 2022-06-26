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

import pytest

from cutyx.lib import match_faces, process_directory, process_image
from tests import download_images


@pytest.fixture(scope="session", autouse=True)
def download_images_fixture() -> None:
    download_images.clear_images()
    download_images.download_images()


@pytest.fixture()
def gallery_path() -> str:
    return download_images.DIR


def test_lib_match_faces_dir(gallery_path: str) -> None:
    os.mkdir("albums")

    img1 = os.path.join(gallery_path, "einstein1.jpg")
    match_faces("albums/a", img1, training_data_prefix="albert")

    process_directory(gallery_path, "albums")
    files = [
        file for file in os.listdir("albums/a") if not file.startswith(".")
    ]
    assert len(files) == 3


def test_lib_match_faces_single(gallery_path: str) -> None:
    os.mkdir("albums")

    img1 = os.path.join(gallery_path, "einstein1.jpg")
    match_faces("albums/a", img1, training_data_prefix="albert")

    process_image(img1, "albums")
    files = [
        file for file in os.listdir("albums/a") if not file.startswith(".")
    ]
    assert "einstein1.jpg" in files
    assert len(files) == 1
