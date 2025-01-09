# Importamos dash
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash import jupyter_dash
from dash import dash_table

# Importamos plotly
import plotly.express as px
import plotly.graph_objects as go

# Importamos librerias para la manipulación de datos
import pandas as pd
import numpy as np

# Configuración warnings
import warnings
warnings.filterwarnings('ignore')

# Carga de datos

def load_data():
    # Cargamos ambos datases
    df_11= pd.read_csv('./data/sales_1_part1.csv',sep=",")
    df_12= pd.read_csv('./data/sales_1_part2.csv',sep=",")
    df_21= pd.read_csv('./data/sales_2_part1.csv',sep=",")
    df_22= pd.read_csv('./data/sales_2_part2.csv',sep=",")
    # Fusionamos los datasets en uno único
    df= pd.concat([df_11,df_12,df_21,df_22])
    # Establecemos la columna de date a datetime ya que será más cómodo de trabajar con fechas
    df['date'] = pd.to_datetime(df['date'])
    return df

# Funciones genéricas

def firma_pag():
    """
    Firma a pie de página con separador horizontal, nombre y año.
    """
    return html.Div([
        html.Hr(style={'borderTop': '1px solid #006d5b', 'marginTop': '30px', 'marginBottom': '10px'}),
        html.Div([
            html.Span('Íñigo de Oñate', style={'color': '#4b565e', 'fontSize': '16px'}),
            html.Span('2024', style={'color': '#4b565e', 'fontSize': '16px', 'float': 'right'})
        ], style={'display': 'flex', 'justify-content': 'space-between', 'alignItems': 'center'})
    ])

def title(tab_name):
    """
    Creación del título principal de las pestañas
    """
    return html.Div([
        html.H1(tab_name, 
            style={
                'text-align': 'center', 
                'color': '#4b565e', 
                'fontSize': '42px',
                'marginBottom': '20px'
            }
        ),
        html.Hr(style={'borderTop': '4px solid #006d5b', 'marginTop': '30px', 'marginBottom': '30px'})
    ])

def create_dropdown_with_label(label_text,label_size, dropdown_id, options, default_value, container_style=None, dropdown_style=None):
    """
    Creación de texto y dropdown.
    
    :param label_text: Texto del encabezado.
    :param label_size: Tamaño del texto.
    :param dropdown_id: ID único para el dropdown.
    :param options: Lista de opciones para el dropdown (formato [{'label': 'Texto', 'value': 'valor'}]).
    :param default_value: Valor seleccionado por defecto en el dropdown.
    :param container_style: Estilo adicional para el contenedor principal.
    :param dropdown_style: Estilo adicional para el dropdown.
    :return: Componente Dash.
    """
    return html.Div([
        html.Div([
            html.H3(label_text, style={'color': '#006d5b', 'fontSize': label_size, 'marginRight': '20px'}),
            dcc.Dropdown(
                id=dropdown_id, # Identificador único 
                options=options,
                value=default_value,
                style=dropdown_style or {'width': '300px'} 
            )
        ], style=container_style or {'display': 'flex', 'alignItems': 'center', 'justifyContent': 'flex-start', 'marginBottom': '20px'})
    ])

def create_section(title, paragraphs):
    """
    Creación de bloques de texto explicativo
    """
    return html.Div([
        html.H3(title, style={'color': '#006d5b'}),
        *[html.P(paragraph) for paragraph in paragraphs]
    ], style={'marginBottom': '20px'}) 

# Funciones Primera Pestaña

# Contador de métricas básicas
def contador(df):
    # Calculamos el número total de tiendas, productos y estados
    num_tiendas = df["store_nbr"].nunique()
    num_productos = df["family"].nunique()
    num_estados = df["state"].nunique()

    return num_tiendas,num_productos,num_estados

# Gráfico de los 10 productos más vendidos
def ranking_productos(df,layout):
    # Calculamos el promedio de ventas por producto y seleccionamos los 10 más vendidos
    ranking_ventas = df.groupby("family")["sales"].mean().sort_values(ascending=False).reset_index().head(10)
    
    # Creamos un gráfico de barras para mostrar el ranking
    barChart = dcc.Graph(
        figure=go.Figure(layout=layout).add_trace(
            go.Bar(
                x=ranking_ventas["family"],  # Productos
                y=ranking_ventas["sales"],  # Ventas promedio
                marker=dict(color='#006d5b')  
            )
        ).update_layout(
            xaxis_title="Productos",  # Etiqueta del eje X
            yaxis_title="Ventas Medias",  # Etiqueta del eje Y
            xaxis=dict(showgrid=False),  # Eliminamos cuadrículas
            yaxis=dict(showgrid=False),  
        ),
        style={'width': '48%', 'height': '40vh', 'display': 'inline-block'}  # Estilo del gráfico
    )
    return barChart

