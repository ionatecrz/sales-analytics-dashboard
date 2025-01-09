import dash
import pandas as pd
from dash import html, dcc
from dash.dependencies import Output, Input
from scripts.config import tabs_styles, tab_style, tab_selected_style
from scripts.tabs_content import tab_1_content, tab_2_content, tab_3_content, tab_4_content
from scripts.utils import load_data
import plotly.express as px

# Inicializamos la app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Sales Analytics Dashboard"

# Layout de la aplicación
app.layout = html.Div([
    html.Header(
        html.H1('Sales Analytics Dashboard', style={
            'textAlign': 'center',
            'color': '#ffffff',
            'padding': '5px 0',
            'font-family': 'Georgia, serif',
            'font-weight': 'bold',
            'fontSize': '42px',
            'textShadow': '3px 3px 7px rgba(0, 0, 0, 0.4)',
        }),
        style={
            'backgroundColor': '#006d5b',
            'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.4)',
            'borderRadius': '15px',
            'margin': '20px',
            'overflow': 'hidden'
        }
    ),

    dcc.Tabs(id="tabs-example-graph", value='tab_1', children=[
        dcc.Tab(label='Resumen de Métricas', value='tab_1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Análisis por Tienda', value='tab_2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Análisis Avanzado', value='tab_3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Pestaña Explicativa', value='tab_4', style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles),

    html.Div(id='tabs-content-example-graph')
])

# Callback para renderizar el contenido de las pestañas
@app.callback(
    Output('tabs-content-example-graph', 'children'),
    Input('tabs-example-graph', 'value')
)
def render_content(tab):
    """
    Callback para renderizar el contenido de las pestañas basado en la pestaña seleccionada.
    """
    if tab == 'tab_1':
        return tab_1_content
    elif tab == 'tab_2':
        return tab_2_content
    elif tab == 'tab_3':
        return tab_3_content
    elif tab == 'tab_4':
        return tab_4_content
    return html.Div("Seleccione una pestaña válida.")

# Callback para Pestaña 2
@app.callback(
    [Output('ventas-anuales', 'figure'),
     Output('ventas-productos', 'figure'),
     Output('productos-promocion', 'figure'),
     Output('tabla-productos-promocion', 'data')],
    Input('dropdown-tienda', 'value')
)
def update_visualizations(tienda):
    df = load_data()
    # Filtramos los datos para la tienda seleccionada
    df_filtrado = df[df['store_nbr'] == tienda]

    # Usaremos una paleta de colores personalizada que van a juego con los colores de la presentación
    green_palette = [
        '#004d40', '#006d5b', '#00897b', '#26a69a', '#4caf50',
        '#66bb6a', '#81c784', '#a5d6a7', '#1b5e20', '#2e7d32', 
        '#388e3c', '#43a047', '#4caf50', '#66bb6a', '#76c68f', 
        '#98e097', '#baf2c1', '#dcffe8'
    ]

    # Ventas Anuales

    # Agrupamos las ventas por año y las convertimos a millones para simplificar la visualización
    ventas_year = df_filtrado.groupby("year")["sales"].sum().reset_index()
    ventas_year["sales"] = ventas_year["sales"] / 1e6

    #  Creamos el gráfico de barras de ventas anuales, usando la paleta de colores previamente declarada
    fig_ventas_anuales = px.bar(
        ventas_year,
        x="year",
        y="sales",
        labels={'year': 'Año', 'sales': 'Ventas (Millones)'},
        title=f'Ventas Anuales de la Tienda {tienda}', # Título dinámico basado en la tienda seleccionada
        color_discrete_sequence=green_palette
    )

    # Fondo transparente y color del texto
    fig_ventas_anuales.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#4b565e'
    )

    # Ventas por Producto

    # Agrupamos las ventas por familia de productos
    ventas_productos = df_filtrado.groupby("family")["sales"].sum().reset_index()
    ventas_productos["sales"] = ventas_productos["sales"] / 1e6  # Convertimos a millones

    # Gráfico de barras de ventas por familia de productos
    fig_ventas_productos = px.bar(
        ventas_productos,
        x="sales",
        y="family",
        orientation='h',
        color="family", # Usamos el color para distinguir las diferentes familias 
        labels={'sales': 'Ventas (Millones)', 'family': 'Familia de Productos'},
        title=f'Ventas por Producto en la Tienda {tienda}', # Título dinámico
        color_discrete_sequence=green_palette
    )

    # Igual que antes, definimos fondo transparente y color del texto
    fig_ventas_productos.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#4b565e'
    )

    # Productos en Promoción

    # Filtramos las ventas que tienen productos en promoción y agrupamos por familia
    productos_promocion = df_filtrado[df_filtrado["onpromotion"] != 0].groupby("family")["sales"].sum().reset_index()
    productos_promocion["sales"] = productos_promocion["sales"] / 1e6

    # Gráfico de barras de ventas de productos en promoción
    fig_productos_promocion = px.bar(
        productos_promocion,
        x="sales",
        y="family",
        orientation='h',
        color="family",
        labels={'sales': 'Ventas (Millones)', 'family': 'Familia de Productos'},
        title=f'Productos en Promoción en la Tienda {tienda}', # Título dinámico
        color_discrete_sequence=green_palette
    )

    # Configuramos el fondo del gráfico como transparente y ajustamos el color del texto
    fig_productos_promocion.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#4b565e'
    )

    # Tabla de Productos en Promoción

    # Creamos un resumen de productos en promoción con ventas totales y la cantidad de productos promocionados por familia
    resumen_promocion = df_filtrado[df_filtrado["onpromotion"] != 0].groupby("family").agg(
        sales=('sales', 'sum'),
        onpromotion=('onpromotion', 'sum') # Sumamos el número de promociones para cada familia
    ).reset_index()

    # Calculamos el porcentaje de ventas por cada familia respecto al total de ventas en promoción
    total_sales = resumen_promocion["sales"].sum()
    if total_sales > 0: # Evitamos divisiones por cero.
        resumen_promocion["sales"] = (resumen_promocion["sales"] / total_sales) * 100

    # Redondeamos las ventas al 2do decimal
    resumen_promocion["sales"] = resumen_promocion["sales"].round(2)

    # Convertimos la tabla a formato dict para el dataTable
    tabla_data = resumen_promocion.to_dict('records')

    return (
        fig_ventas_anuales,
        fig_ventas_productos,
        fig_productos_promocion,
        tabla_data
    )

