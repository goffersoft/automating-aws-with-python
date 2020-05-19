#! /bin/sh

echo `pwd`

pycodestyle "$1"
pydocstyle "$1"
pyflakes "$1"
