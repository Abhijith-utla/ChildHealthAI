import pandas as pd
import numpy as np
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dash.register_page(__name__, path='/explorer')


# Load the data
data = pd.read_csv('datajoined.csv')

# Basic data cleaning
data.fillna(0, inplace=True)

# Create the Dash app with custom styling

# Define custom colors to match the theme from screenshot
background_color = '#000000'  # Black background
text_color_primary = '#ffffff'  # White text
text_color_secondary = '#4080bf'  # Blue accent matching screenshot
accent_color = '#4080bf'  # Blue accent
grid_color = '#333333'  # Dark gray for grids
plot_bg_color = 'rgba(80, 80, 80, 0.3)'  # Dark navy for card backgrounds

# Create age groups for better visualization
data['age_group'] = pd.cut(data['SC_AGE_YEARS'], bins=[0, 5, 10, 15, 20], 
                          labels=['0-5', '6-10', '11-15', '16+'])

# Calculate correlations for mental and physical health
health_cols = ['A1_MENTHEALTH', 'A1_PHYSHEALTH']
corr_matrix = data[health_cols].corr()

# Count health conditions
health_condition_cols = ['DIABETES', 'BLOOD', 'HEADACHE', 'HEART', 'K2Q35A', 
                        'K2Q30A', 'K2Q31A', 'K2Q32A', 'K2Q33A', 'K2Q34A', 
                        'K2Q40A', 'K2Q36A', 'K2Q37A']
data['health_condition_count'] = data[health_condition_cols].sum(axis=1)


