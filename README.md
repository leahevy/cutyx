<div align="center">
<a href="https://github.com/leahevy/template-python-project"><img src="https://raw.githubusercontent.com/leahevy/template-python-project/master/assets/template-python-project.png" width="350px" alt="template-python-project"/></a>
</div>
<br/>

<p align="center">
<b>✨ Template repository for Python projects. ✨</b> 
</p>

<p align="center">
<a href="https://github.com/leahevy/template-python-project/graphs/commit-activity"><img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" alt="This project is maintained"/></a>
<a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="GPLv3"/></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Made with Python"/></a>
<a href="https://www.linux.org/"><img src="https://svgshare.com/i/Zhy.svg" alt="Running on Linux"/></a>
<a href="https://www.apple.com/"><img src="https://svgshare.com/i/ZjP.svg" alt="Running on MacOS"/></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Formatted with black"/></a>
<a href="https://opensource.fb.com/support-ukraine"><img src="https://img.shields.io/badge/Support-Ukraine-FFD500?style=flat&labelColor=005BBB" alt="Support Ukraine"/></a>
</p>

> **HOW TO USE THIS TEMPLATE:** go to <https://github.com/leahevy/template-python-project/generate> to generate a new repository using this template. After that run the provided `./configure-template.sh` script.
  
---

## 💫 [Template Python Project](https://github.com/leahevy/template-python-project)

A Python project template.

This is a fully configured project template for Python with features like API documentation generation using **pdoc** and a full set of *GitHub* workflows which will run on each push to test and check the code, generate test coverage badges, etc.

---

## ✍️ Configure

To configure the template for your project run `./configure-template.sh`,
modify the *README.md* file, and replace the *./assets/template-python-project.png* logo (the logo is generated with a script of mine, provided [here](https://github.com/leahevy/dev/blob/master/python/leahevy/cmds/gen_project_banner.py)).

---

## ✨ Features

- Script (*./configure-template.sh*) to change the file/directory names and references from the template repository to your new repository.
- Example command with main function and argument parsing using *typer*.
- Testing with pytest with coverage report and evaluating doctests (a configurable package shortcut import is injected into the doctest namespace as well).
- GitHub workflows for testing the *build*, *pytest*, *format*, *typechecks*, *style*, and generating a *coverage* svg on each push to **master**.
- GitHub workflow for automatic **pypa** publishing (disabled per default).
- GitHub Issue templates and Code-of-Conduct using issue forms.
- Documentation generated and published on GitHub pages using **pdoc**.
- Configured toolchain including *flake8*, *mypy*, *pytest*, *black*, and *isort*.
- *bumpversion* for version updating.
- *editorconfig* file with defaults suitable to PEP expectations (e.g. line length: 79).
- *dependabot* for dependency management.
- *pre-commit* is ready to use.
- *CONTRIBUTING.md* template.

---

## 📖 Documentation

To setup the documentation page, just push to your repository and wait for the *documentation* workflow to finish. After that, setup [GitHub-Pages](https://github.com/leahevy/template-python-project/settings/pages) by setting the branch to **documentation** and the directory to **docs**. Optionally check the **Enforce HTTPS** checkbox.

---

## 👥 Contributing

Want to add a contribution to **template-python-project**? Feel free to send a [pull request](https://github.com/leahevy/template-python-project/compare).

See also [here](https://github.com/leahevy/template-python-project/blob/master/CONTRIBUTING.md).

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
