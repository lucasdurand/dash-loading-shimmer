# dash-loading-shimmer

[![PyPI version](https://badge.fury.io/py/dash-loading-extras.svg)](https://badge.fury.io/py/dash-loading-extras)


A shimmer pre-load component for Plotly Dash. Check out [sampleapp.py](sampleapp.py) for a *very* minimal example.

![Simple Shimmer Example](simpleshimmer.gif)

## Installation

Get it with **pip**: `pip install dash-loading-extras`

Or maybe you prefer **uv**: `uv add dash-loading-extras`

## Usage

See [sampleapp.py](sampleapp.py) for a simple Dash app example, or use `Shimmer` like you would a `dcc.Loading` component. Wrap it around any components you want to shimmer while loading and don't stop 'til morning.

```python
from dash import Dash, html, dcc
import dash_loading_extras as loading
app = Dash()
app.css.config.serve_locally=True

app.layout = html.Div([
    html.H1("A Long Loading Graph"),
    html.H2("It's worth the wait!"),
    loading.Shimmer(
        dcc.Graph(figure=fig, id="graph"),
        app=app,
        # show_spinner=True # optionally keep the loading animation on top of the shimmering element
    ),
])

app.run()
```

If you want to tweak the CSS used, inject your own CSS before `Shimmer` gets there with the `shimmer_css` function. Common styles to tweak are the opacity, hue, and speed of the shimmer

```python
import dash_loading_extras as loading
app = Dash()

loading.ASSETSDIR = "path/to/your/cssassets/folder"
loading.shimmer_css(app=app, path="my_better_shimmer.css")

app.layout = ...

```

## Deploying the sample app

[sampleapp.py](sampleapp.py) runs on [Google App Engine](https://cloud.google.com/appengine/docs/standard/python3) standard (F1 instance, scales to zero, within the free tier), as the `dash-loading-shimmer` service. App Engine installs from `requirements.txt` and imports `dash_loading_extras` straight from the source tree.

1. Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install), then `gcloud init` and pick your project
1. If you changed dependencies, regenerate `requirements.txt`: `uv export --no-dev --group sampleapp --no-emit-project --no-hashes -o requirements.txt`
1. Deploy with `gcloud app deploy`
1. View it with `gcloud app browse -s dash-loading-shimmer`

App Engine requires a project's first service to be `default`, so in a brand new project remove the `service:` line from `app.yaml` for the first deploy.

## Future Work

Open to ideas! So far there's:

* Customize shimmer styles (programmatically generating CSS at runtime)
* More loaders (spinning, bouncing, erupting?)
* Remove need to pass `app` into `Shimmer` call
