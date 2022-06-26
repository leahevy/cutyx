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

PROJECT_NAME = cutyx
PACKAGE_NAME := $(subst -,_,$(PROJECT_NAME))

FILES = ./$(PACKAGE_NAME) ./tests ./setup.py

WORKDIR_CLEAN = @git diff --quiet --exit-code || { echo "Workdir not clean"; exit 1; } && \
					git diff --cached --quiet --exit-code || { echo "Uncommited staged changes"; exit 1; }

TAG_LAST_COMMIT = $(shell git describe --exact-match HEAD 2>/dev/null)

.PHONY: all
all: help

.PHONY: help
help: ## Prints the help
	@$(MAKE) list-commands

.PHONY: list-commands
list-commands:
	@echo "Project: $(PROJECT_NAME)"
	@echo "  Available commands:"
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST) | sort | sed '/^help.*/d' | sed 's/^/   - /g'

.PHONY: install
install: ## Installs the package
	pip install .

.PHONY: install-dev
install-dev: ## Installs the package with '-e' for local development
	pip install -e .[dev]
	pre-commit install

.PHONY: install-dev-noprecommit
install-dev-noprecommit:
	pip install -e .[dev]

.PHONY: format
format: ## Formats the code
	isort $(FILES)
	@echo
	black $(FILES)
	@echo

.PHONY: check-format
check-format: ## Checks the formatting
	isort --check $(FILES)
	@echo
	black --check $(FILES)
	@echo

.PHONY: check-style
check-style: ## Checks the style
	flake8 $(FILES)
	@echo

.PHONY: check-types
check-types: ## Checks the types (typechecks)
	mypy $(FILES)
	@echo

.PHONY: test
test: ## Runs the unittests and doctests
	pytest $(subst ./setup.py,,$(FILES))
	coverage html
	@echo

.PHONY: virtualenv-create
virtualenv-create: ## Creates a new virtualenv
	@rm -rf .venv
	@python -m venv .venv
	@echo "! Run 'source ./.venv/bin/activate' to enable the environment !"

.PHONY: build
build: ## Builds the package
	@rm -rf dist
	python -m build .
	@echo

.PHONY: clean
clean: ## Cleans the working directory
	@git clean -fdX

.PHONY: make-docs
make-docs: ## Generates the documentation
	pdoc -o docs --math ./$(PACKAGE_NAME)

.PHONY: serve-docs
serve-docs: ## Serves the documentation (Opens in a browser)
	pdoc --math ./$(PACKAGE_NAME)

.PHONY: upload-pypi-public
upload-pypi-public: ## Builds and uploads the package to pypi (public repository)
	@$(MAKE) -- --run-upload-pypi-public

.PHONY: --run-upload-pypi-public
--run-upload-pypi-public: build
	twine upload dist/*

.PHONY: upload-pypi-test
upload-pypi-test: ## Builds and uploads the package to pypi (testpypi repository)
	@$(MAKE) -- --run-upload-pypi-test

.PHONY: --run-upload-pypi-test
--run-upload-pypi-test: build
	twine upload --repository testpypi dist/*

.PHONY: pre-commit-check
pre-commit-check: ## Runs the pre-commit checks (format, types, style)
	@$(MAKE) run-pre-commit-check

.PHONY: run-pre-commit-check
run-pre-commit-check: check-format check-types check-style

.PHONY: all-checks
all-checks: ## Runs all checks (format, types, style, build, test)
	@$(MAKE) run-all-checks

.PHONY: run-all-checks
run-all-checks: check-format check-types check-style build test

.PHONY: --do-release
--do-release:
	$(WORKDIR_CLEAN)
	@echo "Checking if the last commit is tagged..."
	@[ "$(TAG_LAST_COMMIT)" = "" ] && exit 1 || true
	@gitchangelog > CHANGELOG.md
	@egrep -q "^(unreleased)" CHANGELOG.md && { echo "Unreleased changes..."; git checkout CHANGELOG.md; exit 1; } || true
	@egrep -v "^\s*- Bump version:.*" CHANGELOG.md > CHANGELOG.md.2
	@rm CHANGELOG.md
	@mv CHANGELOG.md.2 CHANGELOG.md
	@egrep -v "^\s*- Release: version .*" CHANGELOG.md > CHANGELOG.md.2
	@rm CHANGELOG.md
	@mv CHANGELOG.md.2 CHANGELOG.md
	@git add CHANGELOG.md
	@git commit --amend -s -m "Release: version $(TAG_LAST_COMMIT)"
	@git tag -d "$(TAG_LAST_COMMIT)"
	@git tag -as "$(TAG_LAST_COMMIT)" -m "Release: version $(TAG_LAST_COMMIT)"
	@echo
	@echo "Created release commit for version `git describe --exact-match HEAD`"
	@echo "Push the new release with 'git push --follow-tags'"

.PHONY: release-major
release-major: ## Releases a new major version
	@$(MAKE) -- --run-release-major

.PHONY: --run-release-major
--run-release-major:
	$(WORKDIR_CLEAN)
	@if ! command -v gitchangelog &> /dev/null; then echo "Install dev requirements first" >&2; exit 1; fi
	bump2version major
	@$(MAKE) -- --do-release

.PHONY: release-minor
release-minor: ## Releases a new minor version
	@$(MAKE) -- --run-release-minor

.PHONY: --run-release-minor
--run-release-minor:
	$(WORKDIR_CLEAN)
	@if ! command -v gitchangelog &> /dev/null; then echo "Install dev requirements first" >&2; exit 1; fi
	bump2version minor
	@$(MAKE) -- --do-release

.PHONY: release-patch
release-patch: ## Releases a new patch version
	@$(MAKE) -- --run-release-patch

.PHONY: --run-release-patch
--run-release-patch:
	$(WORKDIR_CLEAN)
	@if ! command -v gitchangelog &> /dev/null; then echo "Install dev requirements first" >&2; exit 1; fi
	bump2version patch
	@$(MAKE) -- --do-release