# Gráfico de líneas de ventas mensuales
def ventas_mensuales(df,layout):
    # Agrupamos las ventas totales por mes
    ventas_mes = df.groupby("month")["sales"].sum().reset_index()
    
    # Convertimos las ventas a millones (mejor visualización)
    ventas_mes["sales"] = ventas_mes["sales"] / 1e6

    # Gráfico de líneas con marcadores para representar las ventas por mes
    lineChart = dcc.Graph(
        figure=go.Figure(layout=layout).add_trace(
            go.Scatter(
                x=ventas_mes["month"],  # Meses
                y=ventas_mes["sales"],  # Ventas totales
                mode="lines+markers",  
                marker=dict(color='#006d5b', size=8), 
                line=dict(width=2) 
            )
        ).update_layout(
            title="Ventas Totales por Mes",  
            xaxis_title="Mes", 
            yaxis_title="Ventas Totales (Millones)", 
            xaxis=dict(
                tickmode="array",  # Visualización de ticks
                tickvals=list(range(1, 13)),  
                ticktext=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],  # Etiquetas de los meses
                showgrid=False  
            ),
            yaxis=dict(
                showgrid=False, 
                ticksuffix="M"  # Sufijo "M" de millones
            )
        ),
        style={'width': '48%', 'height': '40vh', 'display': 'inline-block'}  
    )
    return lineChart

# Gráfico de ventas por día de la semana
def ventas_por_dia_semana(df,layout):
    # Calculamos las ventas totales por día de la semana
    ventas_dia_semana = df.groupby("day_of_week")["sales"].sum().reset_index()
    
    # Creamos un gráfico de líneas para representar las ventas por día
    lineChart = dcc.Graph(
        figure=go.Figure(layout=layout).add_trace(
            go.Scatter(
                x=ventas_dia_semana["day_of_week"],  # Días de la semana en el eje X
                y=ventas_dia_semana["sales"],  # Ventas totales en el eje Y
                mode="lines+markers",  
                marker=dict(color='#006d5b')  
            )
        ).update_layout(
            xaxis_title="Día de la Semana",  
            yaxis_title="Ventas Totales", 
            xaxis=dict(showgrid=False), 
            yaxis=dict(showgrid=False), 
        ),
        style={'width': '48%', 'height': '40vh', 'display': 'inline-block'}  
    )
    return lineChart

# Gráfico de ventas por estado
def ventas_por_estado(df,layout):
    # Calculamos las ventas totales por estado y las ordenamos en orden descendente
    ventas_estado = df.groupby("state")["sales"].sum().sort_values(ascending=False).reset_index()
    
    # Creamos un gráfico de barras para representar las ventas por estado
    barChart = dcc.Graph(
        figure=go.Figure(layout=layout).add_trace(
            go.Bar(
                x=ventas_estado["state"],  # Estados en el eje X
                y=ventas_estado["sales"],  # Ventas totales en el eje Y
                marker=dict(color='#006d5b')  
            )
        ).update_layout(
            xaxis_title="Estado", 
            yaxis_title="Ventas Totales", 
            xaxis=dict(showgrid=False), 
            yaxis=dict(showgrid=False), 
        ),
        style={'width': '48%', 'height': '40vh', 'display': 'inline-block'}  
    )
    return barChart

# Gráfico de ventas durante días laborales vs festivos
def ventas_dias_festivos(df,layout):
    # Agrupamos las ventas totales por tipo de día (laboral o festivo)
    df_festivos = df.groupby("holiday_type")["sales"].sum().reset_index()
    
    # Creamos un gráfico de barras para comparar ventas entre tipos de día
    barChart = dcc.Graph(
        figure=go.Figure(layout=layout).add_trace(
            go.Bar(
                x=df_festivos["holiday_type"],  # Tipos de día en el eje X
                y=df_festivos["sales"],  # Ventas totales en el eje Y
                marker=dict(color='#006d5b') 
            )
        ).update_layout(
            xaxis_title="Tipo de Día",  
            yaxis_title="Ventas Totales",
            xaxis=dict(showgrid=False),  
            yaxis=dict(showgrid=False),  
        ),
        style={'width': '48%', 'height': '40vh', 'display': 'inline-block'}  
    )
    return barChart

# Funciones Segunda Pestaña


