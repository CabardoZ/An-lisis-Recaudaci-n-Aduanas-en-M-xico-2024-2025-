# -*- coding: utf-8 -*-
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# ========== CARGA DE DATOS ==========
ruta_panel = "Panel_Esfuerzo_Recaudatorio.xlsx"  # archivo en la raíz del repo
panel = pd.read_excel(ruta_panel)
panel.columns = panel.columns.str.lower()

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
server = app.server  # para gunicorn

app.layout = html.Div(
    style={'backgroundColor': '#f9f9f9','padding': '30px','fontFamily': 'Montserrat Light, sans-serif'},
    children=[

        # CABECERA
        html.Div(
            style={'display': 'flex','justifyContent': 'flex-start','alignItems': 'center','marginBottom': '30px',
                   'padding': '20px','backgroundColor': color_principal,'borderRadius': '10px','color': 'white'},
            children=[
                html.Img(src='/assets/logo.png', style={'height': '140px', 'marginRight': '60px'}),
                html.H1("TABLERO ESFUERZO RECAUDATORIO ADUANAS EN MÉXICO", style={'margin': '0'})
            ]
        ),

        # CONTROLES
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

        # GRÁFICO 1
        html.Div([
            html.H3("Recaudación por Aduana", style={'color': color_principal, 'textAlign': 'center'}),
            html.P("Con el menú de selección superior, puede consultar la recaudación por Aduana en las 50 distribuidas en México por impuesto, mes y año.", style={'textAlign': 'center'}),
            dcc.Graph(id='grafico-recaudacion')
        ], style={'width': '95%','border': f'2px solid {color_principal}','borderRadius': '10px','padding': '20px',
                  'backgroundColor': 'white','margin': 'auto','marginBottom': '30px'}),

        # GRÁFICO 2
        html.Div([
            html.H3("Evolución Mensual de la Recaudación", style={'color': color_principal, 'textAlign': 'center'}),
            html.P("En el presente gráfico se puede observar el comportamiento mensual de la recaudación por impuesto y año, seleccione Año e Impuesto en el menú superior para consultar.", style={'textAlign': 'center','marginBottom': '20px'}),
            dcc.Graph(id='grafico-mensual')
        ], style={'width': '95%','border': f'2px solid {color_principal}','borderRadius': '10px','padding': '20px',
                  'backgroundColor': 'white','margin': 'auto','marginBottom': '30px'}),

        # GRÁFICO 3
        html.Div([
            html.H3("Variación Mensual Total Enero–Julio 2024 vs 2025", style={'color': color_principal, 'textAlign': 'center'}),
            html.P("En cada uno de los meses mostrados, la recaudación de 2025 fue consistentemente mayor que en 2024.Esto indica una tendencia general de crecimiento en la recaudación interanual durante este período. La recaudación se mantuvo relativamente estable en los siete meses de ambos años, no obstante mostrando una tendencia creciente, siendo abril dónde se registró un pico crecimiento notable, además en este mes se presenta la mayo diferencia entre 2024 y 2025.Para 2024 se registró una recaudación en un rango de 170 a 205 millones de pesos y para 2025 en un rango entre 191 y 239 millones de pesos.", style={'textAlign': 'justify'}),
            dcc.Graph(id='grafico-variacion')
        ], style={'width': '95%','border': f'2px solid {color_principal}','borderRadius': '10px','padding': '20px',
                  'backgroundColor': 'white','margin': 'auto','marginBottom': '30px'}),

        # GRÁFICO 4 - PASTEL
        html.Div([
            html.H3("Distribución de Impuestos Reales Enero–Julio 2024 vs 2025",
                    style={'color': color_principal, 'textAlign': 'center'}),
            html.P("Ambos gráficos muestran la distribución porcentual de la recaudación real por impuestos para el periodo de enero a julio, comparado entre los años 2024 y 2025. En ambos años, el IVA es el impuesto que aporta la mayor parte de la recaudación total, seguido del IEPS y el IGI. La recaudación tuvo un cambio notable de 2024 a 2025, la dependencia del IVA disminuyó, de 72.6% (2024) a 67.8% (2025), por otro lado el IEPS aumentó de 13.3% (2024) a 17.9% (2025), los demás impuestos mantuvieron su peso porcentual en la recaudación en ambos años. Los datos nos sugieren que las políticas y condiciones ecónomicas en 2025 llevaron a una mayor recaudación del IEPS, diversificando ligeramente las fuentes de ingresos en comparación con 2024. ", style={'textAlign': 'justify'}),
            html.Div([
                dcc.Graph(id='grafico-pastel-2024', style={'width': '48%', 'display': 'inline-block'}),
                dcc.Graph(id='grafico-pastel-2025', style={'width': '48%', 'display': 'inline-block'})
            ])
        ], style={'width': '95%','border': f'2px solid {color_principal}','borderRadius': '10px','padding': '20px',
                  'backgroundColor': 'white','margin': 'auto','marginBottom': '30px'}),

        # GRÁFICO 5 - RANKING TOP 10
        html.Div([
            html.H3("Top 10 Aduanas por Recaudación Total", style={'color': color_principal, 'textAlign': 'center'}),
            html.P("Las aduanas ubicadas en las ciudades de Nuevo Laredo,Manzanillo, Veracruz y Lázaro Cardenas son las que obtuvieron mayor recaudación, con un rango entre 120 y 221 millones de pesos (2024) y 134 y 231 millones de pesos (2025), con una recaudación notablemente superior respecto al año anterior. En general, la recaudación total en 2025 fue significativamente mayor en 2025 que en 2024, por citar un ejemplo en Lázaro Cárdenas aumentó en terminos reales en 11.67 %. El aumento en las principales aduanas del país podría ser la causa principal en el aumento de los ingresos recaudatorios, cómo se observó en los gráficos anteriores.  ", style={'textAlign': 'justify'}),
            dcc.Graph(id='grafico-top10')
        ], style={'width': '95%','border': f'2px solid {color_principal}','borderRadius': '10px','padding': '20px',
                  'backgroundColor': 'white','margin': 'auto','marginBottom': '30px'}),

        # GRÁFICO 6 - SERIE TEMPORAL
        html.Div([
            html.H3("Serie Temporal Comparativa (2024 vs 2025)", style={'color': color_principal, 'textAlign': 'center'}),
            html.P("La recaudación de 2025 fue consistentemente superior a la del 2024 en el mismo periodo (enero-julio). El comportamiento de ambos años es similar, siguen un patrón similar de picos y valles en la recaudación, en marzo de ambos años denota una disminución, pero en abril se observa que alcanza su máximo valor en la recaudación, después la tendencia baja ligeramente para recuperarse en julio. En general la gráfica muestra una tendencia positiva en la recaudación de 2025, lo que indica un mejor desempeño fiscal respecto al 2024.", style={'textAlign': 'justify'}),
            dcc.Graph(id='grafico-serie')
        ], style={'width': '95%','border': f'2px solid {color_principal}','borderRadius': '10px','padding': '20px',
                  'backgroundColor': 'white','margin': 'auto','marginBottom': '30px'}),
  
        # GRÁFICO 7 - MAPA
        html.Div([
            html.H3("Mapa de Recaudación por Aduana", style={'color': color_principal, 'textAlign': 'center'}),
            html.P("Consulte en el mapa la recaudación por Aduana en todo el territorio nacional, seleccione en el menú superior el Año para visualizar.", style={'textAlign': 'center','marginBottom': '20px'}),
            dcc.Graph(id='grafico-mapa')
        ], style={'width': '95%','border': f'2px solid {color_principal}','borderRadius': '10px','padding': '20px',
                  'backgroundColor': 'white','margin': 'auto','marginBottom': '30px'}),
    ]
)

