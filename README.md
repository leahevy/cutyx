<div align="center">
<a href="https://github.com/leahevy/cutyx"><img src="https://raw.githubusercontent.com/leahevy/cutyx/master/assets/cutyx.png" width="350px" alt="cutyx"/></a>
</div>
<br/>

<p align="center">
<b>✨ Tool to organise your image gallery using machine learning. ✨</b> 
</p>

<p align="center">
<a href="https://github.com/leahevy/cutyx/graphs/commit-activity"><img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" alt="This project is maintained"/></a>
<a href="https://github.com/leahevy/cutyx/actions/workflows/build.yml"><img src="https://github.com/leahevy/cutyx/actions/workflows/build.yml/badge.svg" alt="Build"/></a>
<a href="https://github.com/leahevy/cutyx/actions/workflows/tests.yml"><img src="https://github.com/leahevy/cutyx/actions/workflows/tests.yml/badge.svg" alt="Tests"/></a>
<a href="https://github.com/leahevy/cutyx/actions/workflows/coverage.yml"><img src="https://raw.githubusercontent.com/leahevy/cutyx/coverage/coverage.svg" alt="Coverage"/></a>
<a href="https://github.com/leahevy/cutyx/actions/workflows/style.yml"><img src="https://github.com/leahevy/cutyx/actions/workflows/style.yml/badge.svg" alt="Coding style"/></a>
<a href="https://github.com/leahevy/cutyx/actions/workflows/format.yml"><img src="https://github.com/leahevy/cutyx/actions/workflows/format.yml/badge.svg" alt="Formatting checks"/></a>
<a href="https://github.com/leahevy/cutyx/actions/workflows/typechecks.yml"><img src="https://github.com/leahevy/cutyx/actions/workflows/typechecks.yml/badge.svg" alt="Typechecks"/></a>
<a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="GPLv3"/></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Made with Python"/></a>
<a href="https://www.linux.org/"><img src="https://img.shields.io/badge/OS-Linux-green" alt="Running on Linux"/></a>
<a href="https://www.apple.com/"><img src="https://img.shields.io/badge/OS-MacOS-green" alt="Running on MacOS"/></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Formatted with black"/></a>
<a href="https://opensource.fb.com/support-ukraine"><img src="https://img.shields.io/badge/Support-Ukraine-FFD500?style=flat&labelColor=005BBB" alt="Support Ukraine"/></a>
</p>
  
---

## 💫 [CutyX](https://github.com/leahevy/cutyx)

Tool to organise your image gallery using machine learning.

To get an overview how **CutyX** can be used, see the examples in the [documentation](https://leahevy.de/cutyx/cutyx/examples.html).

A simple usage is shown below:

```bash
cutyx match faces /path/to/some/image.jpg albums/some-album
cutyx run
```

This will register similar faces as in `image.jpg` to be automatically sorted into the `albums/some-album` directory. The second command will do the actual sorting (copying or symlinking).

[The source for this project is available here.](https://github.com/leahevy/cutyx)

---

## 💿 Installation

To install it with pip run: `pip install cutyx`.

To install this package locally for development, clone it first using `git clone https://github.com/leahevy/cutyx` and run: `pip install -e .[dev]`.

For installation of the latest version you can install it with pip directly from *GitHub* with the command: `pip install git+https://github.com/leahevy/cutyx.git`.

---

## 💡 Shell completion

For shell completion run one of the appropriate commands:

- `cutyx --install-completion=bash`
- `cutyx --install-completion=zsh`
- `cutyx --install-completion=fish`

---

## ⌨️ Commands

The following commands are available:

<dl>
  <dt><strong>run</strong></dt>
  <dd>Process images anywhere in a directory hierarchy.</dd>
  <dt><strong>process-image</strong></dt>
  <dd>Process a single image</dd>
  <dt><strong>match</strong></dt>
  <dd>Group of commands to register matching conditions for album directories.</dd>
  <dt><strong>update-cache</strong></dt>
  <dd>Generates or updates the cache for processed images.</dd>
  <dt><strong>clear-cache</strong></dt>
  <dd>Clears the local cache.</dd>
</dl>

---

## 📖 Documentation

The documentation is available at <https://leahevy.github.io/cutyx>.

---

## 👥 Contributing

Want to add a contribution to **CutyX**? Feel free to send a [pull request](https://github.com/leahevy/cutyx/compare).

See also [here](https://github.com/leahevy/cutyx/blob/master/CONTRIBUTING.md).

---

## 🎓 License

Copyright (C) 2022 Leah Lackner

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
