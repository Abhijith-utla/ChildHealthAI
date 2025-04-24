import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import requests
import json

# Register this page
dash.register_page(__name__, path='/findDoc')

# Dictionary mapping conditions to taxonomy codes
condition_taxonomy_map = {
    "Autism/ASD": "2084P0804X",  # Child & Adolescent Psychiatry
    "Learning Disability": "2084P0804X",  # Child & Adolescent Psychiatry
    "ADD/ADHD": "2084P0804X",  # Child & Adolescent Psychiatry
    "Depression": "2084P0804X",  # Child & Adolescent Psychiatry
    "Anxiety": "2084P0804X",  # Child & Adolescent Psychiatry
    "Behavior Problems": "2084P0804X",  # Child & Adolescent Psychiatry
    "Speech Disorder": "261QM0855X",  # Adolescent and Children Mental Health
    "Asthma": "261QM0801X",  # Mental Health
}

# States dropdown options
states = [
    {"label": "Alabama", "value": "AL"},
    {"label": "Alaska", "value": "AK"},
    {"label": "Arizona", "value": "AZ"},
    {"label": "Arkansas", "value": "AR"},
    {"label": "California", "value": "CA"},
    {"label": "Colorado", "value": "CO"},
    {"label": "Connecticut", "value": "CT"},
    {"label": "Delaware", "value": "DE"},
    {"label": "Florida", "value": "FL"},
    {"label": "Georgia", "value": "GA"},
    {"label": "Hawaii", "value": "HI"},
    {"label": "Idaho", "value": "ID"},
    {"label": "Illinois", "value": "IL"},
    {"label": "Indiana", "value": "IN"},
    {"label": "Iowa", "value": "IA"},
    {"label": "Kansas", "value": "KS"},
    {"label": "Kentucky", "value": "KY"},
    {"label": "Louisiana", "value": "LA"},
    {"label": "Maine", "value": "ME"},
    {"label": "Maryland", "value": "MD"},
    {"label": "Massachusetts", "value": "MA"},
    {"label": "Michigan", "value": "MI"},
    {"label": "Minnesota", "value": "MN"},
    {"label": "Mississippi", "value": "MS"},
    {"label": "Missouri", "value": "MO"},
    {"label": "Montana", "value": "MT"},
    {"label": "Nebraska", "value": "NE"},
    {"label": "Nevada", "value": "NV"},
    {"label": "New Hampshire", "value": "NH"},
    {"label": "New Jersey", "value": "NJ"},
    {"label": "New Mexico", "value": "NM"},
    {"label": "New York", "value": "NY"},
    {"label": "North Carolina", "value": "NC"},
    {"label": "North Dakota", "value": "ND"},
    {"label": "Ohio", "value": "OH"},
    {"label": "Oklahoma", "value": "OK"},
    {"label": "Oregon", "value": "OR"},
    {"label": "Pennsylvania", "value": "PA"},
    {"label": "Rhode Island", "value": "RI"},
    {"label": "South Carolina", "value": "SC"},
    {"label": "South Dakota", "value": "SD"},
    {"label": "Tennessee", "value": "TN"},
    {"label": "Texas", "value": "TX"},
    {"label": "Utah", "value": "UT"},
    {"label": "Vermont", "value": "VT"},
    {"label": "Virginia", "value": "VA"},
    {"label": "Washington", "value": "WA"},
    {"label": "West Virginia", "value": "WV"},
    {"label": "Wisconsin", "value": "WI"},
    {"label": "Wyoming", "value": "WY"},
    {"label": "District of Columbia", "value": "DC"}
]

# API functions for searching providers
def search_by_taxonomy_code(taxonomy_code, city=None, state=None, limit=5):
    """Search for healthcare providers by taxonomy code and location"""
    base_url = "https://npiregistry.cms.hhs.gov/api/"
    
    # Build query parameters
    params = {
        "version": "2.1",
        "limit": limit
    }
    
    # Use taxonomy_code parameter
    if taxonomy_code:
        params["taxonomy_code"] = taxonomy_code
    
    # Add location parameters if provided
    if city:
        params["city"] = city.upper()
    if state:
        params["state"] = state.upper()
    
    # Make the API request
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        result = response.json()
        # Check if there's an error in the response
        if "Errors" in result:
            return None
        return result
    except requests.exceptions.RequestException:
        return None

# Format the provider data for display
def format_provider_results(results):
    """Format the API results into a list of provider info dictionaries"""
    if not results or "results" not in results:
        return []

    doctors = results["results"]
    result_count = results.get("result_count", 0)
    
    if result_count == 0:
        return []
    
    formatted_providers = []
    
    for doctor in doctors:
        # Basic information
        npi = doctor.get("number")
        basic = doctor.get("basic", {})
        name = basic.get("first_name", "") + " " + basic.get("last_name", "")
        
        if not name.strip():
            name = basic.get("organization_name", "Unknown Organization")
        
        # Address information
        addresses = doctor.get("addresses", [])
        location = "No address found"
        phone = ""
        
        for address in addresses:
            if address.get("address_purpose") == "LOCATION":
                street = address.get("address_1", "")
                city = address.get("city", "")
                state = address.get("state", "")
                zip_code = address.get("postal_code", "")
                phone = address.get("telephone_number", "")
                location = f"{street}, {city}, {state} {zip_code}"
                break
        
        # Taxonomy/specialty information
        taxonomies = doctor.get("taxonomies", [])
        specialties = []
        primary_taxonomy = ""
        
        for taxonomy in taxonomies:
            desc = taxonomy.get("desc")
            primary = taxonomy.get("primary")
            
            if desc:
                if primary:
                    primary_taxonomy = f"{desc} (Primary)"
                    specialties.insert(0, primary_taxonomy)
                else:
                    specialties.append(desc)
        
        specialty_str = ", ".join(specialties) if specialties else "No specialty listed"
        
        formatted_providers.append({
            "name": name,
            "npi": npi,
            "address": location,
            "phone": phone,
            "specialty": specialty_str
        })
    
    return formatted_providers

