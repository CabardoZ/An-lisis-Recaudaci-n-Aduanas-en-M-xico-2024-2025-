# -*- coding: utf-8 -*-
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# ========== CARGA DE DATOS ==========
ruta_panel = "Panel_Esfuerzo_Recaudatorio.xlsx"  # archivo en la raíz del repo
panel = pd.read_excel(ruta_panel)
panel.columns = panel.columns.str.lower()  # latitud y longitud quedan en minúsculas

# Listas únicas
impuestos = panel['impuesto'].unique().tolist()
años = panel['año'].unique().tolist()

# Meses en orden
orden_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
               "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
panel['mes'] = pd.Categorical(panel['mes'], categories=orden_meses, ordered=True)
meses = panel['mes'].cat.categories.tolist()

# ========== COLORES ==========
color_principal = '#9F2241'
colores_comparativo = ['#9F2241', '#691C32', '#BC955C', '#DDC9A3']

# ========== CONFIGURACIÓN DE LA APP ==========
app = dash.Dash(__name__)
server = app.server   # <-- para gunicorn

app.layout = html.Div(
    style={'backgroundColor': '#f9f9f9','padding': '30px','fontFamily': 'Montserrat Light, sans-serif'},
    children=[
        html.Div(
            style={'display': 'flex','justifyContent': 'flex-start','alignItems': 'center','marginBottom': '30px',
                   'padding': '20px','backgroundColor': color_principal,'borderRadius': '10px','color': 'white'},
            children=[
                html.Img(src='/assets/logo.png', style={'height': '140px', 'marginRight': '60px'}),
                html.H1("TABLERO ESFUERZO RECAUDATORIO ADUANAS EN MÉXICO", style={'margin': '0'})
            ]
        ),
        html.Div([
            html.Label('Selecciona Impuesto:'),
            dcc.Dropdown(id='dropdown-impuesto',
                         options=[{'label': imp, 'value': imp} for imp in impuestos],
                         value=impuestos[0]),
            html.Label('Selecciona Año:'),
            dcc.Dropdown(id='dropdown-año',
                         options=[{'label': año, 'value': año} for año in años],
                         value=años[0]),
            html.Label('Selecciona Mes:'),
            dcc.Dropdown(id='dropdown-mes',
                         options=[{'label': mes, 'value': mes} for mes in meses],
                         value=None,
                         placeholder='Todos los meses')
        ], style={'width': '50%','margin': 'auto','marginBottom': '20px'}),

        dcc.Graph(id='grafico-recaudacion'),
        # … (el resto de sus divs y gráficos tal como ya los tiene)
    ]
)

# ========== CALLBACK ==========
@app.callback(
    # salidas ...
)
def update_graphs(impuesto, año, mes):
    # … (misma lógica que ya tiene)
    return fig_barras, fig_linea, fig_var, fig_pie_2024, fig_pie_2025, fig_top10, fig_serie, fig_mapa

# ========== EJECUCIÓN ==========
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
