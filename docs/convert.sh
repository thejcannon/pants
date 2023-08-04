#!/usr/bin/env bash
set -eux

# 0. Start from a known state
git checkout -- docs/markdown
git clean -df docs/markdown



# - Rename dirs/files
#   - Introduction
mv docs/markdown/Introduction docs/markdown/introduction
#   - Getting Started
mv "docs/markdown/Getting Started" docs/markdown/getting-started
mv docs/markdown/getting-started/getting-started.md docs/markdown/getting-started/index.md
mv docs/markdown/getting-started/getting-started/*.md docs/markdown/getting-started
rm -rf docs/markdown/getting-started/getting-started
#   - Getting Help
mv "docs/markdown/Getting Help" docs/markdown/getting-help
mv docs/markdown/getting-help/the-pants-community.md docs/markdown/getting-help/the-pants-community/index.md
#   - Using Pants
mv "docs/markdown/Using Pants" docs/markdown/using-pants
# ... on and on and so forth



# - Manual Conversions. Do these before `prettier` so we don't have to worry about formatting
#   (NB: Media images should be hosted elsewhere, not readme.io)
python3 docs/convert.py

# - Convert using prettier to make simpler Markdown
#npx prettier --write docs/


# Finally, run with
# pants --concurrent run 3rdparty/python:mkdocs -- serve -f docs/mkdocs.yml