# Define the layout for the page
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Find Healthcare Providers 🏥", 
                   className="text-center mb-4", 
                   style={'color': '#63B3ED'}),
            html.P("Based on your health predictions, we can help you find relevant healthcare providers in your area.", 
                  className="text-center mb-4", 
                  style={'color': '#A0AEC0'}),
        ], width=12)
    ]),
    
    # Location input section
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("Your Location", className="mb-3", style={'color': '#63B3ED'}),
                
                dbc.Row([
                    dbc.Col([
                        html.Label("City", className="mb-2", style={'color': 'gray'}),
                        dbc.Input(
                            id="city-input",
                            type="text",
                            placeholder="Enter city name",
                            className="mb-3",
                            style={'backgroundColor': '#1E1E1E', 'color': 'white', 'border': '1px solid #3498db'}
                        ),
                    ], width=6),
                    
                    dbc.Col([
                        html.Label("State", className="mb-2", style={'color': 'gray'}),
                        dcc.Dropdown(
                            id="state-dropdown",
                            options=states,
                            value="TX",
                            className="dash-dropdown mb-3",
                            clearable=False,
                            style={'backgroundColor': '#1E1E1E', 'color': '#FFFFFF'}
                        ),
                    ], width=6),
                ]),
                
                html.H3("Health Condition", className="mb-3 mt-3", style={'color': '#63B3ED'}),
                dcc.Dropdown(
                    id="condition-dropdown",
                    options=[{"label": condition, "value": condition} for condition in condition_taxonomy_map.keys()],
                    value=list(condition_taxonomy_map.keys())[0],
                    className="dash-dropdown mb-3",
                    clearable=False,
                    style={'backgroundColor': '#1E1E1E', 'color': '#FFFFFF'}
                ),
                
                dbc.Button(
                    "Find Providers", 
                    id="find-providers-button", 
                    color="primary", 
                    size="lg", 
                    className="w-100 mb-4",
                    style={'backgroundColor': '#2B6CB0', 'borderColor': '#2C5282'}
                ),
            ], style={
                'backgroundColor': '#0D1117',
                'color': '#E0E0E0',
                'border': '1px solid #333',
                'borderRadius': '5px',
                'padding': '15px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)',
                'marginBottom': '15px'
            })
        ], width={"size": 10, "offset": 1})
    ]),
    
    # Loading spinner
    dbc.Spinner(
        html.Div(id="provider-results-container"),
        color="primary",
        type="grow",
        fullscreen=False,
    ),
    
    # Store for global prediction data
    dcc.Store(id="global-store", storage_type="local"),
    
    # Store component to store retrieved data
    dcc.Store(id='retrieved-prediction-data'),
    
], fluid=True, style={'backgroundColor': '#0A0A0A', 'minHeight': '100vh', 'padding': '20px'})

# Callback to find providers
@callback(
    Output("provider-results-container", "children"),
    [Input("find-providers-button", "n_clicks")],
    [State("city-input", "value"),
     State("state-dropdown", "value"),
     State("condition-dropdown", "value")],
    prevent_initial_call=True
)
def find_providers(n_clicks, city, state, condition):
    if n_clicks is None or not city or not state or not condition:
        return html.Div()
    
    # Get the taxonomy code for the selected condition
    taxonomy_code = condition_taxonomy_map.get(condition)
    if not taxonomy_code:
        return dbc.Alert("No taxonomy code found for the selected condition.", color="warning")
    
    # Search for providers
    results = search_by_taxonomy_code(taxonomy_code, city=city, state=state)
    
    if not results or "results" not in results or results.get("result_count", 0) == 0:
        return dbc.Alert(f"No providers found for {condition} in {city}, {state}.", color="warning")
    
    # Format the provider results
    formatted_providers = format_provider_results(results)
    
    if not formatted_providers:
        return dbc.Alert(f"No providers found for {condition} in {city}, {state}.", color="warning")
    
    # Create a list of provider cards
    provider_cards = []
    for provider in formatted_providers:
        provider_cards.append(
            dbc.Card([
                dbc.CardHeader(provider["name"], 
                             className="fw-bold", 
                             style={'backgroundColor': '#2C5282', 'color': '#FFFFFF'}),
                dbc.CardBody([
                    html.P(f"NPI: {provider['npi']}", className="mb-2"),
                    html.P(f"Address: {provider['address']}", className="mb-2"),
                    html.P(f"Phone: {provider['phone']}", className="mb-2"),
                    html.P(f"Specialty: {provider['specialty']}", className="mb-2"),
                ], style={'backgroundColor': '#1A202C', 'color': '#E0E0E0','padding': '30px'})
            ], className="mb-5")
        )
    
    # Create the providers results display
    # Create the providers results display
    return html.Div([
        html.H3(f"Providers for {condition} in {city}, {state}", 
            className="text-center mb-4", 
            style={'color': '#63B3ED'}),
        html.Div(provider_cards)
    ], style={
        'backgroundColor': 'rgb(0,0,0,0)',
        'color': '#E0E0E0',
        'border': '1px solid rgb(0,0,0,0)',
        'borderRadius': '5px',
        'paddingTop': '100px',
        'paddingBottom':'100px',
        'paddingLeft': '140px',
        'paddingRight': '140px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)',
        'marginBottom': '15px'
    })
