#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

cd "$(dirname "$0")"
SCRIPT_NAME="$(basename "$0")"


# VALUES OF THIS TEMPLATE PROJECT
#################################
VERSION="0.40.0"
THIS_PROJECT_NAME="template-python-project"
THIS_PACKAGE_NAME="${THIS_PROJECT_NAME//-/_}" 
THIS_AUTHOR="Leah Lackner"
THIS_AUTHOR_EMAIL="leah.lackner+github@gmail.com"
THIS_AUTHOR_GITHUB_HANDLE="leahevy"
THIS_PROJECT_COPYRIGHT_YEAR="2022"
THIS_DESCRIPTION="Template repository for Python projects\."
THIS_PYTHON_VERSION="3.10"


# DEFAULT VALUES
################
DEFAULT_USER_NAME="$THIS_AUTHOR"
DEFAULT_USER_MAIL="$THIS_AUTHOR_EMAIL"
DEFAULT_GITHUB_HANDLE="$THIS_AUTHOR_GITHUB_HANDLE"
DEFAULT_PYTHON_VERSION="$THIS_PYTHON_VERSION"
DEFAULT_VERSION="0.0.1"


# COLORS
################
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
ENDCOLOR="\e[0m"


# Read user data
################
printf "${GREEN}Provide the following information:${ENDCOLOR}\n"
printf "${GREEN}----------------------------------${ENDCOLOR}\n"

printf "${YELLOW}Python project name (required):${ENDCOLOR} "
read PYTHON_PROJECT_NAME
if [ "${PYTHON_PROJECT_NAME}" = "" ]; then
    printf "  ${RED}+ Project name required${ENDCOLOR}\n" 1>&2
    exit 1
fi
PYTHON_PROJECT_NAME="${PYTHON_PROJECT_NAME//_/-}" 
PYTHON_PROJECT_NAME="$(echo "$PYTHON_PROJECT_NAME" | tr '[:upper:]' '[:lower:]')"

printf "${YELLOW}Minimum Python version to support [$DEFAULT_PYTHON_VERSION]: ${ENDCOLOR}"
read PYTHON_VERSION
if [ "${PYTHON_VERSION}" = "" ]; then
    PYTHON_VERSION="$DEFAULT_PYTHON_VERSION"
fi

printf "${YELLOW}Your full name [$DEFAULT_USER_NAME]: ${ENDCOLOR}"
read USER_NAME
if [ "${USER_NAME}" = "" ]; then
    USER_NAME="$DEFAULT_USER_NAME"
fi

printf "${YELLOW}Your mail [$DEFAULT_USER_MAIL]: ${ENDCOLOR}"
read USER_MAIL
if [ "${USER_MAIL}" = "" ]; then
    USER_MAIL="$DEFAULT_USER_MAIL"
fi

printf "${YELLOW}Your GitHub handle [$DEFAULT_GITHUB_HANDLE]: ${ENDCOLOR}"
read GITHUB_HANDLE
if [ "${GITHUB_HANDLE}" = "" ]; then
    GITHUB_HANDLE="$DEFAULT_GITHUB_HANDLE"
fi

DEFAULT_PYTHON_PACKAGE_NAME="$PYTHON_PROJECT_NAME" 
DEFAULT_PYTHON_PACKAGE_NAME="${DEFAULT_PYTHON_PACKAGE_NAME//-/_}" 
DEFAULT_PYTHON_PACKAGE_NAME="$(echo "$DEFAULT_PYTHON_PACKAGE_NAME" | tr '[:upper:]' '[:lower:]')"
printf "${YELLOW}Python package name [$DEFAULT_PYTHON_PACKAGE_NAME]: ${ENDCOLOR}"
read PYTHON_PACKAGE_NAME
if [ "${PYTHON_PACKAGE_NAME}" = "" ]; then
    PYTHON_PACKAGE_NAME="${PYTHON_PROJECT_NAME}"
fi
PYTHON_PACKAGE_NAME="${PYTHON_PACKAGE_NAME//-/_}" 
PYTHON_PACKAGE_NAME="$(echo "$PYTHON_PACKAGE_NAME" | tr '[:upper:]' '[:lower:]')"

DEFAULT_PYTHON_PACKAGE_DESCRIPTION="The $PYTHON_PROJECT_NAME package." 
printf "${YELLOW}Python package description [$DEFAULT_PYTHON_PACKAGE_DESCRIPTION]: ${ENDCOLOR}"
read PYTHON_PACKAGE_DESCRIPTION
if [ "${PYTHON_PACKAGE_DESCRIPTION}" = "" ]; then
    PYTHON_PACKAGE_DESCRIPTION="${DEFAULT_PYTHON_PACKAGE_DESCRIPTION}"
fi

