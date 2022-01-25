from dash import html, dcc, Dash, Output, Input
import dash_bootstrap_components as dbc
from flask import send_from_directory
import plotly.express as px
import os  # TODO: use PathLib

ASSETSDIR = os.path.join(os.path.dirname(__file__), "packagedassets")

fig = px.bar(x=[1, 2, 3, 4, 5], y=[10, 10, 5, 6, 12])


class Shimmer(dcc.Loading):  # TODO: spinner briefly appears before stylesheets load
    def __init__(self, *args, show_spinner=False, **kwargs):
        shimmerclass = "shimmer" if show_spinner else "shimmer no-dash-spinner"
        parent_className = kwargs.pop("parent_className", shimmerclass)
        super().__init__(*args, parent_className=parent_className, **kwargs)


# inject the CSS?


def local_css(app: Dash, *, path: os.PathLike):
    endpoint = app.get_relative_path("/shimmerstylesheet")

    if (
        "serve_shimmer_stylesheet" not in app.server.view_functions
        and endpoint not in app.server.url_map.iter_rules()
    ):

        @app.server.route(endpoint)
        def serve_shimmer_stylesheet():
            return send_from_directory(directory=ASSETSDIR, path=path)

    return html.Link(rel="stylesheet", href=endpoint)


# Little App

app = Dash()
app.layout = html.Div(
    [
        local_css(app=app, path="shimmer.css"),
        html.H1("Hello"),
        dbc.Button("Click me!", type="submit", id="button"),
        Shimmer(
            dcc.Graph(figure=fig, id="graph"),
        ),
    ]
)


@app.callback(Output("graph", "figure"), Input("button", "n_clicks"))
def update_graph(click):
    import time

    time.sleep(2)  # something long to bring out the shimmer
    return fig


app.run_server()