# Callback para Pestaña 3
@app.callback(
    Output('grafico-estacionalidad', 'figure'),
    [Input('dropdown', 'value'),
     Input('estacionalidad-variables', 'value'),
     Input('range-slider-estacionalidad', 'value')]
)
def update_estacionalidad(estado, variables, slider_range):
    df = load_data()
    # Convertimos el rango del slider en fechas específicas
    fecha_inicio = pd.to_datetime(slider_range[0], unit='s')
    fecha_fin = pd.to_datetime(slider_range[1], unit='s')

    # Filtramos los datos para el estado seleccionado dentro del rango de fechas
    df_filtrado = df.query("state == @estado and @fecha_inicio <= date <= @fecha_fin")

    # Extraemos las columnas numéricas válidas seleccionadas para el análisis
    columnas_validas = [col for col in variables if col in df_filtrado.select_dtypes(include=['number']).columns]
    df_resumen = df_filtrado.groupby('date', as_index=False)[columnas_validas].sum()

    # Creamos el gráfico de líneas para mostrar la estacionalidad
    fig = px.line(
        df_resumen, 
        x='date', 
        y=columnas_validas,
        labels={'value': 'Valor', 'date': 'Fecha'},
        title=f'Estacionalidad en el Estado de {estado}'
    )

    # Incorporamos días festivos como puntos adicionales si se seleccionan
    if 'holidays' in variables:
        festivos = (
            df_filtrado.query("holiday_type == 'Holiday'")
            .groupby('date', as_index=False)['sales']
            .sum()
        )

        # Añadimos marcadores para los festivos si existen datos
        if not festivos.empty:
            fig.add_scatter(
                x=festivos['date'],
                y=festivos['sales'],
                mode='markers',
                marker=dict(size=8, color='red', symbol='circle'),
                name='Festivos'
            )

    # Configuramos el diseño del gráfico para mantener coherencia visual
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#4b565e'
    )

    return fig

