#!/bin/bash

git clone "https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.module_name }}.git" tempdir/
cd tempdir || return 1
mv ./* ../
mv ./.[!.]* ../
# shellcheck disable=SC2103
cd .. || return 1
git checkout -b cookiecutter
rmdir tempdir
git add -A
git commit -m "Repository template"
git push --set-upstream origin cookiecutter
hub pull-request --no-edit
