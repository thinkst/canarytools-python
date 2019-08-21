#!/bin/bash
echo "-- uploading canarytools-python to pypi --"
pip list | grep -F twine > /dev/null
if [ $? -ne 0 ]; then
    echo "-! python package: twine wasn't found. !-"
    echo "-! check that you in a virtualenv      !-"
    exit 1
fi
echo "-- removing old packages from /dist --"
rm -R dist
echo "-- building new packages for pypi   --"
python setup.py sdist bdist_wheel
echo "-- uploading new package to pypi    --"
python -m twine upload dist/*
