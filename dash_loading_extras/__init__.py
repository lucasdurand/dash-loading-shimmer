from __future__ import annotations
import os  # TODO: use PathLib
from typing import TYPE_CHECKING
from importlib.metadata import version, PackageNotFoundError

from dash import html, dcc
from flask import send_from_directory

if TYPE_CHECKING:
    from dash import Dash


try:  # get version at importtime
    __version__ = version("dash_loading_extras")
except PackageNotFoundError:  # package is not installed
    try:
        from setuptools_scm import get_version

        __version__ = get_version(root="..", relative_to=__file__)
    except (ModuleNotFoundError, LookupError):  # deployed without package install
        __version__ = None

ASSETSDIR = os.path.join(os.path.dirname(__file__), "..", "packagedassets")


class Shimmer(dcc.Loading):
    """Display a pre-load shimmer over loading Dash components"""

    def __init__(self, children: list, *, app: Dash, show_spinner=False, **kwargs):
        shimmer_css(app=app, path="shimmer.css")
        shimmerclass = "shimmer" if show_spinner else "shimmer no-dash-spinner"
        parent_className = kwargs.pop("parent_className", shimmerclass)
        super().__init__(children=children, parent_className=parent_className, **kwargs)


def shimmer_css(app: Dash, *, path: os.PathLike = "shimmer.css"):
    endpoint = app.get_relative_path("/shimmerstylesheet")
    servedlocally = app.css.config.serve_locally

    if (
        "serve_shimmer_stylesheet" not in app.server.view_functions
        and endpoint not in app.server.url_map.iter_rules()
    ):

        @app.server.route(endpoint)
        def serve_shimmer_stylesheet():
            return send_from_directory(directory=ASSETSDIR, path=path)

        if servedlocally:
            app.css.append_css({"external_url": endpoint})
            app.css.config.serve_locally = (
                False  # this would be a common setting for PROD dashboards -- but
                # should we enforce it always? That would make this easier
                # and solve the slow load on CSS via html.Link
                # Consider raising an Exception here, requiring explicitly passing local=False
                # to the function or setting explictly in the app settings
            )

    return html.Div() if servedlocally else html.Link(rel="stylesheet", href=endpoint)
