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

from typing import Any

import face_recognition  # type: ignore


def load_image_file(image_path: str) -> Any:
    return face_recognition.load_image_file(image_path)


def face_encodings(image: Any) -> Any:
    return face_recognition.face_encodings(image)


def compare_faces(
    faces_encodings: list[Any], file_encoding_to_compare: Any
) -> list[bool]:
    res: list[bool] = face_recognition.compare_faces(  # type: ignore
        faces_encodings, file_encoding_to_compare
    )
    if not res:
        res = []
    return res
