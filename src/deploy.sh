#!/bin/zsh

set -e

python3 src/build.py clean
python3 src/build.py build

msg="build: $(date '+%Y-%m-%d')"
git add .
git commit -m "$msg"
git push