import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Initialize the Dash app with dark theme
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.DARKLY],
                use_pages=True)

# Custom CSS for the app
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #000000;
                color: #3498db;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .dash-dropdown .Select-control {
                background-color: #111111;
                color: #3498db;
                border-color: #3498db;
            }
            .dash-dropdown .Select-menu-outer {
                background-color: #111111;
                color: #3498db;
            }
            .dash-dropdown .Select-value-label {
                color: #3498db !important;
            }
            .dash-dropdown .Select-placeholder {
                color: #3498db !important;
            }
            .card {
                background-color: #111111;
                border: 1px solid #3498db;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 0 15px rgba(52, 152, 219, 0.3);
            }
            .nav-link {
                color: #3498db !important;
            }
            .nav-link.active {
                background-color: #3498db !important;
                color: #000000 !important;
            }
            .btn-primary {
                background-color: #3498db;
                border-color: #3498db;
            }
            .btn-primary:hover {
                background-color: #2980b9;
                border-color: #2980b9;
            }
            h1, h2, h3, h4, h5 {
                color: #3498db;
            }
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table {
                background-color: #111111;
                color: #3498db;
            }
            .dash-spinner * {
                background-color: #3498db !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define the navbar
# Define the navbar
navbar = html.Div(
    [
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Predictor", href="/predictor")),
                dbc.NavItem(dbc.NavLink("Results", href="/results")),
                dbc.NavItem(dbc.NavLink("Data Explorer", href="/explorer")),
                dbc.NavItem(dbc.NavLink("FindDoc", href="/findDoc")),
                dbc.NavItem(dbc.NavLink("DocChat", href="/chat")),
            ],
            brand=html.Span([
                html.Img(
                    src="/assets/logo.png",
                    height="40px",
                    style={"marginRight": "10px"}
                ),
                html.Span("ChildHealth_AI", style={"color": "white", "fontWeight": "bold", "fontSize": "1.25rem"})
            ], style={"display": "flex", "alignItems": "center"}),
            brand_href="/",
            color="lightblack",  # Assuming this is custom defined in CSS
            dark=True,
            className="mb-0",
        ),
        html.Hr(style={"borderTop": "1px solid white", "marginTop": "0", "marginBottom": "1rem"}),
    ],
    className="mb-4"
)


# Define the layout for the app
app.layout = html.Div([
    # URL Location component for page navigation
    dcc.Location(id='url', refresh=False),
    
    # Navbar and page container
    navbar,
    dash.page_container
])

# Register pages
import pages.home
import pages.predictor
import pages.explorer
import pages.about
import pages.results
import pages.find_doc
import pages.doc_chat 

# Run the app
if __name__ == '__main__':
    app.run(debug=True)