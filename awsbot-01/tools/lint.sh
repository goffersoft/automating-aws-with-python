#! /bin/sh

echo `pwd`

echo
echo
echo "********* pycodestyle *********"
pycodestyle *.py
echo "********* pycodestyle *********"
echo
echo
echo "********* pydocstyle *********"
pydocstyle *.py
echo "********* pydocstyle *********"
echo
echo
echo "********* pyflakes *********"
pyflakes *.py
echo "********* pyflakes *********"
