# https://realpython.com/pypi-publish-python-package/

# https://packaging.python.org/distributing/

## update version number in pyproject.toml

### BUILDING THE PACKAGE

python -m build

### check contents

tar -xvf dist/mpytools-0.0.4.tar.gz

### LOCAL INSTALL

pip install $MPYTOOLS/dist/mpytools-0.0.4-py3-none-any.whl

### UPLOAD

python -m twine upload dist/*-0.0.22*

### deps:

sys
re
subprocess
time
curses
os
math
json
emoji
numpy
matplotlib
cycler
string
mpl_toolkits
plotly
