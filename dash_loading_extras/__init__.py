from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("dash_loading_extras")
except PackageNotFoundError:
    # package is not installed
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)
