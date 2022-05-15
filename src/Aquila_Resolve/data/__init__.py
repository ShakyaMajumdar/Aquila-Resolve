import sys

if sys.version_info < (3, 9):
    # In Python versions below 3.9, this is needed
    from importlib_resources import files
else:
    # Since python 3.9+, importlib.resources.files is built-in
    from importlib.resources import files


DATA_PATH = files(__name__)