DEFAULT_PYTHON_PACKAGE_SHORT_NAME="tp" 
printf "${YELLOW}Short package import name (e.g. pd for pandas) [$DEFAULT_PYTHON_PACKAGE_SHORT_NAME]: ${ENDCOLOR}"
read PYTHON_PACKAGE_SHORT_NAME
if [ "${PYTHON_PACKAGE_SHORT_NAME}" = "" ]; then
    PYTHON_PACKAGE_SHORT_NAME="${DEFAULT_PYTHON_PACKAGE_SHORT_NAME}"
fi

printf "${GREEN}----------------------------------${ENDCOLOR}\n"

# Functions
##########################
titlecase() {
    printf "%s" "$1" | awk '{for(j=1;j<=NF;j++){ $j=toupper(substr($j,1,1)) substr($j,2) }}1'
}

replace-words() {
    printf "${GREEN}Replace words ('$1' -> '$2')...${ENDCOLOR}\n"
    find . -type f -not -path "*$SCRIPT_NAME" -not -path "*.venv/*" -not -path "*.git/*" -not -path "*__pycache__*" -not -path "*.egg-info*" -not -path "*.png" | xargs -n 1 perl -pi -e "s,$1,$2,g" || true
}

rename-files() {
    printf "${GREEN}Rename files and folders ('$1' -> '$2')...${ENDCOLOR}\n"
    find . -type d -not -path "*__pycache__*" -not -path "*.venv/*" -not -path "*.egg-info*" | grep "$1" | sed -n "s/\(.*\)$1\(.*\)/& \1$2\2/p" | xargs -n 2 mv || true
    find . -type f -not -path "*__pycache__*" -not -path "*.venv/*" -not -path "*.egg-info*" | grep "$1" | sed -n "s/\(.*\)$1\(.*\)/& \1$2\2/p" | xargs -n 2 mv || true
}

# Process variables
##########################
USER_MAIL="${USER_MAIL//@/\@}" 
USER_MAIL="$(echo "$USER_MAIL" | tr '[:upper:]' '[:lower:]')"
THIS_AUTHOR_EMAIL_QUOTED="$(echo "$THIS_AUTHOR_EMAIL" | sed 's/\./\\\./g' | sed 's/+/\\\+/g' | sed 's/@/\\\@/g')"
CURRENT_YEAR="$(date +'%Y')"
VERSION_QUOTED="$(echo "$VERSION" | sed 's/\./\\\./g' | sed 's/+/\\\+/g' | sed 's/@/\\\@/g')"
THIS_PYTHON_VERSION_QUOTED="$(echo "$THIS_PYTHON_VERSION" | sed 's/\./\\\./g' | sed 's/+/\\\+/g' | sed 's/@/\\\@/g')"
PYTHON_PROJECT_TITLE_NAME="${PYTHON_PROJECT_NAME//-/ }"
PYTHON_PROJECT_TITLE_NAME="$(titlecase "$PYTHON_PROJECT_TITLE_NAME")"
THIS_PYTHON_PROJECT_TITLE_NAME="${THIS_PROJECT_NAME//-/ }"
THIS_PYTHON_PROJECT_TITLE_NAME="$(titlecase "$THIS_PYTHON_PROJECT_TITLE_NAME")"


# Rename folders and files
##########################
rename-files "$THIS_PROJECT_NAME" "$PYTHON_PROJECT_NAME"
rename-files "$THIS_PACKAGE_NAME" "$PYTHON_PACKAGE_NAME"


# Replace words
###############
replace-words "$THIS_PROJECT_NAME" "$PYTHON_PROJECT_NAME"
replace-words "$THIS_PACKAGE_NAME" "$PYTHON_PACKAGE_NAME"
replace-words "$THIS_DESCRIPTION" "$PYTHON_PACKAGE_DESCRIPTION"
replace-words "$THIS_AUTHOR" "$USER_NAME"
replace-words "$THIS_AUTHOR_GITHUB_HANDLE" "$GITHUB_HANDLE"
replace-words "$THIS_AUTHOR_EMAIL_QUOTED" "$USER_MAIL"
replace-words "Copyright \(C\) $THIS_PROJECT_COPYRIGHT_YEAR" "Copyright (C) $CURRENT_YEAR"
replace-words "\"tp\"" "\"$PYTHON_PACKAGE_SHORT_NAME\""
replace-words "$VERSION_QUOTED" "$DEFAULT_VERSION"
replace-words "$THIS_PYTHON_VERSION_QUOTED" "$PYTHON_VERSION"
replace-words "$THIS_PYTHON_PROJECT_TITLE_NAME" "$PYTHON_PROJECT_TITLE_NAME"


# Re-Format
###########
black -l 79 . || true
isort -l 79 . || true


# Exchange Readmes
#############
rm -f ./README.md
mv ./README-template.md ./README.md || true


# Remove changelog
##################
rm -f ./CHANGELOG.md


# Fix bumpversion
#################
sed '/configure-template.sh/d' ./.bumpversion.cfg > ./.bumpversion.cfg.2
rm -f "./.bumpversion.cfg"
mv "./.bumpversion.cfg.2" "./.bumpversion.cfg"


# Delete self
#############
rm -f "./$SCRIPT_NAME"


# Git add
#########
git add . || true
