from dash import Dash
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
load_dotenv()

# Definir los estilos externos
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://use.fontawesome.com/releases/v5.15.1/css/all.css",
]

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.title = "ESTADISTICAS-DSLD"
# Configurar el favicon
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
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


server = app.server
