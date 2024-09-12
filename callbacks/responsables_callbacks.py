from dash import Input, Output, State, dash_table, html
import plotly.express as px
import pandas as pd
from app import app  # Importar la instancia de la aplicación desde app.py
from utils.data_loader import run_query
from sqlalchemy import text


