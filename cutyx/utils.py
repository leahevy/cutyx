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

"""Utility functions used within `Cutyx`."""

import os
import os.path


def mksymlink(target: str, linkpath: str) -> None:
    """Creates a symlink and automatically resolves it as a relative path.

    :param target: The target file to be linked to.

    :param linkpath: The path of the generated link.
    """
    os.symlink(os.path.relpath(target, os.path.dirname(linkpath)), linkpath)
