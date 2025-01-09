from dash import html
from dash import dcc
from scripts.utils import *
from scripts.config import layout

# Cargamos los datos
df = load_data()

def title(text):
    return html.H1(text, style={'text-align': 'center', 'color': '#006d5b', 'fontSize': '36px'})

tab_1_content = html.Div([

    # Título principal de la pestaña
    title("Resumen de Métricas"),
    
    # Métricas clave: número de tiendas, productos y estados
    html.Div([
        html.Div([
            html.H3(
                ["Nº de tiendas", "Nº total de productos", "Total de Estados"][i], 
                style={'text-align': 'center', 'color': '#006d5b', 'fontSize': '28px'}
            ),
            html.H2(
                contador(df)[i], 
                style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '52px'}
            )
        ], style={'width': '30%', 'text-align': 'center'}) for i in range(3)
    ], style={'display': 'flex', 'justify-content': 'space-around', 'marginTop': '20px', 'marginBottom': '20px'}),
    
    # Línea horizontal decorativa
    html.Hr(style={'borderTop': '3px solid #006d5b', 'marginTop': '30px', 'marginBottom': '30px'}),
    
    # Gráficos organizados en filas
    html.Div([
        # Primera fila
        html.Div([
            html.Div([
                html.H3('10 Productos más vendidos', style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
                dcc.Graph(
                    id='top_10_productos',
                    figure=ranking_productos(df,layout).figure,
                    style={'width': '100%', 'height': '300px'}
                )
            ], style={'border': '1px solid #006d5b', 'padding': '10px', 'borderRadius': '10px', 
                      'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'width': '45%', 'marginBottom': '20px'}),
            
            html.Div([
                html.H3('Ventas mensuales', style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
                dcc.Graph(
                    id='ventas_mensuales',
                    figure=ventas_mensuales(df,layout).figure,
                    style={'width': '100%', 'height': '300px'}
                )
            ], style={'border': '1px solid #006d5b', 'padding': '10px', 'borderRadius': '10px', 
                      'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'width': '45%', 'marginBottom': '20px'})
        ], style={'display': 'flex', 'justify-content': 'space-around'}),
        
        # Segunda fila
        html.Div([
            html.Div([
                html.H3('Ventas por día de la semana', style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
                dcc.Graph(
                    id='ventas_por_dia_semana',
                    figure=ventas_por_dia_semana(df,layout).figure,
                    style={'width': '100%', 'height': '300px'}
                )
            ], style={'border': '1px solid #006d5b', 'padding': '10px', 'borderRadius': '10px', 
                      'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'width': '45%', 'marginBottom': '20px'}),
            
            html.Div([
                html.H3('Ventas por estado', style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
                dcc.Graph(
                    id='ventas_por_estado',
                    figure=ventas_por_estado(df,layout).figure,
                    style={'width': '100%', 'height': '300px'}
                )
            ], style={'border': '1px solid #006d5b', 'padding': '10px', 'borderRadius': '10px', 
                      'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'width': '45%', 'marginBottom': '20px'})
        ], style={'display': 'flex', 'justify-content': 'space-around'}),
        
        # Tercera fila
        html.Div([
            html.Div([
                html.H3('Ventas en días laborales y festivos', style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
                dcc.Graph(
                    id='ventas_dias_festivos',
                    figure=ventas_dias_festivos(df,layout).figure,
                    style={'width': '100%', 'height': '300px'}
                )
            ], style={'border': '1px solid #006d5b', 'padding': '10px', 'borderRadius': '10px', 
                      'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'width': '95%', 'marginBottom': '20px'})
        ], style={'display': 'flex', 'justify-content': 'space-around'}),
    ]),
    
    # Firma a pie de página
    firma_pag(),
    
], style={'background-color': '#eaf4eb', 'padding': '20px', 'border-radius': '20px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'margin-top': '10px'})

tab_2_content = html.Div([

    # Título de la pestaña
    title("Análisis por Tienda"),

    # Dropdown para seleccionar una tienda específica
    create_dropdown_with_label(label_text="Seleccione una tienda para ver el análisis",label_size="30px",dropdown_id="dropdown-tienda",options=[{'label': i, 'value': i} for i in sorted(df['store_nbr'].unique())],default_value=1,container_style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'flex-start', 'padding': '10px 20px', 'marginBottom': '30px'}, dropdown_style={'width': '50%'}),
            
    # Gráfico de Ventas Anuales por Tienda
    html.Div([
        html.H3('Ventas anuales por tienda', style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
        dcc.Graph(
            id='ventas-anuales',
            style={'width': '100%', 'height': '450px'}
        )
    ], style={'border': '1px solid #006d5b', 'padding': '20px', 'borderRadius': '10px', 
              'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'width': '95%', 'margin': 'auto', 'marginBottom': '20px'}),

    # Gráfico de Ventas por Producto
    html.Div([
        html.H3('Ventas por producto', style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
        dcc.Graph(
            id='ventas-productos',
            style={'width': '100%', 'height': '450px'}
        )
    ], style={'border': '1px solid #006d5b', 'padding': '20px', 'borderRadius': '10px', 
              'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'width': '95%', 'margin': 'auto', 'marginBottom': '20px'}),

    # Gráfico de Productos en Promoción
    html.Div([
        html.H3('Productos en promoción', style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
        dcc.Graph(
            id='productos-promocion',
            style={'width': '100%', 'height': '450px'}
        )
    ], style={'border': '1px solid #006d5b', 'padding': '20px', 'borderRadius': '10px', 
              'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'width': '95%', 'margin': 'auto', 'marginBottom': '20px'}),

    # Tabla resumen de productos en promoción
    html.Div([
        html.H3('Resumen de productos en promoción', style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
        dash_table.DataTable(
            id='tabla-productos-promocion',
            columns=[
                {'name': 'Familia', 'id': 'family'}, # Categoría del producto
                {'name': 'Ventas (% Promoción)', 'id': 'sales'}, # Porcentaje de ventas en promoción
                {'name': 'Nº Promociones', 'id': 'onpromotion'} # Número total de promociones
            ],
            style_cell={'textAlign': 'center', 'padding': '10px', 'minWidth': '90px', 'width': '90px', 'maxWidth': '100px'},
            style_table={'overflowX': 'auto', 'width': '100%'}, # Habilitamos el scroll horizontal
            style_header={'backgroundColor': '#006d5b', 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': '#f5f5f5'},
            page_size=10 # Nº filas visibles por página
        )
    ], style={'border': '1px solid #006d5b', 'padding': '20px', 'borderRadius': '10px',
            'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'width': '95%', 'margin': 'auto', 'marginBottom': '20px'}),

    # Firma a pie de página
    firma_pag(),
    
], style={'background-color': '#eaf4eb', 'padding': '20px','border-radius': '20px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)','margin-top': '10px'})

tab_3_content = html.Div([
    # Título principal de la pestaña
    title("Visualización por Estados"),

    # Dropdown para filtrar datos por estado
    create_dropdown_with_label(label_text="Seleccione un estado",label_size="30px",dropdown_id="dropdown",
                               options=[{'label': i, 'value': i} for i in sorted(df['state'].unique())],
                               default_value="Pichincha"),

    # Gráfico: Análisis de estacionalidad
    html.Div([
        html.H3("Análisis de estacionalidad", style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),

        # Checklist para elegir las variables a dibujar
        dcc.Checklist(
            id='estacionalidad-variables',
            options=[
                {'label': 'Ventas diarias', 'value': 'sales'},
                {'label': 'Productos en promoción', 'value': 'onpromotion'},
                {'label': 'Días festivos', 'value': 'holidays'}
            ],
            value=['sales'],  # Por defecto, mostramos las ventas diarias
            inline=True,  
            style={
                'text-align': 'center', 
                'marginBottom': '20px'
            },
            inputStyle={
                'marginRight': '10px',  # Espacio entre el cuadro de selección y la etiqueta
            },
            labelStyle={
                'display': 'inline-block', # Permitimos espaciado personalizado
                'marginRight': '15px',     # Espacio entre opciones
                'padding': '5px 10px',     # Espaciado interno para estilo del fondo
                'borderRadius': '5px',     # Bordes redondeados
                'cursor': 'pointer'        # Cambiar cursor al pasar sobre la opción
            },
            persistence=True,  # Mantenemos la selección en caso de recarga
            persistence_type='session'  # Persistencia por sesión
        ),

        # Actualiza los datos según los filtros
        dcc.Graph(
            id='grafico-estacionalidad',
            style={'width': '100%', 'height': '450px'}
        ),

        # Slider para seleccionar rango de fechas
        html.Div(
            dcc.RangeSlider(
                id='range-slider-estacionalidad',
                min=df['date'].min().timestamp(),
                max=df['date'].max().timestamp(),
                value=[df['date'].min().timestamp(), df['date'].max().timestamp()],
                marks={ # Intervalos de 6 meses para mayor claridad
                    int(date.timestamp()): date.strftime('%b-%Y')  # Formato abreviado del mes y año
                    for date in pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='6M')
                },
                step=None,  
                tooltip={"always_visible": True}  # Tooltip siempre visible para mostrar el rango seleccionado
            ),
            style={'marginTop': '20px', 'marginBottom': '20px'}  
        )
    ], style={'border': '1px solid #006d5b', 'padding': '20px', 'borderRadius': '10px', 
            'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'width': '95%', 'margin': 'auto', 'marginBottom': '20px'}),

    # Gráfico: Análisis comparativo multidimensional
    html.Div([
        html.H3("Análisis comparativo multidimensional", style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
        create_dropdown_with_label(
            label_text="Agrupar por:",
            label_size="20px",
            dropdown_id="agrupacion-selector",
            options=[
                {'label': 'No agrupar', 'value': 'none'},  # Opción inicial (sin agrupar)
                {'label': 'Clúster', 'value': 'cluster'},
                {'label': 'Tipo de Tienda', 'value': 'store_type'}
            ],
            default_value='none',  # Por defecto
            container_style={'justifyContent': 'center'},
            dropdown_style={'width': '250px'}
        ),
        # Actualiza los datos según los filtros
        dcc.Graph(
            id='grafico-comparativo',
            style={'width': '100%', 'height': '450px'}
        ),
        # Slider para ajustar el rango temporal del análisis (misma lógica que antes)
        html.Div(
            dcc.RangeSlider(
                id='range-slider-comp',
                min=df['date'].min().timestamp(),
                max=df['date'].max().timestamp(),
                value=[df['date'].min().timestamp(), df['date'].max().timestamp()],
                marks={
                    int(date.timestamp()): date.strftime('%b %Y')  # Formato abreviado de mes y año
                    for date in pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='6M')
                },
                step=None,  
                tooltip={"always_visible": True}  
            ),
            style={'marginTop': '20px', 'marginBottom': '20px'}  # Espaciado
        )
    ], style={'border': '1px solid #006d5b', 'padding': '20px', 'borderRadius': '10px', 
              'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)', 'width': '95%', 'margin': 'auto', 'marginBottom': '20px'}),

    # Gráfico: Patrones de venta
    html.Div([
        html.H3("Patrones de venta", style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
        # Primera línea: Dropdown para seleccionar familia de producto
        html.Div([
            create_dropdown_with_label(
                label_text="Seleccione una familia",
                label_size="20px",
                dropdown_id="familia-selector",
                options=[{'label': i, 'value': i} for i in sorted(df['family'].unique())], # Las opciones serán los valores únicos de familias
                default_value=sorted(df['family'].unique())[0] # Por defecto, seleccionamos la primera en el dataframe
            ),
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'marginBottom': '10px'}),
        # Segunda línea: Selector de normalización (Absoluto/Relativo)
        html.Div([
            dcc.RadioItems(
                id='normalizacion-selector',
                options=[
                    {'label': 'Absoluto', 'value': 'absoluto'},
                    {'label': 'Relativo', 'value': 'relativo'}
                ],
                value='absoluto',  # Valor predeterminado
                inline=True,
                style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'fontSize': '16px'}
            )
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        # Tercera línea: Comparación entre períodos y selección de años
        html.Div([
            # Comparación entre períodos
            html.Div([
                dcc.Checklist(
                    id='comparacion-selector',
                    options=[{'label': 'Comparar entre años', 'value': 'comparar'}],
                    value=[],
                    inline=True,
                    style={'fontSize': '16px', 'marginBottom': '10px'}
                )
            ], style={'marginRight': '20px'}),
            # Dropdowns para seleccionar los años (visibles solo si se selecciona comparar)
            html.Div([
                # Dropdown para seleccionar año 1
                create_dropdown_with_label(
                    label_text="Año 1",
                    label_size="16px",
                    dropdown_id="año-1-selector",
                    options=[{'label': str(año), 'value': año} for año in sorted(df['year'].unique())], # Presentamos como opciones los distintos años presentes en el daataset 
                    default_value=None
                ),
                # Dropdown para seleccionar año 2
                create_dropdown_with_label(
                    label_text="Año 2",
                    label_size="16px",
                    dropdown_id="año-2-selector",
                    options=[{'label': str(año), 'value': año} for año in sorted(df['year'].unique())],
                    default_value=None
                ),
            ], id='años-comparacion', style={'display': 'none', 'gap': '10px'})
        ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'marginBottom': '20px', 'gap': '20px'}),
        # Heatmap
        dcc.Graph(id='heatmap-patrones', style={'width': '100%', 'height': '450px'})
    ], style={
        'border': '1px solid #006d5b',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',
        'width': '95%',
        'margin': 'auto',
        'marginBottom': '20px'
    }),

    # Comparación de estados con Radar Chart
    html.Div([
        html.H3("Comparación de rendimiento entre estados", style={'text-align': 'center', 'color': '#4b565e', 'fontSize': '30px'}),
        html.Div([
            html.Div([
                html.H3("Seleccione los estados a comparar:", style={'color': '#006d5b', 'fontSize': '20px', 'marginRight': '20px'}),
                # Dropdown para seleccionar varios estados a la vez (multi)
                dcc.Dropdown(
                    id="radar-estados-selector",
                    options=[{'label': state, 'value': state} for state in sorted(df['state'].unique())], # Presentaremos los distintos estados del df como opciones a seleccionar
                    value=["Pichincha", "Guayas"],  # Valores predeterminados
                    multi=True,  # Permitir múltiples selecciones
                    style={'width': '300px'}
                )
            ], style={
                'display': 'flex',
                'alignItems': 'center', 
                'justifyContent': 'center', 
                'marginBottom': '20px'
            }),
        ], style={'textAlign': 'center'}),
        dcc.Graph(
            id='grafico-radar-estados',
            style={'width': '100%', 'height': '500px'}
        )
    ], style={
        'border': '1px solid #006d5b',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',
        'width': '95%',
        'margin': 'auto',
        'marginBottom': '20px'
    }),


        # Firma a pie de pagina
        firma_pag(),
        
    ], style={'background-color': '#eaf4eb', 'padding': '20px','border-radius': '20px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)','margin-top': '10px'})

tab_4_content = html.Div([
    # Título principal
    title("Documentación del Dashboard"),
    
    # Línea divisoria
    html.Br(),
    
    # Explicación de la pestaña de visualización básica
    create_section("Resumen de Métricas", [
        "Esta primera pestaña del dashboard está diseñada para proporcionar una visión general rápida y clara del rendimiento de la empresa. Se enfoca en exponer "
        "tanto métricas clave como tendencias generales, distribuidas en gráficos que cubren diferentes dimensiones del análisis. Para ello hace uso de:",
        html.Ul([
            html.Li([
                html.Span("Contador de métricas básicas: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Esta sección calcula tres datos clave: el número total de tiendas, productos y estados en los que la empresa opera. Estos valores se obtienen "
                "a partir de registros únicos en el dataset, lo que ofrece una visión global de las capacidades de la empresa. Los resultados son mostrados de forma clara y directa."
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("10 Productos más vendidos: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Un gráfico de barras que muestra los diez productos con mayor volumen de ventas. Para crearlo, se calculan las ventas promedio por familia de producto "
                "y se seleccionan las diez con mayores valores, excluyendo datos faltantes o inconsistentes. Esto asegura un análisis preciso y enfocado."
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Ventas mensuales: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Un gráfico de líneas que visualiza la evolución de las ventas mes a mes. Las ventas totales por mes se agrupan y convierten a millones para simplificar la interpretación. "
                "Se utilizan líneas y marcadores para resaltar los picos estacionales y facilitar la identificación de tendencias."
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Ventas por día de la semana: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Este gráfico detalla las ventas promedio según el día de la semana, permitiendo identificar los días con mayor actividad. "
                "Los datos se agrupan por día y se representan en un gráfico de líneas con marcadores para resaltar los patrones."
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Ventas por estado: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Un gráfico de barras que desglosa las ventas por estado, destacando las regiones con mayor rendimiento. Los datos se ordenan en orden descendente "
                "para facilitar el análisis visual de los estados más relevantes."
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Ventas en días laborales y festivos: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Un gráfico comparativo que analiza las diferencias de ventas entre días laborales y festivos. Las ventas se agrupan por tipo de día y se representan "
                "en un gráfico de barras para visualizar cómo el contexto afecta el comportamiento de los consumidores."
            ], style={'marginBottom': '10px'}),
        ])
    ]),
   
    # Línea divisoria
    html.Br(),
    
    # Explicación de la pestaña de interactividad simple
    create_section("Análisis por Tienda", [
        "La segunda pestaña se centra en el rendimiento específico de cada tienda de la empresa. Esta sección es especialmente útil para "
        "analizar cómo las operaciones individuales contribuyen al rendimiento general y detectar patrones relevantes que pueden guiar decisiones locales.",
        "Incluye los siguientes componentes principales:",
        html.Ul([
            html.Li([
                html.Span("Menú desplegable: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Este menú permite seleccionar una tienda específica. Los identificadores únicos de las tiendas se extraen del dataset y "
                "se limpian para eliminar duplicados o inconsistencias. El diseño asegura accesibilidad, y el menú interactúa con los gráficos "
                "para mostrar datos relacionados con la tienda seleccionada."
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Gráfico de ventas anuales por tienda: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Este gráfico de barras se crea agrupando las ventas totales por año para la tienda seleccionada. Las ventas se convierten a millones "
                "para facilitar la interpretación. El gráfico utiliza una paleta de colores personalizada y es interactivo, permitiendo zoom, restablecimiento "
                "de vistas y la opción de descarga como imagen. Los datos de años incompletos se manejan para asegurar consistencia en la representación visual."
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Gráfico de ventas por producto: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Desglosa las ventas por familia de productos mediante un gráfico de barras horizontal. Los datos se agrupan por familia y se transforman a millones "
                "para mantener coherencia visual. Los colores se utilizan para diferenciar las familias de productos, y el diseño permite identificar fácilmente "
                "las familias más importantes en términos de ventas."
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Gráfico de productos en promoción: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Este gráfico de barras horizontal muestra las ventas de productos en promoción, agrupadas por familia. Los datos se filtran para incluir solo productos "
                "en promoción, y las ventas se convierten a millones. La visualización ayuda a analizar cómo las promociones impactan las ventas y a identificar "
                "familias de productos clave para futuras estrategias promocionales."
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Tabla resumen de productos en promoción: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "La tabla presenta un resumen detallado de las familias de productos promocionados. Se muestran el porcentaje de ventas en promoción de cada familia "
                "y el número total de promociones activas. Los datos se normalizan para destacar las contribuciones relativas de cada familia. Además, la tabla incluye "
                "funcionalidades de paginación y colores para mejorar la legibilidad."
            ], style={'marginBottom': '10px'})
        ])
    ]),

    # Línea divisoria
    html.Br(),
    
    # Explicación de la pestaña de análisis avanzado
    create_section("Análisis Avanzado", [
        "La tercera pestaña está diseñada para ofrecer un análisis exhaustivo que combina patrones estacionales, comparaciones multidimensionales y análisis de patrones de venta. Cada gráfico incluye características interactivas y opciones de personalización que permiten un entendimiento profundo de las dinámicas de ventas y promociones.",
        "La pestaña incluye las siguientes funcionalidades clave:",
        html.Ul([
            html.Li([
                html.Span("Análisis de Estacionalidad: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Este gráfico interactivo permite observar cómo las ventas diarias, los productos en promoción y los días festivos varían a lo largo del tiempo para un estado seleccionado.",
                html.Ul([
                    html.Li([
                        html.Span("Filtros dinámicos: ", style={'fontWeight': 'bold'}),
                        "Los datos se filtran por estado usando un menú desplegable y se selecciona un rango temporal a través de un slider interactivo."
                    ]),
                    html.Li([
                        html.Span("Variables visualizables: ", style={'fontWeight': 'bold'}),
                        "Un checklist permite al usuario elegir entre ventas diarias, productos en promoción y días festivos para incluir en el gráfico."
                    ]),
                    html.Li([
                        html.Span("Formato del gráfico: ", style={'fontWeight': 'bold'}),
                        "Se utiliza un gráfico de líneas para las ventas y promociones, con los días festivos representados como puntos rojos marcados en la línea de tiempo."
                    ]),
                    html.Li([
                        html.Span("Interactividad: ", style={'fontWeight': 'bold'}),
                        "Los usuarios pueden acercar o alejar áreas específicas para un análisis detallado, restablecer vistas, y descargar el gráfico como imagen."
                    ]),
                    html.Li([
                        html.Span("Estilo visual: ", style={'fontWeight': 'bold'}),
                        "El gráfico incluye una paleta de colores coherente con la identidad visual del dashboard, y los puntos de los días festivos destacan con un color rojo intenso."
                    ])
                ])
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Análisis Comparativo Multidimensional: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Este gráfico de burbujas está diseñado para comparar métricas clave como las ventas promedio, el porcentaje de productos en promoción y el total de transacciones.",
                html.Ul([
                    html.Li([
                        html.Span("Opciones de agrupación: ", style={'fontWeight': 'bold'}),
                        "Un menú desplegable permite agrupar los datos por tipo de tienda o por clúster, ajustando los colores de las burbujas en consecuencia."
                    ]),
                    html.Li([
                        html.Span("Ejes principales: ", style={'fontWeight': 'bold'}),
                        "El eje X representa las ventas promedio, mientras que el eje Y muestra el porcentaje de productos en promoción. El tamaño de las burbujas indica el volumen total de transacciones."
                    ]),
                    html.Li([
                        html.Span("Interactividad: ", style={'fontWeight': 'bold'}),
                        "Incluye funcionalidades de zoom, selección de puntos (box y lasso), y la capacidad de descargar la visualización."
                    ]),
                    html.Li([
                        html.Span("Leyenda: ", style={'fontWeight': 'bold'}),
                        "Proporciona información sobre los colores según la agrupación seleccionada, permitiendo destacar u ocultar categorías específicas con un solo clic."
                    ]),
                    html.Li([
                        html.Span("Estilo visual: ", style={'fontWeight': 'bold'}),
                        "Se utiliza una cuadrícula ligera para mantener el enfoque en los datos, con colores optimizados para una clara diferenciación."
                    ])
                ])
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Patrones de Venta: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Este mapa de calor visualiza las ventas según el día de la semana y la semana del año, destacando patrones temporales significativos.",
                html.Ul([
                    html.Li([
                        html.Span("Ejes del gráfico: ", style={'fontWeight': 'bold'}),
                        "El eje Y representa los días de la semana, mientras que el eje X muestra las semanas del año."
                    ]),
                    html.Li([
                        html.Span("Colores: ", style={'fontWeight': 'bold'}),
                        "La intensidad del color refleja los volúmenes de ventas. Los usuarios pueden optar por normalizar los datos a valores absolutos o relativos."
                    ]),
                    html.Li([
                        html.Span("Opciones de filtrado: ", style={'fontWeight': 'bold'}),
                        "Permite seleccionar un año base y una familia de productos específica mediante menús desplegables."
                    ]),
                    html.Li([
                        html.Span("Comparación entre años: ", style={'fontWeight': 'bold'}),
                        "Si se selecciona la opción de comparar años y se eligen dos años distintos, se muestra un mapa de calor comparativo en el que los colores indican las diferencias entre ambos años (aumentos en azul, disminuciones en rojo)."
                    ]),
                    html.Li([
                        html.Span("Caso especial: ", style={'fontWeight': 'bold'}),
                        "Si la comparación está habilitada pero el mismo año es seleccionado para ambos campos, el gráfico mostrará únicamente el mapa de calor para ese año, sin realizar comparación."
                    ]),
                    html.Li([
                        html.Span("Visualización comparativa: ", style={'fontWeight': 'bold'}),
                        "Los colores se ajustan para mostrar aumentos (azul) o disminuciones (rojo) en las ventas al comparar dos años."
                    ]),
                    html.Li([
                        html.Span("Interactividad: ", style={'fontWeight': 'bold'}),
                        "La visualización es completamente interactiva, permitiendo explorar las celdas en detalle y descargar el gráfico como imagen."
                    ])
                ])
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Comparación de Rendimiento entre Estados: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Este gráfico radar permite comparar métricas clave como ventas totales, promociones activas, transacciones realizadas y promedio de ventas por transacción entre varios estados.",
                html.Ul([
                    html.Li([
                        html.Span("Selección de estados: ", style={'fontWeight': 'bold'}),
                        "Un menú desplegable permite al usuario elegir múltiples estados a analizar."
                    ]),
                    html.Li([
                        html.Span("Normalización de datos: ", style={'fontWeight': 'bold'}),
                        "Todas las métricas se escalan de 0 a 100 para facilitar la comparación."
                    ]),
                    html.Li([
                        html.Span("Datos representados: ", style={'fontWeight': 'bold'}),
                        "Cada métrica se visualiza en un eje del radar, proporcionando una visión integral de las fortalezas y debilidades de cada estado."
                    ]),
                    html.Li([
                        html.Span("Estilo visual: ", style={'fontWeight': 'bold'}),
                        "Se utilizan colores consistentes con la identidad del dashboard y un fondo transparente para destacar los datos."
                    ])
                ])
            ], style={'marginBottom': '10px'})
        ])
    ]),

    # Línea divisoria
    html.Br(),
    
    # Explicación de decisiones de diseño
    create_section("Decisiones de diseño", [
        "El diseño del dashboard sigue principios claros de simplicidad, funcionalidad y estética:",
        html.Ul([
            html.Li([
                html.Span("Simplicidad: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Cada pestaña está estructurada de manera lógica, permitiendo a los usuarios centrarse en las métricas y gráficos relevantes sin distracciones."
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Funcionalidad: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Se priorizó la interactividad en todas las visualizaciones, incluyendo opciones como filtros, zoom y tooltips. Esto permite un análisis "
                "dinámico y adaptado a las necesidades específicas de cada usuario."
            ], style={'marginBottom': '10px'}),
            html.Li([
                html.Span("Estética: ", style={'color': '#26a69a','fontWeight': 'bold'}),
                "Los colores y estilos utilizados se seleccionaron para garantizar una experiencia visual agradable y profesional. Los bordes redondeados y "
                "las sombras sutiles aportan una apariencia moderna y pulida."
            ], style={'marginBottom': '10px'})
        ]),
        "\nFinalmente, el código está completamente documentado para facilitar su comprensión y futura ampliación. Cada cálculo o funcionalidad implementada "
        "ha sido explicada con detalle, asegurando transparencia en todo el desarrollo."
    ]),
    
    # Línea divisoria
    html.Br(),
    
    # Firma a pie de página
    firma_pag()

], style={'background-color': '#eaf4eb', 'padding': '20px','border-radius': '20px', 'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)','margin-top': '10px'})