# Define app layout with improved styling
layout = html.Div(
    html.Div(style={
        'backgroundColor': background_color, 
        'color': text_color_primary, 
        'padding': '20px',
        'fontFamily': '"Roboto", "Helvetica Neue", Arial, sans-serif',
        'minHeight': '100vh'
    }, children=[
        # Stats Cards Row
        html.Div([
            html.Div([
                html.Div(style={
                    'backgroundColor': '#0D1117',
                    'borderRadius': '10px',
                    'padding': '20px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'border': '1px solid #2C5282',
                    'height': '100%'
                }, children=[
                    html.H2('Overview Statistics 📊', style={'color': text_color_secondary, 'marginTop': '0'}),
                    html.Div([
                        html.Div([
                            html.H3(f"Total Records", style={'color': text_color_primary, 'marginBottom': '5px'}),
                            html.P(f"{len(data):,}", style={'color': text_color_secondary, 'fontSize': '28px', 'fontWeight': 'bold'}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                        html.Div([
                            html.H3(f"Age Range", style={'color': text_color_primary, 'marginBottom': '5px'}),
                            html.P(f"{data['SC_AGE_YEARS'].min()}-{data['SC_AGE_YEARS'].max()} years", 
                                style={'color': text_color_secondary, 'fontSize': '28px', 'fontWeight': 'bold'}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                    ]),
                    html.Div([
                        html.Div([
                            html.H3(f"Mental Health Score", style={'color': text_color_primary, 'marginBottom': '5px'}),
                            html.P(f"{data['A1_MENTHEALTH'].mean():.1f}", 
                                style={'color': text_color_secondary, 'fontSize': '28px', 'fontWeight': 'bold'}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                        html.Div([
                            html.H3(f"Physical Health Score", style={'color': text_color_primary, 'marginBottom': '5px'}),
                            html.P(f"{data['A1_PHYSHEALTH'].mean():.1f}", 
                                style={'color': text_color_secondary, 'fontSize': '28px', 'fontWeight': 'bold'}),
                        ], style={'width': '50%', 'display': 'inline-block'}),
                    ]),
                ])
            ], style={'width': '100%'})
        ], style={'display': 'flex', 'marginBottom': '30px'}),
        
        # First row of charts
        html.Div([
            html.Div([
                html.Div(style={
                    'backgroundColor': '#0D1117',
                    'borderRadius': '10px',
                    'padding': '20px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'border': '1px solid #2C5282',
                    'height': '100%'
                }, children=[
                    html.H2('Age Distribution', style={'color': text_color_secondary, 'textAlign': 'center', 'marginTop': '0'}),
                    dcc.Graph(
                        id='age-distribution',
                        figure=go.Figure()
                        .add_trace(go.Histogram(
                            x=data['SC_AGE_YEARS'],
                            xbins=dict(  # Make bins discrete with gaps
                                start=0,
                                end=20,
                                size=1
                            ),
                            marker=dict(
                                color=text_color_secondary,
                                line=dict(
                                    color='#000000',
                                    width=1
                                ),
                                opacity=0.7
                            ),
                            name='Age Count'
                        ))
                        .update_layout(
                            plot_bgcolor=background_color,
                            paper_bgcolor='rgba(80, 80, 80, 0.0)',
                            font_color=text_color_primary,
                            margin=dict(l=40, r=40, t=40, b=40),
                            xaxis=dict(
                                gridcolor=grid_color,
                                title='Age (Years)',
                                tickmode='linear',
                                tick0=0,
                                dtick=1,  # Force 1-year intervals
                                showgrid=True
                            ),
                            yaxis=dict(
                                gridcolor=grid_color,
                                title='Count',
                                showgrid=True
                            ),
                            bargap=0.2,  # Add gap between bars for discrete look
                        )
                    )
                ])
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.Div(style={
                    'backgroundColor': '#0D1117',
                    'borderRadius': '10px',
                    'padding': '20px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'border': '1px solid #2C5282',
                    'height': '100%'
                }, children=[
                    html.H2('Mental vs Physical Health', style={'color': text_color_secondary, 'textAlign': 'center', 'marginTop': '0'}),
                    # Changed to simpler bar chart instead of scatter
                    dcc.Graph(
                        id='mental-vs-physical',
                        figure=go.Figure()
                        .add_trace(go.Bar(
                            x=data['age_group'].unique(),
                            y=[data[data['age_group'] == age]['A1_MENTHEALTH'].mean() for age in data['age_group'].unique()],
                            name='Mental Health',
                            marker_color=text_color_secondary
                        ))
                        .add_trace(go.Bar(
                            x=data['age_group'].unique(),
                            y=[data[data['age_group'] == age]['A1_PHYSHEALTH'].mean() for age in data['age_group'].unique()],
                            name='Physical Health',
                            marker_color='#6ca0ff'  # Lighter blue to complement the main blue
                        ))
                        .update_layout(
                            barmode='group',
                            plot_bgcolor=background_color,
                            paper_bgcolor='rgba(80, 80, 80, 0.0)',
                            font_color=text_color_primary,
                            margin=dict(l=40, r=40, t=40, b=40),
                            xaxis=dict(gridcolor=grid_color, title='Age Group'),
                            yaxis=dict(gridcolor=grid_color, title='Average Health Score'),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                    )
                ])
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ], style={'marginBottom': '30px'}),
        
        # Second row of charts
        html.Div([
            html.Div([
                html.Div(style={
                    'backgroundColor': '#0D1117',
                    'borderRadius': '10px',
                    'padding': '20px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'border': '1px solid #2C5282',
                    'height': '100%'
                }, children=[
                    html.H2('ACE Score Distribution', style={'color': text_color_secondary, 'textAlign': 'center', 'marginTop': '0'}),
                    dcc.Graph(
                        id='ace-pie',
                        figure=px.pie(
                            data, 
                            names='ACE1', 
                            color_discrete_sequence=[text_color_secondary, '#6ca0ff', '#97b9ff', '#ccd6f6']
                        ).update_layout(
                            plot_bgcolor=background_color,
                            paper_bgcolor='rgba(80, 80, 80, 0.0)',
                            font_color=text_color_primary,
                            margin=dict(l=40, r=40, t=40, b=40),
                        )
                    )
                ])
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.Div(style={
                    'backgroundColor': '#0D1117',
                    'borderRadius': '10px',
                    'padding': '20px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'border': '1px solid #2C5282',
                    'height': '100%'
                }, children=[
                    html.H2('Health Conditions Count', style={'color': text_color_secondary, 'textAlign': 'center', 'marginTop': '0'}),
                    dcc.Graph(
                        id='health-conditions',
                        figure=px.bar(
                            data.groupby('health_condition_count').size().reset_index(name='count'),
                            x='health_condition_count',
                            y='count',
                            color_discrete_sequence=[text_color_secondary]
                        ).update_layout(
                            plot_bgcolor=background_color,
                            paper_bgcolor='rgba(80, 80, 80, 0.0)',
                            font_color=text_color_primary,
                            margin=dict(l=40, r=40, t=40, b=40),
                            xaxis=dict(gridcolor=grid_color, title='Number of Health Conditions'),
                            yaxis=dict(gridcolor=grid_color, title='Count of Children')
                        )
                    )
                ])
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ], style={'marginBottom': '30px'}),
        
        # Screen Time Chart - Changed to simpler visualization
        html.Div([
            html.Div(style={
                'backgroundColor': '#0D1117',
                'borderRadius': '10px',
                'padding': '20px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'border': '1px solid #2C5282'
            }, children=[
                html.H2('Screen Time vs Grade Performance', style={'color': text_color_secondary, 'textAlign': 'center', 'marginTop': '0'}),
                dcc.Graph(
                    id='screentime-grades',
                    figure=go.Figure()
                    .add_trace(go.Scatter(
                        x=data.groupby('SCREENTIME')['A1_GRADE'].mean().index,
                        y=data.groupby('SCREENTIME')['A1_GRADE'].mean().values,
                        mode='lines+markers',
                        line=dict(color=text_color_secondary, width=3),
                        marker=dict(size=10, color='#ffffff', line=dict(color=text_color_secondary, width=2))
                    ))
                    .update_layout(
                        plot_bgcolor=background_color,
                        paper_bgcolor='rgba(80, 80, 80, 0.0)',
                        font_color=text_color_primary,
                        margin=dict(l=40, r=40, t=40, b=40),
                        xaxis=dict(gridcolor=grid_color, title='Screen Time (Hours)'),
                        yaxis=dict(gridcolor=grid_color, title='Average Grade')
                    )
                )
            ])
        ], style={'marginBottom': '30px'}),
        
        # Data table
        html.Div([
            html.Div(style={
                'backgroundColor': '#0D1117',
                'borderRadius': '10px',
                'padding': '20px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'border': '1px solid #2C5282'
            }, children=[
                html.H2('Data Explorer', style={'color': text_color_secondary, 'marginTop': '0'}),
                dash_table.DataTable(
                    id='data-table',
                    columns=[{"name": i, "id": i} for i in data.head().columns],
                    data=data.head(10).to_dict('records'),
                    style_header={
                        'backgroundColor': '#1a1a1a',
                        'color': text_color_secondary,
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'backgroundColor': background_color,
                        'color': text_color_primary,
                        'border': '1px solid #333',
                        'padding': '10px',
                        'fontFamily': '"Roboto", sans-serif'
                    },
                    style_table={
                        'overflowX': 'auto',
                        'border': '1px solid #333'
                    }
                )
            ])
        ], style={'marginBottom': '30px'}),
        
        # Key insights
        html.Div([
            html.Div(style={
                'backgroundColor': '#0D1117',
                'borderRadius': '10px',
                'padding': '20px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'border': '1px solid #2C5282'
            }, children=[
                html.H2('Key Insights', style={'color': text_color_secondary, 'marginTop': '0'}),
                html.Div([
                    html.Div([
                        html.Div(style={
                            'backgroundColor': background_color,
                            'borderRadius': '8px',
                            'padding': '15px',
                            'marginBottom': '15px',
                            'borderLeft': f'4px solid {text_color_secondary}'
                        }, children=[
                            html.P('The average mental health score is lower than the physical health score, indicating potential focus areas for intervention.', 
                                style={'color': text_color_primary, 'margin': '0'})
                        ]),
                    ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
                    html.Div([
                        html.Div(style={
                            'backgroundColor': background_color,
                            'borderRadius': '8px',
                            'padding': '15px',
                            'marginBottom': '15px',
                            'borderLeft': f'4px solid {text_color_secondary}'
                        }, children=[
                            html.P('There appears to be a correlation between screen time and academic performance that varies by age group.', 
                                style={'color': text_color_primary, 'margin': '0'})
                        ]),
                    ], style={'width': '48%', 'display': 'inline-block'}),
                ]),
                html.Div([
                    html.Div([
                        html.Div(style={
                            'backgroundColor': background_color,
                            'borderRadius': '8px',
                            'padding': '15px',
                            'marginBottom': '15px',
                            'borderLeft': f'4px solid {text_color_secondary}'
                        }, children=[
                            html.P('Children with multiple health conditions tend to report lower mental health scores.', 
                                style={'color': text_color_primary, 'margin': '0'})
                        ]),
                    ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
                    html.Div([
                        html.Div(style={
                            'backgroundColor': background_color,
                            'borderRadius': '8px',
                            'padding': '15px',
                            'marginBottom': '15px',
                            'borderLeft': f'4px solid {text_color_secondary}'
                        }, children=[
                            html.P('ACE scores show significant impact on both mental and physical health outcomes.', 
                                style={'color': text_color_primary, 'margin': '0'})
                        ]),
                    ], style={'width': '48%', 'display': 'inline-block'}),
                ]),
            ])
        ]),
        
        # Footer
        html.Footer(
            html.P('© 2025 Health Conditions Predictor', 
                style={'color': text_color_secondary, 'textAlign': 'center', 'marginTop': '30px', 'opacity': '0.7'})
        )
    ]),
    style={
        'paddingLeft': '40px',
        'paddingRight': '40px',
        'backgroundColor': background_color  # match your base theme
    }
)