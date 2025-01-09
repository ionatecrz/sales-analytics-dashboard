# config.py
import plotly.graph_objects as go

tabs_styles = {
    'height': '60px',
    'backgroundColor': 'transparent',
    'borderRadius': '8px',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
    'padding': '10px',
}

tab_style = {
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'center',
    'borderBottom': '2px solid #e0e0e0',
    'padding': '15px 25px',
    'fontWeight': 'bold',
    'fontSize': '18px',
    'color': '#4b565e',
    'backgroundColor': '#ffffff',
    'borderRadius': '8px',
    'margin': '7px',
    'transition': 'all 0.3s ease',
    'cursor': 'pointer',
}

tab_selected_style = {
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'center',
    'borderTop': '4px solid #00845b',
    'borderBottom': '3px solid #00845b',
    'backgroundColor': '#eaf5f0',
    'color': '#00845b',
    'padding': '15px 25px',
    'fontSize': '18px',
    'fontWeight': 'bold',
    'boxShadow': '0 6px 14px rgba(0, 0, 0, 0.2)',
    'borderRadius': '8px',
    'margin': '7px',
    'transition': 'all 0.3s ease',
    'cursor': 'pointer',
}

# Layout
layout = go.Layout(
    margin=go.layout.Margin(
        l=60,  
        r=60,  
        b=60,  
        t=60  
    ),
    title_font=dict(size=20, color='#006d5b', family="Arial"),
    font=dict(color='#4b565e', size=12),
    plot_bgcolor='#eaf4eb',  
    paper_bgcolor='#eaf4eb',
)
