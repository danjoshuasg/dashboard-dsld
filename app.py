from dash import Dash
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
load_dotenv()

# Definir los estilos externos
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://use.fontawesome.com/releases/v5.15.1/css/all.css"
]


app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.title = "DSLD-DASHBOARD"
server = app.server