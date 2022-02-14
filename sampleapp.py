from dash import html, dcc, Dash, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

import dash_loading_extras as loading

fig = px.bar(x=[1, 2, 3, 4, 5], y=[10, 10, 5, 6, 12])

# Little App
app = Dash()
app.layout = html.Div(
    [
        html.H1("Hello"),
        dbc.Button("Click me!", type="submit", id="button"),
        loading.Shimmer(dcc.Graph(figure=fig, id="graph"), app=app),
    ]
)


@app.callback(Output("graph", "figure"), Input("button", "n_clicks"))
def update_graph(click):
    # simulate something timeful
    import time

    time.sleep(2)  # something long to bring out the shimmer
    return fig


server = app.server
if __name__ == "__main__":
    app.run_server(debug=True)

if __name__ != "__main__":
    import logging

    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