@app.callback(
    Output('grafico-comparativo', 'figure'),
    [Input('dropdown', 'value'),
     Input('range-slider-comp', 'value'),
     Input('agrupacion-selector', 'value')]  # Selector para la agrupación
)
def update_comparativo(estado, slider_range, agrupacion):
    df = load_data()
    # Convertimos el rango del slider a fechas específicas
    fecha_inicio = pd.to_datetime(slider_range[0], unit='s')
    fecha_fin = pd.to_datetime(slider_range[1], unit='s')
    
    # Filtramos los datos por estado y rango de fechas
    df_filtrado = df.query("state == @estado and @fecha_inicio <= date <= @fecha_fin").copy()
    
    # Aseguramos que las columnas numéricas no contengan NaN y convertimos valores no válidos
    df_filtrado['transactions'] = pd.to_numeric(df_filtrado['transactions'], errors='coerce').fillna(0)
    df_filtrado['sales'] = pd.to_numeric(df_filtrado['sales'], errors='coerce').fillna(0)
    df_filtrado['onpromotion'] = pd.to_numeric(df_filtrado['onpromotion'], errors='coerce').fillna(0)
    
    # Verificamos si los datos filtrados están vacíos
    if df_filtrado.empty:
        return px.scatter().update_layout(
            title="No hay datos disponibles",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
    
    # Lógica para gráficos sin agrupación
    if agrupacion == 'none':
        # Agrupamos los datos a nivel de tienda
        df_agrupado = df_filtrado.groupby('store_nbr').agg(
            sales_avg=('sales', 'mean'),
            onpromotion_avg=('onpromotion', 'mean'),
            transactions_sum=('transactions', 'sum'),
            store_type=('store_type', 'first')  # Tipo de tienda asociado
        ).reset_index()
        
        # Creamos un gráfico de dispersión comparativo para las tiendas
        fig = px.scatter(
            df_agrupado,
            x='sales_avg',
            y='onpromotion_avg',
            size='transactions_sum',
            color='store_type',
            labels={
                'sales_avg': 'Ventas Promedio por Tienda',
                'onpromotion_avg': '% Promoción Promedio',
                'transactions_sum': 'Total de Transacciones',
                'store_type': 'Tipo de Tienda'
            },
            title=f'Comparación Multidimensional en el Estado de {estado}',
            hover_data=['store_nbr']
        )
    else:
        # Agrupamos los datos por clúster o tipo de tienda
        agrupacion_columna = 'store_type' if agrupacion == 'store_type' else 'cluster'
        
        # Verificamos que la columna de agrupación exista
        if agrupacion_columna not in df_filtrado.columns:
            return px.scatter().update_layout(
                title="No hay datos disponibles para la agrupación seleccionada",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
        
        # Calculamos las métricas agregadas según la agrupación
        df_agrupado = df_filtrado.groupby(agrupacion_columna).agg(
            sales_avg=('sales', 'mean'),
            onpromotion_avg=('onpromotion', 'mean'),
            transactions_sum=('transactions', 'sum')
        ).reset_index()
        
        # Verificamos si los datos agrupados están vacíos
        if df_agrupado.empty:
            return px.scatter().update_layout(
                title="No hay datos disponibles",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
        
        # Creamos un gráfico comparativo para la agrupación seleccionada
        fig = px.scatter(
            df_agrupado,
            x='sales_avg',
            y='onpromotion_avg',
            size='transactions_sum',
            color=agrupacion_columna,
            labels={
                'sales_avg': 'Ventas Promedio',
                'onpromotion_avg': '% Promoción Promedio',
                'transactions_sum': 'Total de Transacciones',
                agrupacion_columna: 'Agrupación'
            },
            title=f'Comparación Multidimensional en el Estado de {estado}',
            hover_data=['transactions_sum']
        )
    
    # Ajustamos la opacidad y configuramos el diseño visual del gráfico
    fig.update_traces(marker=dict(opacity=0.7))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#4b565e'
    )
    
    return fig

@app.callback(
    Output('heatmap-patrones', 'figure'),
    [Input('familia-selector', 'value'),  # Filtro por familia de producto
     Input('normalizacion-selector', 'value'),  # Selector de normalización
     Input('comparacion-selector', 'value'),  # Comparación entre períodos
     Input('año-1-selector', 'value'),  # Primer año para comparación
     Input('año-2-selector', 'value')]  # Segundo año para comparación
)
def update_heatmap(familia, normalizacion, comparacion, año_1, año_2):
    df = load_data()
    # Filtramos los datos según la familia seleccionada
    df_filtrado = df[df['family'] == familia].copy()

    # Verificamos si el DataFrame está vacío, devolviendo un heatmap vacío si no hay datos
    if df_filtrado.empty:
        empty_data = pd.DataFrame(
            data=[[0]], index=["Sin datos"], columns=["Sin datos"]
        )
        return px.imshow(
            empty_data,
            labels={'x': '', 'y': '', 'color': 'Sin datos'},
            title="No hay datos disponibles"
        ).update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#4b565e'
        )

    # Agregamos columnas auxiliares para identificar día de la semana, semana y año
    df_filtrado['day_of_week'] = df_filtrado['date'].dt.day_name()
    df_filtrado['week'] = df_filtrado['date'].dt.isocalendar().week
    df_filtrado['year'] = df_filtrado['date'].dt.year

    # Implementamos lógica de comparación si la opción está habilitada y se especificaron años
    if 'comparar' in comparacion and año_1 and año_2:
        if año_1 == año_2:
            # Si los años son iguales, simplemente mostramos un heatmap para ese año
            df_año_1 = df_filtrado[df_filtrado['year'] == año_1]
            heatmap_data = df_año_1.groupby(['day_of_week', 'week'])['sales'].sum().reset_index()
            heatmap_data = heatmap_data.pivot(index='day_of_week', columns='week', values='sales').fillna(0)
            color_label = 'Ventas (%)' if normalizacion == 'relativo' else 'Ventas'
        else:
            # Filtramos los datos por los años seleccionados
            df_año_1 = df_filtrado[df_filtrado['year'] == año_1]
            df_año_2 = df_filtrado[df_filtrado['year'] == año_2]

            # Agrupamos las ventas por día y semana para ambos años
            heatmap_año_1 = df_año_1.groupby(['day_of_week', 'week'])['sales'].sum().reset_index()
            heatmap_año_2 = df_año_2.groupby(['day_of_week', 'week'])['sales'].sum().reset_index()

            # Normalizamos los datos si se seleccionó la opción de relativo
            if normalizacion == 'relativo':
                total_año_1 = heatmap_año_1['sales'].sum()
                total_año_2 = heatmap_año_2['sales'].sum()

                if total_año_1 > 0:
                    heatmap_año_1['sales'] = (heatmap_año_1['sales'] / total_año_1) * 100
                if total_año_2 > 0:
                    heatmap_año_2['sales'] = (heatmap_año_2['sales'] / total_año_2) * 100

            # Combinamos los datos de ambos años para generar la comparación
            heatmap_comparacion = pd.merge(
                heatmap_año_1, heatmap_año_2,
                on=['day_of_week', 'week'],
                how='outer',
                suffixes=(f'_{año_1}', f'_{año_2}')
            ).fillna(0)

            # Calculamos las diferencias entre ambos años (absolutas o porcentuales)
            heatmap_comparacion['diferencia'] = heatmap_comparacion[f'sales_{año_1}'] - heatmap_comparacion[f'sales_{año_2}']

            # Creamos la matriz para el heatmap basada en las diferencias calculadas
            heatmap_data = heatmap_comparacion.pivot(index='day_of_week', columns='week', values='diferencia').fillna(0)
            color_label = f'Diferencia de Ventas (%) ({año_1} vs {año_2})' if normalizacion == 'relativo' else f'Diferencia de Ventas ({año_1} vs {año_2})'
    else:
        # Normalizamos las ventas si se seleccionó la opción de relativo (sin comparación)
        if normalizacion == 'relativo':
            total_sales = df_filtrado['sales'].sum()
            if total_sales > 0:
                df_filtrado['sales'] = (df_filtrado['sales'] / total_sales) * 100

        # Creamos la matriz para el heatmap basada en datos normales o normalizados
        heatmap_data = df_filtrado.groupby(['day_of_week', 'week'])['sales'].sum().reset_index()
        heatmap_data = heatmap_data.pivot(index='day_of_week', columns='week', values='sales').fillna(0)
        color_label = 'Ventas (%)' if normalizacion == 'relativo' else 'Ventas'

    # Creamos el gráfico de heatmap con los datos procesados
    fig = px.imshow(
        heatmap_data,
        labels={'x': 'Semana del Año', 'y': 'Día de la Semana', 'color': color_label},
        title=f'Patrones de Venta ({familia})'
    )

    # Configuramos la estética del gráfico para alinearlo con el diseño general
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#4b565e'
    )

    return fig

