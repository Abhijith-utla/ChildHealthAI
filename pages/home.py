import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import os

dash.register_page(__name__, path='/')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Row([
                    # Left side content
                    dbc.Col([
                        html.Div([
                            html.H1("Child Health AI", 
                                    className="display-4 mb-4", 
                                    style={"font-weight": "bold", "color": "white"}),
                            html.P("Advanced machine learning for pediatric health prediction", 
                                  className="lead mb-4",
                                  style={"color": "primary"}),
                            html.P("Our AI-powered platform analyzes health factors to provide early detection of potential health conditions, enabling proactive care and better outcomes.",
                                  className="mb-5",
                                  style={"color": "#A0AEC0"}),
                            dbc.Button("Predict Now", 
                                      color="primary", 
                                      size="lg", 
                                      href="/predictor", 
                                      className="me-3",
                                      style={"background-color": "#3498db", "border-color": "#3498db"}),
                            dbc.Button("Explore Data", 
                                      outline=True, 
                                      color="light", 
                                      size="lg", 
                                      href="/explorer",
                                      style={"color": "#3498db", "border-color": "#3498db"}),
                        ], className="py-5")
                    ], md=7, sm=12),
                    
                    # Right side with GIF or video animation
                    dbc.Col([
                        html.Div([
                            # Use an image for GIF or video for MOV
                            html.Img(
                                src="/assets/ann.gif",  # Place your GIF in the assets folder
                                style={
                                "width": "auto",  # Take up full width of container
                                "height": "auto",  # Maintain aspect ratio
                                "min-height": "300px",  # Set minimum height (increase this value for larger size)
                                "object-fit": "contain",  # Ensure the entire image is visible
                                "border-radius": "10px",
                            }
                            )
                            
                            # Alternatively, if you want to use a video:
                            # html.Video(
                            #     src="/assets/medical_animation.mp4",
                            #     controls=False,
                            #     autoPlay=True,
                            #     loop=True,
                            #     muted=True,
                            #     style={
                            #         "max-width": "100%",
                            #         "max-height": "400px",
                            #         "border-radius": "10px",
                            #         "box-shadow": "0 4px 15px rgba(52, 152, 219, 0.3)"
                            #     }
                            # )
                        ], className="d-flex align-items-center justify-content-center h-100")
                    ], md=5, sm=12),
                ]),
            ], style={"background-color": "#121212", 
                      "border-radius": "15px", 
                      "padding": "60px", 
                      "box-shadow": "0 10px 30px rgba(0, 0, 0, 0.5)",
                      "border": "1px solid #2a2a2a"})
        ], width={"size": 12}),
    ], className="my-5"),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("Advanced Features", 
                       className="mb-4 text-center", 
                       style={"color": "white"}),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-brain fa-2x mb-3", style={"color": "#3498db"}),
                                html.H5("AI-Powered Analysis", className="mb-3", style={"color": "#3498db"}),
                                html.P("Machine learning algorithms trained on extensive pediatric health data to predict conditions with high accuracy.", 
                                      style={"color": "#A0AEC0"})
                            ], className="text-center")
                        ], style={"background-color": "#1a1a1a", 
                                 "border-radius": "10px", 
                                 "padding": "25px",
                                 "height": "100%",
                                 "border": "1px solid #2a2a2a"})
                    ], width=4),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-heartbeat fa-2x mb-3", style={"color": "#3498db"}),
                                html.H5("Preventive Care", className="mb-3", style={"color": "#3498db"}),
                                html.P("Identify risk factors early to enable proactive interventions and improved health outcomes.", 
                                      style={"color": "#A0AEC0"})
                            ], className="text-center")
                        ], style={"background-color": "#1a1a1a", 
                                 "border-radius": "10px", 
                                 "padding": "25px",
                                 "height": "100%",
                                 "border": "1px solid #2a2a2a"})
                    ], width=4),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-chart-bar fa-2x mb-3", style={"color": "#3498db"}),
                                html.H5("Data Exploration", className="mb-3", style={"color": "#3498db"}),
                                html.P("Interactive visualization tools to explore health data patterns and correlations.", 
                                      style={"color": "#A0AEC0"})
                            ], className="text-center")
                        ], style={"background-color": "#1a1a1a", 
                                 "border-radius": "10px", 
                                 "padding": "25px",
                                 "height": "100%",
                                 "border": "1px solid #2a2a2a"})
                    ], width=4),
                ]),
            ], style={"background-color": "#121212", 
                     "border-radius": "15px", 
                     "padding": "30px",
                     "box-shadow": "0 10px 30px rgba(0, 0, 0, 0.5)",
                     "border": "1px solid #2a2a2a"})
        ], width={"size": 12}),
    ], className="mb-5"),
    
    # Special section highlighting the benefits
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("Why Choose ChildHealth_AI?", 
                       className="mb-4 text-center", 
                       style={"color": "white"}),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.H1("75%", className="display-4 mb-2", style={"color": "#3498db"}),
                                html.P("Prediction Accuracy", style={"color": "#A0AEC0"})
                            ], className="text-center")
                        ], style={"background-color": "#1a1a1a", 
                                 "border-radius": "10px", 
                                 "padding": "25px",
                                 "height": "100%",
                                 "border": "1px solid #2a2a2a"})
                    ], width=4),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.H1("12+", className="display-4 mb-2", style={"color": "#3498db"}),
                                html.P("Health Conditions Detected", style={"color": "#A0AEC0"})
                            ], className="text-center")
                        ], style={"background-color": "#1a1a1a", 
                                 "border-radius": "10px", 
                                 "padding": "25px",
                                 "height": "100%",
                                 "border": "1px solid #2a2a2a"})
                    ], width=4),
                    dbc.Col([
                        html.Div([
                            html.Div([
                                html.H1("33+", className="display-4 mb-2", style={"color": "#3498db"}),
                                html.P("Risk Factors Analyzed", style={"color": "#A0AEC0"})
                            ], className="text-center")
                        ], style={"background-color": "#1a1a1a", 
                                 "border-radius": "10px", 
                                 "padding": "25px",
                                 "height": "100%",
                                 "border": "1px solid #2a2a2a"})
                    ], width=4),
                ]),
            ], style={"background-color": "#121212", 
                     "border-radius": "15px", 
                     "padding": "30px",
                     "box-shadow": "0 10px 30px rgba(0, 0, 0, 0.5)",
                     "border": "1px solid #2a2a2a"})
        ], width={"size": 12}),
    ], className="mb-5"),
    
    # Call-to-action section
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    dbc.Button("Try Predictor Now", 
                              color="primary", 
                              size="lg", 
                              href="/predictor",
                              className="px-5 py-3",
                              style={"background-color": "#3498db", "border-color": "#3498db"}),
                ], className="text-center")
            ], style={"background-color": "#121212", 
                     "border-radius": "15px", 
                     "padding": "20px",
                     "box-shadow": "0 10px 30px rgba(0, 0, 0, 0.5)",
                     "border": "1px solid #2a2a2a"})
        ], width={"size": 8, "offset": 2}),
    ], className="mb-5"),
    
    # Load FontAwesome for icons
    html.Link(
        rel="stylesheet",
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"
    ),
], fluid=True, style={'backgroundColor': '#0A0A0A', 'minHeight': '100vh', 'padding': '20px'})