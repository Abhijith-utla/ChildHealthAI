import dash
from dash import html, dcc, callback, Input, Output, State, clientside_callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import json

# Register this page
dash.register_page(__name__, path='/results')

# Define the layout
layout = dbc.Container([
    # Hidden component that will trigger when the page loads
    html.Div(id='results-page-loaded', style={'display': 'none'}),
    
    dbc.Row([
        dbc.Col([
            html.H1("Prediction Results 💡", 
                   className="text-center mb-4", 
                   style={'color': '#63B3ED'}),
            html.P("Based on your inputs, we've analyzed the likelihood of various health conditions.", 
                  className="text-center mb-4", 
                  style={'color': '#A0AEC0'}),
        ], width=12)
    ]),
    
    # This div will be populated by the callback
    html.Div(id="results-content", className="mb-4"),
    
    # Graph for the results
    dcc.Graph(id="results-chart", className="mb-4",
             style={"display": "block", "backgroundColor": "#1A202C", 
                    "border": "1px solid #2C5282", "borderRadius": "5px", "padding": "10px"}),
    
    # Navigation buttons
    dbc.Row([
        dbc.Col([
            dbc.Button("Make New Prediction", color="primary", href="/predictor"),
        ], width={"size": 6, "offset": 3}, className="text-center mb-4")
    ]),
    
    # Important note
    dbc.Row([
        
    ], className="mb-5"),
    
    # Store component to store retrieved data
    dcc.Store(id='retrieved-data'),
    
    # Global store that will be accessed from predictor page
    dcc.Store(id="global-store", storage_type="local"),
    
], fluid=True, style={'backgroundColor': '#0A0A0A', 'minHeight': '100vh', 'padding': '20px'})

# Clientside callback to get data from localStorage when page loads
clientside_callback(
    """
    function(n) {
        const data = localStorage.getItem('global-store');
        return data ? JSON.parse(data) : null;
    }
    """,
    Output('retrieved-data', 'data'),
    Input('results-page-loaded', 'children')
)

# Callback to populate the results content and chart from retrieved data
@callback(
    [Output("results-content", "children"),
     Output("results-chart", "figure")],
    [Input("retrieved-data", "data")],
)
def update_results(data):
    if data is None:
        # If no data is passed, show warning message
        return dbc.Alert("No prediction data available. Please make a prediction first.", color="warning"), {}
    
    # Parse the data that was sent from the predictor page
    predictions = data.get('predictions', [])
    conditions = data.get('conditions', [])
    
    if not predictions or not conditions:
        return dbc.Alert("No prediction data available. Please make a prediction first.", color="warning"), {}
    
    # Divide all prediction values by 2
    predictions = [p / 2 for p in predictions]
    
    # Create dataframe for predictions
    results_df = pd.DataFrame({
        'Condition': conditions,
        'Probability': predictions,
        'Percentage': [p * 100 for p in predictions]
    })
    
    # Get top 3 conditions
    top_3 = results_df.sort_values('Probability', ascending=False).head(3).reset_index(drop=True)
    
    # Colors for the bars - adjust for dark theme
    colors = ['#63B3ED', '#4FD1C5', '#F6AD55']  # Blue, teal, orange
    
    # Create horizontal bar chart for top 3 conditions
    fig = go.Figure()
    
    for i, row in top_3.iterrows():
        fig.add_trace(go.Bar(
            y=[row['Condition']],
            x=[row['Percentage']],
            orientation='h',
            name=row['Condition'],
            marker_color=colors[i],
            text=[f"{row['Percentage']:.1f}%"],
            textposition='auto',
            textfont=dict(
                color='white'
            )
        ))
    
    fig.update_layout(
        title={
            'text': 'Top 3 Predicted Health Conditions',
            'font': {
                'color': '#E0E0E0'
            }
        },
        xaxis_title={
            'text': 'Probability (%)',
            'font': {
                'color': '#E0E0E0'
            }
        },
        yaxis={
            'categoryorder': 'total ascending',
            'tickfont': {
                'color': '#E0E0E0'
            }
        },
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        paper_bgcolor='rgba(26, 32, 44, 0.0)',  # Dark blue-gray
        plot_bgcolor='rgba(26, 32, 44, 0.7)',   # Slightly lighter
        font={
            'color': '#E0E0E0'
        }
    )
    
    # Create summary component with dark theme styling
    summary_cards = []
    for i, row in top_3.iterrows():
        risk_level = "Moderate Risk" if row['Probability'] >= 0.3 else "Low Risk"
        
        # Using different colors for dark theme
        color = "rgb(255,165,0)" if risk_level == "Moderate Risk" else "success"
        bg_color = "#2D3748" if i % 2 == 0 else "#1A202C"  # Alternating card backgrounds
        
        summary_cards.append(
            dbc.Card([
                dbc.CardHeader(row['Condition'], 
                             className="fw-bold", 
                             style={'backgroundColor': '#2C5282', 'color': '#FFFFFF'}),  # Blue header
                dbc.CardBody([
                    html.H3(f"{row['Percentage']:.1f}%", 
                          className="card-title", 
                          style={'color': colors[i]}),  # Using the same colors as the chart
                    html.P(risk_level, 
                         className=f"text-{color}", 
                         style={'fontWeight': 'bold'})
                ], style={'backgroundColor': bg_color})
            ], className="text-center mb-3")
        )
    
    # Create prediction output div
    prediction_div = html.Div([
        html.Div([
            html.P(
                className="mb-3 text-center",
                style={'color': '#A0AEC0'}  # Light blue-gray text
            ),
            dbc.Row([
                dbc.Col(card, width=4) for card in summary_cards
            ], className="justify-content-center")
        ], style={
            'backgroundColor': 'rgba(0, 0, 0, 0.0)',
            'color': '#E0E0E0',
            'border': '1px solid rgba(0, 0, 0, 0.0)',
            'borderRadius': '5px',
            'padding': '20px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)',
            'marginBottom': '15px'
        })
    ])
    
    return prediction_div, fig