@app.callback(
    Output('años-comparacion', 'style'),  # Modificamos el estilo del contenedor de selección de años
    Input('comparacion-selector', 'value')  # Detectamos el valor seleccionado en el comparador
)
def toggle_año_dropdowns(comparacion_value):
    # Verificamos si la opción de comparación está activa
    if 'comparar' in comparacion_value:
        # Mostramos el selector de años con un diseño flexible y espacio entre elementos
        return {'display': 'flex', 'gap': '10px'}
    # Ocultamos el selector de años si no se selecciona la comparación
    return {'display': 'none'}

@app.callback(
    Output('grafico-radar-estados', 'figure'),  # Salida: figura del gráfico radar
    Input('radar-estados-selector', 'value')  # Entrada: lista de estados seleccionados
)
def update_radar_estados(estados):
    df = load_data()
    # Verificamos si hay estados seleccionados
    if not estados or len(estados) == 0:
        # Devolvemos un gráfico vacío con un mensaje si no se seleccionan estados
        return px.scatter().update_layout(
            title="No hay estados seleccionados",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#4b565e'
        )

    # Filtramos los datos para incluir únicamente los estados seleccionados
    df_filtrado = df[df['state'].isin(estados)].copy()

    # Verificamos si los datos filtrados están vacíos
    if df_filtrado.empty:
        # Devolvemos un gráfico vacío con un mensaje si no hay datos disponibles
        return px.scatter().update_layout(
            title="No hay datos disponibles para los estados seleccionados",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#4b565e'
        )

    # Calculamos métricas agregadas por estado
    resumen_estados = df_filtrado.groupby('state').agg(
        Ventas=('sales', 'sum'),  # Total de ventas por estado
        Promociones_Activas=('onpromotion', 'sum'),  # Total de promociones activas
        Transacciones=('transactions', 'sum')  # Total de transacciones
    ).reset_index()

    # Calculamos métricas adicionales para el análisis
    resumen_estados['Ventas_Promedio_Transaccion'] = (
        resumen_estados['Ventas'] / resumen_estados['Transacciones']
    ).fillna(0)  # Calculamos el promedio de ventas por transacción y manejamos valores nulos

    resumen_estados['Promociones_Por_Transaccion'] = (
        resumen_estados['Promociones_Activas'] / resumen_estados['Transacciones']
    ).fillna(0)  # Calculamos el promedio de promociones por transacción y manejamos valores nulos

    # Normalizamos las métricas en una escala de 0 a 100
    for col in ['Ventas', 'Promociones_Activas', 'Transacciones', 'Ventas_Promedio_Transaccion', 'Promociones_Por_Transaccion']:
        max_val = resumen_estados[col].max()  # Encontramos el valor máximo en la métrica
        if max_val > 0:
            resumen_estados[col] = (resumen_estados[col] / max_val) * 100  # Normalizamos el valor

    # Reestructuramos los datos para que se adapten al formato del gráfico radar
    radar_data = resumen_estados.melt(
        id_vars='state',  # La variable de identificación es el estado
        var_name='Métrica',  # Nombramos la columna de métricas
        value_name='Valor'  # Nombramos la columna de valores
    )

    # Creamos el gráfico de radar para comparar el rendimiento por estado
    fig = px.line_polar(
        radar_data,
        r='Valor',  # Valor radial (métrica normalizada)
        theta='Métrica',  # Las métricas en el eje angular
        color='state',  # Coloreamos por estado
        line_close=True,  # Cerramos las líneas del radar
        title="Comparación de rendimiento por estado"  # Título del gráfico
    )

    # Configuramos el diseño del gráfico para mantener coherencia estética
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])  # Definimos la escala del eje radial
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo transparente del gráfico
        font_color='#4b565e'  # Color del texto
    )

    # Devolvemos el gráfico generado
    return fig


# Run server
if __name__ == '__main__':
    app.run_server(debug=True, jupyter_mode='external', port=5001)