# ========== CALLBACK ==========

@app.callback(
    [Output('grafico-recaudacion', 'figure'),
     Output('grafico-mensual', 'figure'),
     Output('grafico-variacion', 'figure'),
     Output('grafico-pastel-2024', 'figure'),
     Output('grafico-pastel-2025', 'figure'),
     Output('grafico-top10', 'figure'),
     Output('grafico-serie', 'figure'),
     Output('grafico-mapa', 'figure')],
    [Input('dropdown-impuesto', 'value'),
     Input('dropdown-año', 'value'),
     Input('dropdown-mes', 'value')]
)
def update_graphs(impuesto, año, mes):
    df_filtrado = panel[(panel['impuesto'] == impuesto) & (panel['año'] == año)]
    if mes:
        df_filtrado = df_filtrado[df_filtrado['mes'] == mes]

    if df_filtrado.empty:
        empty_fig = {'data': [], 'layout': {'title': 'Sin datos'}}
        return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

    # Gráfico 1
    fig_barras = px.bar(df_filtrado, x='recaudación', y='aduana', color='mes', orientation='h',
                        color_discrete_sequence=colores_comparativo)
    fig_barras.update_layout(xaxis_title='Recaudación', yaxis_title='Aduana', template='plotly_white')

    # Gráfico 2
    df_mensual = (panel[(panel['impuesto'] == impuesto) & (panel['año'] == año)]
                  .groupby('mes', as_index=False)['recaudación'].sum())
    df_mensual['mes'] = pd.Categorical(df_mensual['mes'], categories=orden_meses, ordered=True)
    df_mensual = df_mensual.sort_values('mes')
    fig_linea = px.line(df_mensual, x='mes', y='recaudación', markers=True,
                        color_discrete_sequence=[color_principal])
    fig_linea.update_layout(xaxis_title='Mes', yaxis_title='Recaudación Total', template='plotly_white')

    # Gráfico 3
    df_var = (panel[(panel['mes'].isin(orden_meses[:7])) & (panel['año'].isin([2024, 2025]))]
              .groupby(['año', 'mes'], as_index=False)['recaudación'].sum())
    df_var['mes'] = pd.Categorical(df_var['mes'], categories=orden_meses[:7], ordered=True)
    df_var = df_var.sort_values(['mes', 'año'])
    df_var['año'] = df_var['año'].astype(str)
    fig_var = px.bar(df_var, x='mes', y='recaudación', color='año', barmode='group',
                     color_discrete_map={'2024': '#DDC9A3', '2025': '#9F2241'})
    fig_var.update_layout(xaxis_title='Mes', yaxis_title='Recaudación Total', template='plotly_white')

    # Gráfico 4 - Pastel
    meses_filtrar = orden_meses[:7]
    impuestos_real = ['iva_real', 'igi_real', 'dta_real', 'ieps_real', 'isan_real', 'otros_real']
    df_pie_2024 = (panel[(panel['año'] == 2024) & (panel['mes'].isin(meses_filtrar)) &
                         (panel['impuesto'].isin(impuestos_real))]
                   .groupby('impuesto', as_index=False)['recaudación'].sum())
    df_pie_2025 = (panel[(panel['año'] == 2025) & (panel['mes'].isin(meses_filtrar)) &
                         (panel['impuesto'].isin(impuestos_real))]
                   .groupby('impuesto', as_index=False)['recaudación'].sum())
    fig_pie_2024 = px.pie(df_pie_2024, names='impuesto', values='recaudación',
                          color_discrete_sequence=colores_comparativo)
    fig_pie_2024.update_traces(textinfo='percent+label')
    fig_pie_2025 = px.pie(df_pie_2025, names='impuesto', values='recaudación',
                          color_discrete_sequence=colores_comparativo)
    fig_pie_2025.update_traces(textinfo='percent+label')

    # Gráfico 5 - Top 10 Aduanas
    df_top10 = (panel[(panel['año'] == año) & (panel['mes'].isin(meses_filtrar))]
                .groupby('aduana', as_index=False)['recaudación'].sum()
                .nlargest(10, 'recaudación'))
    fig_top10 = px.bar(df_top10, x='recaudación', y='aduana', orientation='h',
                       color_discrete_sequence=[color_principal])
    fig_top10.update_layout(xaxis_title='Recaudación Total', yaxis_title='Aduana', template='plotly_white')

    # Gráfico 6 - Serie temporal
    df_serie = (panel[(panel['año'].isin([2024, 2025])) & (panel['mes'].isin(orden_meses[:7]))]
                .groupby(['año', 'mes'], as_index=False)['recaudación'].sum())
    df_serie['mes'] = pd.Categorical(df_serie['mes'], categories=orden_meses[:7], ordered=True)
    df_serie = df_serie.sort_values(['mes', 'año'])
    df_serie['año'] = df_serie['año'].astype(str)
    fig_serie = px.line(df_serie, x='mes', y='recaudación', color='año', markers=True,
                        color_discrete_map={'2024': '#DDC9A3', '2025': '#9F2241'})
    fig_serie.update_layout(xaxis_title='Mes', yaxis_title='Recaudación Total', template='plotly_white')

    # Gráfico 7 - MAPA
    df_mapa = panel[(panel['impuesto'] == impuesto) & (panel['año'] == año)]
    if mes:
        df_mapa = df_mapa[df_mapa['mes'] == mes]

    df_mapa_group = df_mapa.groupby(['aduana','latitud','longitud'], as_index=False)['recaudación'].sum()

    if df_mapa_group.empty:
        fig_mapa = {'data': [], 'layout': {'title': 'Sin datos para el mapa'}}
    else:
        fig_mapa = px.scatter_mapbox(
            df_mapa_group,
            lat='latitud',
            lon='longitud',
            hover_name='aduana',
            hover_data={'recaudación': True, 'latitud': False, 'longitud': False},
            size='recaudación',
            color='recaudación',
            color_continuous_scale='Reds',
            zoom=4,
            height=600,
            size_max=70
        )
        fig_mapa.update_layout(
            mapbox_style="carto-positron",
            margin={"l":0,"r":0,"t":30,"b":0}
        )

    return fig_barras, fig_linea, fig_var, fig_pie_2024, fig_pie_2025, fig_top10, fig_serie, fig_mapa

# ========== EJECUCIÓN ==========
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)

