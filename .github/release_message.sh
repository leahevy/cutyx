#!/bin/bash
current_tag="$(git tag --sort=-creatordate | head -n 1)"
previous_tag="$(git tag --sort=-creatordate | sed -n 2p)"


echo "## Version ${current_tag}"
echo
echo "### Project links"
echo
echo "- Source code: <https://github.com/leahevy/template-python-project/tree/$current_tag>"
echo "- Release: <https://github.com/leahevy/template-python-project/releases/tag/$current_tag>"
echo "- Download: <https://github.com/leahevy/template-python-project/archive/refs/tags/$current_tag.zip>"
echo
echo "### Changelog"
echo
git shortlog -n "${previous_tag}.." |
    sed 's/^./    &/' |
    sed 's/ ([[:digit:]][[:digit:]]*)://g' |
    sed '/\s*Release: version /d' |
    sed '/\s*Bump version: /d' |
    sed 's/^    //g' |
    sed 's/^\([^ ]\)/#### \1/g' |
    sed 's/^  */- /g'