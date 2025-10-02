# main.py - Enhanced Global Economic Dashboard with Responsive UI
import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
from datetime import datetime
import os
import io
import base64
from fpdf import FPDF
from config import (
    SERVER_CONFIG,
    CACHE_CONFIG,
    API_CONFIG,
    DEFAULT_YEARS,
    ECONOMIC_INDICATORS,
    COUNTRY_GROUPS
)

# Initialize the app. Use suppress_callback_exceptions=True for dynamic outputs
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
                suppress_callback_exceptions=True) 

app.title = "Global Economic Dashboard"

ALL_INDICATORS = ECONOMIC_INDICATORS
CHART_TYPES = [
    {"label": "📈 Line Chart", "value": "line"},
    {"label": "📊 Bar Chart", "value": "bar"},
    {"label": "🎯 Scatter Plot", "value": "scatter"},
    {"label": "📋 Area Chart", "value": "area"},
    {"label": "🗂️ Box Plot", "value": "box"},
    {"label": "🌡️ Heatmap", "value": "heatmap"},
    {"label": "📉 Histogram", "value": "histogram"}
]

_countries_cache = None
_cache_timestamp = None

# --- Utility Functions (Same as previous version) ---

def fetch_all_countries():
    """Fetch all available countries from World Bank API."""
    global _countries_cache, _cache_timestamp
    
    if (_countries_cache is not None and _cache_timestamp is not None and 
        (datetime.now() - _cache_timestamp).seconds < 86400):
        return _countries_cache

    try:
        url = "http://api.worldbank.org/v2/country?format=json&per_page=500"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        countries = {}
        if len(data) > 1 and data[1]:
            for country in data[1]:
                if country['capitalCity'] and country['longitude'] and country['latitude']:
                    countries[country['name']] = country['id']
                
        _countries_cache = dict(sorted(countries.items()))
        _cache_timestamp = datetime.now()
        return _countries_cache
        
    except Exception as e:
        print(f"Error fetching countries: {e}")
        return {
            'United States': 'USA', 'China': 'CHN', 'Japan': 'JPN', 'Germany': 'DEU',
            'India': 'IND', 'United Kingdom': 'GBR', 'France': 'FRA', 'Italy': 'ITA',
            'Brazil': 'BRA', 'Canada': 'CAN', 'Russia': 'RUS', 'South Korea': 'KOR',
        }

def fetch_country_data(country_codes, start_year=2010, end_year=2023, indicators=None):
    """Fetch data from World Bank API for given countries and indicators."""
    if isinstance(country_codes, str):
        country_codes = [country_codes]
        
    if indicators is None:
        indicators = list(ALL_INDICATORS.keys())
        
    all_data = []
    
    for country_code in country_codes:
        for indicator_name in indicators:
            if indicator_name not in ALL_INDICATORS:
                continue
                            
            indicator_code = ALL_INDICATORS[indicator_name]
            url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
            params = {
                'format': 'json',
                'date': f"{start_year}:{end_year}",
                'per_page': 1000
            }
                        
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                                
                if len(data) > 1 and data[1]:
                    for entry in data[1]:
                        if entry['value'] is not None:
                            all_data.append({
                                'country_code': country_code,
                                'country_name': entry['country']['value'],
                                'indicator': indicator_name,
                                'year': int(entry['date']),
                                'value': float(entry['value'])
                            })
                                
                time.sleep(0.05)
            except Exception as e:
                print(f"Error fetching {indicator_name} for {country_code}: {e}")
                continue

    if all_data:
        df = pd.DataFrame(all_data)
        return df.sort_values(['country_name', 'indicator', 'year'])
    else:
        return pd.DataFrame()

def create_chart(df, indicator, chart_type="line", countries=None):
    """Create a Plotly figure."""
    if df.empty:
        return go.Figure().add_annotation(
            text="No data available", xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="gray")
        )
        
    indicator_data = df[df['indicator'] == indicator].copy()
    
    if indicator_data.empty:
        return go.Figure().add_annotation(
            text=f"No data available for {indicator}", xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="gray")
        )

    if countries and 'country_code' in indicator_data.columns:
        indicator_data = indicator_data[indicator_data['country_code'].isin(countries)]
    
    if indicator_data.empty:
         return go.Figure().add_annotation(
            text=f"No data available for {indicator} with selected countries", xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False, font=dict(size=14, color="gray")
        )
        
    if chart_type == "line":
        fig = px.line(indicator_data, x="year", y="value", color="country_name",
                     title=f"📈 {indicator} - Trend Analysis",
                     labels={'value': indicator, 'year': 'Year', 'country_name': 'Country'})
    elif chart_type == "bar":
        latest_year = indicator_data['year'].max()
        latest_data = indicator_data[indicator_data['year'] == latest_year]
        fig = px.bar(latest_data, x="country_name", y="value", color="country_name",
                    title=f"📊 {indicator} ({latest_year}) - Comparison",
                    labels={'value': indicator, 'country_name': 'Country'})
        fig.update_xaxes(tickangle=45)
    elif chart_type == "scatter":
        fig = px.scatter(indicator_data, x="year", y="value", color="country_name",
                        size="value", hover_data=['country_name'],
                        title=f"🎯 {indicator} - Scatter Analysis",
                        labels={'value': indicator, 'year': 'Year'})
    elif chart_type == "area":
        fig = px.area(indicator_data, x="year", y="value", color="country_name",
                     title=f"📋 {indicator} - Area Chart",
                     labels={'value': indicator, 'year': 'Year'})
    elif chart_type == "box":
        fig = px.box(indicator_data, x="country_name", y="value",
                    title=f"🗂️ {indicator} - Distribution Analysis",
                    labels={'value': indicator, 'country_name': 'Country'})
        fig.update_xaxes(tickangle=45)
    elif chart_type == "heatmap":
        pivot_data = indicator_data.pivot_table(
            values='value', index='country_name', columns='year', aggfunc='mean'
        ).fillna(0)
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values, x=pivot_data.columns, y=pivot_data.index,
            colorscale='Viridis',
            hovertemplate='Year: %{x}<br>Country: %{y}<br>Value: %{z}<extra></extra>'
        ))
        fig.update_layout(title=f"🌡️ {indicator} - Heatmap")
    elif chart_type == "histogram":
        fig = px.histogram(indicator_data, x="value", color="country_name",
                          title=f"📉 {indicator} - Value Distribution",
                          labels={'value': indicator})
    else:
        fig = px.line(indicator_data, x="year", y="value", color="country_name",
                     title=f"📈 {indicator} - Default View")
        
    fig.update_layout(
        template="plotly_white", height=500, showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        title_font_size=16, title_x=0.5,
        margin=dict(l=50, r=50, t=80, b=100),
        plot_bgcolor='rgba(248,249,250,0.8)', paper_bgcolor='white'
    )
        
    return fig

def fig_to_base64(fig):
    """Converts a Plotly figure to a base64 encoded PNG image."""
    img_bytes = fig.to_image(format="png", width=800, height=500)
    return base64.b64encode(img_bytes).decode()

def export_to_csv(df, filename="economic_data.csv"):
    """Export data to CSV format in exports/csv folder."""
    try:
        export_dir = os.path.join("exports", "csv")
        os.makedirs(export_dir, exist_ok=True)
        filepath = os.path.join(export_dir, filename)
        export_df = df[['country_code', 'country_name', 'indicator', 'year', 'value']].copy()
        export_df.to_csv(filepath, index=False)
        return os.path.abspath(filepath)
    except Exception as e:
        print(f"Error creating CSV: {e}")
        return None

def export_to_pdf(df, chart_list, filename="economic_report.pdf"):
    """Export data, summary, and charts to PDF format in exports/pdf folder."""
    try:
        export_dir = os.path.join("exports", "pdf")
        os.makedirs(export_dir, exist_ok=True)
        filepath = os.path.join(export_dir, filename)
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 15, txt="Global Economic Dashboard Report", ln=True, align="C")
        pdf.ln(5)
        
        pdf.set_font("Arial", 'I', 10)
        timestamp_str = datetime.now().strftime('%B %d, %Y at %H:%M UTC')
        pdf.cell(0, 8, txt=f"Generated on: {timestamp_str}", ln=True, align="C")
        pdf.ln(10)
        
        # Summary Section
        if not df.empty:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, txt="Data Summary", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.cell(0, 8, txt=f"Total data points: {len(df):,}", ln=True)
            pdf.cell(0, 8, txt=f"Countries analyzed: {df['country_name'].nunique()}", ln=True)
            pdf.cell(0, 8, txt=f"Economic indicators: {df['indicator'].nunique()}", ln=True)
            pdf.cell(0, 8, txt=f"Time period: {df['year'].min()} - {df['year'].max()}", ln=True)
            pdf.cell(0, 8, txt=f"Latest data year: {df['year'].max()}", ln=True)
            pdf.ln(5)

            # Chart Section
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, txt="Visual Analysis", ln=True)
            pdf.ln(2)

            for chart_info in chart_list:
                indicator = chart_info['indicator'].encode('latin-1', 'replace').decode('latin-1')
                # Use a cleaner label for the chart type in the report
                chart_type_label = next((item['label'] for item in CHART_TYPES if item['value'] == chart_info['chart_type']), chart_info['chart_type'])
                chart_type = chart_type_label.encode('latin-1', 'replace').decode('latin-1')

                img_data = chart_info['image_b64']
                
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 8, txt=f"Indicator: {indicator}", ln=True)
                pdf.set_font("Arial", 'I', 10)
                pdf.cell(0, 6, txt=f"Chart Type: {chart_type}", ln=True)
                pdf.ln(1)
                
                if img_data:
                    pdf.image(io.BytesIO(base64.b64decode(img_data)), w=180)
                    pdf.ln(5)
                
                if pdf.get_y() > 250:
                    pdf.add_page()
                    pdf.ln(5)

        # Footer
        pdf.ln(10)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 8, txt="Data source: World Bank Open Data API", ln=True, align="C")
        
        pdf.output(filepath)
        return os.path.abspath(filepath)
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None

def parse_uploaded_csv(contents, filename):
    """Parse uploaded CSV file and return DataFrame."""
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            required_cols = ['country_code', 'country_name', 'indicator', 'year', 'value']
            if not all(col in df.columns for col in required_cols):
                return None, f"CSV must contain columns: {', '.join(required_cols)}"
            
            df = df[required_cols].copy()
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df.dropna()
            
            return df, "✅ CSV uploaded successfully!"
        else:
            return None, "Please upload a CSV file"
            
    except Exception as e:
        return None, f"Error processing file: {str(e)}"


# --- Layout (FIXED FOR RESPONSIVENESS AND BUTTON PLACEMENT) ---
app.layout = dbc.Container([
    # Header (Responsive)
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("🌍 Global Economic Dashboard", className="display-4 fw-bold text-white mb-2"),
                html.P("Real-time economic indicators from World Bank API", className="lead text-white-50"),
            ], className="text-center py-5 bg-primary rounded-3 shadow-sm mb-4")
        ], xs=12) # Full width on all sizes
    ]),
    
    # 1. Data Controls Card (Responsive)
    dbc.Card([
        dbc.CardHeader([html.H4("🎛️ Data Controls", className="mb-0 text-primary")]),
        dbc.CardBody([
            dbc.Row([
                # Country Selection
                dbc.Col([
                    html.Label("🌍 Select Countries", className="fw-bold mb-2"),
                    dcc.Loading([
                        dcc.Dropdown(id="country-dropdown", placeholder="Loading countries...",
                                   multi=True, value=[], className="mb-3")
                    ]),
                    html.Div([
                        dbc.ButtonGroup([
                            dbc.Button("G7", id="select-g7", size="sm", color="outline-primary"),
                            dbc.Button("BRICS", id="select-brics", size="sm", color="outline-success"),
                            dbc.Button("EU", id="select-eu", size="sm", color="outline-info"),
                            dbc.Button("Clear", id="clear-countries", size="sm", color="outline-secondary")
                        ], className="w-100")
                    ], className="mb-3"),
                ], xs=12, md=6, lg=4), # Stack on mobile, side-by-side on tablet/desktop
                                
                # Indicators Selection
                dbc.Col([
                    html.Label("📊 Select Economic Indicators", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        id="indicator-dropdown",
                        options=[{"label": ind, "value": ind} for ind in sorted(ALL_INDICATORS.keys())],
                        value=["GDP (Current US$)", "GDP Growth (Annual %)"],
                        multi=True, className="mb-2"
                    ),
                    html.Div([
                        dbc.Button("Clear Indicators", id="clear-indicators", size="sm",
                                 color="outline-secondary", className="w-100")
                    ], className="mb-3"),
                ], xs=12, md=6, lg=4), # Stack on mobile, side-by-side on tablet/desktop
                                
                # Year Range and Action Buttons
                dbc.Col([
                    html.Label("📅 Year Range", className="fw-bold mb-2"),
                    dcc.RangeSlider(
                        id="year-slider", min=2000, max=2023, step=1, value=[2018, 2023],
                        marks={y: {'label': str(y), 'style': {'fontSize': '10px'}} 
                               for y in range(2000, 2024, 4)},
                        tooltip={"placement": "bottom", "always_visible": True}, className="mb-4"
                    ),
                    
                    # Action Buttons Row (Responsive)
                    dbc.Row(className="g-2", children=[
                        dbc.Col([
                            dbc.Button("🚀 Analyze Data", id="fetch-data-btn", color="primary",
                                     size="lg", className="w-100 shadow-sm"),
                        ], xs=12, md=6),
                        # FIX: Clear All Data Button moved here
                        dbc.Col([
                            dbc.Button("🗑️ Clear All Data", id="clear-all-btn", color="danger", 
                                     size="lg", className="w-100 shadow-sm", outline=True),
                        ], xs=12, md=6)
                    ])

                ], xs=12, lg=4) # Full width on mobile/tablet, dedicated column on desktop
            ])
        ])
    ], className="mb-4 shadow-sm"),
    
    # 2. Charts Container
    html.Div(id="charts-container"), 
    
    # 3. Import Custom Data (Responsive)
    dbc.Card([
        dbc.CardHeader([html.H5("📤 Import Custom Data", className="mb-0 text-success")]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            html.I(className="bi bi-cloud-upload-fill me-2"),
                            'Drag and Drop or Click to Upload CSV File'
                        ]),
                        style={
                            'width': '100%', 'height': '60px', 'lineHeight': '60px',
                            'borderWidth': '2px', 'borderStyle': 'dashed',
                            'borderRadius': '10px', 'textAlign': 'center',
                            'backgroundColor': '#f8f9fa', 'cursor': 'pointer'
                        },
                        multiple=False
                    )
                ], xs=12, md=8), # Larger upload area
                dbc.Col([
                    dbc.Button("📊 Use Imported Data", id="use-imported-btn", color="success",
                             size="lg", className="w-100", disabled=True)
                ], xs=12, md=4) # Smaller button area
            ]),
            html.Div(id='upload-status', className="mt-2")
        ])
    ], className="mb-4 shadow-sm"),
    
    # 4. Export Section
    html.Div(id="export-section", style={"display": "none"}),
    
    # Storage
    dcc.Store(id="data-store", storage_type='session'),
    dcc.Store(id="imported-data-store", storage_type='session'),
    dcc.Store(id="countries-store", storage_type='session'),
    dcc.Store(id="ui-state-store", storage_type='session'),
    dcc.Store(id="chart-images-store", data=[], storage_type='session') 
    
], fluid=True, className="px-4")

# --- Callbacks ---

@app.callback(
    [Output("country-dropdown", "options"),
     Output("country-dropdown", "placeholder"),
     Output("countries-store", "data")],
    Input("country-dropdown", "id")
)
def load_countries(_):
    countries = fetch_all_countries()
    options = [{"label": f"🌍 {name}", "value": code} for name, code in countries.items()]
    return options, "Select countries to analyze...", countries

@app.callback(
    Output("country-dropdown", "value", allow_duplicate=True),
    [Input("select-g7", "n_clicks"), Input("select-brics", "n_clicks"),
     Input("select-eu", "n_clicks"), Input("clear-countries", "n_clicks")],
    [State("countries-store", "data")],
    prevent_initial_call=True
)
def update_country_selection(g7_clicks, brics_clicks, eu_clicks, clear_clicks, countries):
    if not countries:
        return []
    
    ctx = callback_context
    if not ctx.triggered:
        return []
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "select-g7":
        g7_countries = ['USA', 'JPN', 'DEU', 'GBR', 'FRA', 'ITA', 'CAN']
        return [code for code in g7_countries if code in countries.values()]
    elif button_id == "select-brics":
        brics_countries = ['BRA', 'RUS', 'IND', 'CHN', 'ZAF']
        return [code for code in brics_countries if code in countries.values()]
    elif button_id == "select-eu":
        eu_countries = ['DEU', 'FRA', 'ITA', 'ESP', 'NLD', 'BEL', 'POL']
        return [code for code in eu_countries if code in countries.values()]
    elif button_id == "clear-countries":
        return []
        
    return []

@app.callback(
    Output("indicator-dropdown", "value"),
    Input("clear-indicators", "n_clicks"),
    prevent_initial_call=True
)
def clear_indicators(n_clicks):
    if n_clicks is None:
        return dash.no_update
    return []

@app.callback(
    [Output('imported-data-store', 'data', allow_duplicate=True),
     Output('upload-status', 'children', allow_duplicate=True),
     Output('use-imported-btn', 'disabled', allow_duplicate=True)],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def handle_file_upload(contents, filename):
    if contents is None:
        return {}, "", True
    
    df, message = parse_uploaded_csv(contents, filename)
    
    if df is not None:
        return df.to_dict('records'), dbc.Alert(message, color="success", className="mt-2"), False
    else:
        return {}, dbc.Alert(message, color="danger", className="mt-2"), True

@app.callback(
    [Output("charts-container", "children"),
     Output("export-section", "children"),
     Output("export-section", "style"),
     Output("data-store", "data"),
     Output("ui-state-store", "data")],
    [Input("fetch-data-btn", "n_clicks"),
     Input("use-imported-btn", "n_clicks")],
    [State("country-dropdown", "value"),
     State("indicator-dropdown", "value"),
     State("year-slider", "value"),
     State("imported-data-store", "data"),
     State("data-store", "data"),
     State("ui-state-store", "data")]
)
def fetch_and_display_data(fetch_clicks, import_clicks, selected_countries, selected_indicators,
                           year_range, imported_data, existing_data, existing_ui_state):
    """Fetch/load data and create charts/export section."""
    ctx = callback_context
    if not ctx.triggered:
        if existing_data and existing_ui_state:
            df = pd.DataFrame(existing_data)
            indicators = existing_ui_state.get('indicators', [])
            countries = existing_ui_state.get('countries', None)
            charts, export_section = create_charts_and_export(df, indicators, countries)
            return charts, export_section, {"display": "block"}, existing_data, existing_ui_state
        return [], "", {"display": "none"}, {}, {}
        
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == "use-imported-btn" and import_clicks and imported_data:
        df = pd.DataFrame(imported_data)
        indicators_in_data = df['indicator'].unique().tolist()
        data_source = "imported"
    elif trigger_id == "fetch-data-btn" and fetch_clicks and selected_countries and selected_indicators:
        df = fetch_country_data(selected_countries, year_range[0], year_range[1], selected_indicators)
        indicators_in_data = selected_indicators
        data_source = "api"
    else:
        return [], "", {"display": "none"}, {}, {}
        
    if df.empty:
        return [
            dbc.Alert("No data found. Please try different selections or upload a CSV file.",
                     color="warning", className="mt-4")
        ], "", {"display": "none"}, {}, {}
        
    charts, export_section = create_charts_and_export(
        df, indicators_in_data, 
        selected_countries if data_source == "api" else None 
    )
    
    ui_state = {
        "source": data_source,
        "indicators": indicators_in_data,
        "countries": selected_countries if data_source == "api" else df['country_code'].unique().tolist()
    }
    
    return charts, export_section, {"display": "block"}, df.to_dict('records'), ui_state


def create_charts_and_export(df, indicators, countries):
    """Helper function to generate dynamic charts and export section."""
    charts = []
    
    if not isinstance(indicators, list):
        indicators = list(indicators)

    for i, indicator in enumerate(indicators):
        if indicator not in df['indicator'].values:
            continue
            
        chart_card = dbc.Card([
            dbc.CardHeader([
                dbc.Row([
                    dbc.Col([
                        html.H5(f"📊 {indicator}", className="mb-0 text-primary")
                    ], xs=8), # Responsive chart header
                    dbc.Col([
                        dcc.Dropdown(
                            id={"type": "chart-type", "index": i},
                            options=CHART_TYPES, value="line",
                            className="chart-type-dropdown"
                        )
                    ], xs=4) # Responsive chart header
                ])
            ]),
            dbc.CardBody([
                dcc.Loading([
                    dcc.Graph(
                        id={"type": "chart", "index": i},
                        figure=create_chart(df, indicator, "line", countries),
                        config={'displayModeBar': False} 
                    )
                ])
            ])
        ], className="mb-4 shadow-sm")
        
        charts.append(chart_card)

    export_section = dbc.Card([
        dbc.CardHeader([html.H4("📁 Export Data", className="mb-0 text-success")]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        [html.I(className="bi bi-file-earmark-spreadsheet me-2"), "Export to CSV"],
                        id="export-csv-btn", color="success", size="lg", className="w-100 mb-2"
                    ),
                    html.Small("Download data in spreadsheet format", className="text-muted")
                ], xs=12, md=6), # Responsive export buttons
                dbc.Col([
                    dbc.Button(
                        [html.I(className="bi bi-file-earmark-pdf me-2"), "Export to PDF"],
                        id="export-pdf-btn", color="danger", size="lg", className="w-100 mb-2"
                    ),
                    html.Small("Download summary report", className="text-muted")
                ], xs=12, md=6) # Responsive export buttons
            ]),
            html.Div(id="export-status", className="mt-3")
        ])
    ], className="mt-4 shadow-sm")
    
    return charts, export_section

@app.callback(
    Output("chart-images-store", "data"),
    [Input({"type": "chart", "index": ALL}, "figure"),
     Input({"type": "chart-type", "index": ALL}, "value")],
    [State("ui-state-store", "data")]
)
def store_chart_images(figures, chart_types, ui_state):
    """Stores the base64 image data and metadata for each chart."""
    if not figures or not ui_state:
        return []
    
    indicators = ui_state.get('indicators', [])
    chart_data_list = []
    
    num_figures = len(figures)
    active_indicators = [ind for ind in indicators if ind in [f['layout']['title']['text'].split(' - ')[0].split('📈 ')[-1].split('📊 ')[-1].split('🎯 ')[-1].split('📋 ')[-1].split('🗂️ ')[-1].split('🌡️ ')[-1].split('📉 ')[-1] for f in figures if f.get('layout') and f['layout'].get('title')]]
    
    if len(figures) != len(active_indicators):
        active_indicators = active_indicators[:num_figures]
        chart_types = chart_types[:num_figures]
    
    for i in range(num_figures):
        fig_dict = figures[i]
        indicator = active_indicators[i] if i < len(active_indicators) else 'Unknown Indicator'
        chart_type = chart_types[i] if i < len(chart_types) else 'line'

        if fig_dict:
            try:
                fig = go.Figure(fig_dict)
                img_b64 = fig_to_base64(fig)
            except Exception as e:
                # Handle cases where the figure dict might be empty or malformed
                img_b64 = None
        else:
            img_b64 = None

        chart_data_list.append({
            'indicator': indicator,
            'chart_type': chart_type,
            'image_b64': img_b64
        })
        
    return chart_data_list

@app.callback(
    Output({"type": "chart", "index": ALL}, "figure"),
    Input({"type": "chart-type", "index": ALL}, "value"),
    [State("data-store", "data"), State("ui-state-store", "data")],
    prevent_initial_call=True
)
def update_chart_types(chart_types, stored_data, ui_state):
    if not stored_data or not ui_state:
        return []
        
    df = pd.DataFrame(stored_data)
    indicators = ui_state.get('indicators', [])
    countries = ui_state.get('countries', None)
    
    figures = []
    
    active_indicators = [ind for ind in indicators if ind in df['indicator'].values]

    if len(chart_types) != len(active_indicators):
        chart_types = ['line'] * len(active_indicators)
    
    for chart_type, indicator in zip(chart_types, active_indicators):
        fig = create_chart(df, indicator, chart_type, countries)
        figures.append(fig)
        
    return figures

@app.callback(
    Output("export-status", "children"),
    [Input("export-csv-btn", "n_clicks"),
     Input("export-pdf-btn", "n_clicks")],
    [State("data-store", "data"),
     State("chart-images-store", "data")]
)
def handle_exports(csv_clicks, pdf_clicks, stored_data, chart_images_data):
    if not stored_data:
        return ""
        
    ctx = callback_context
    if not ctx.triggered:
        return ""
        
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    df = pd.DataFrame(stored_data)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if trigger_id == "export-csv-btn" and csv_clicks:
        filepath = export_to_csv(df, f"economic_data_{timestamp}.csv")
        if filepath:
            return dbc.Alert(
                [html.I(className="bi bi-check-circle me-2"), 
                  f"✅ CSV exported successfully to: exports/csv/{os.path.basename(filepath)}"],
                color="success"
            )
        else:
            return dbc.Alert("❌ CSV export failed", color="danger")
            
    elif trigger_id == "export-pdf-btn" and pdf_clicks:
        filepath = export_to_pdf(df, chart_images_data, f"economic_report_{timestamp}.pdf")
        if filepath:
            return dbc.Alert(
                [html.I(className="bi bi-check-circle me-2"), 
                  f"✅ PDF exported successfully to: exports/pdf/{os.path.basename(filepath)}"],
                color="success"
            )
        else:
            return dbc.Alert("❌ PDF export failed. Check console for details.", color="danger")
            
    return ""

@app.callback(
    [Output("country-dropdown", "value", allow_duplicate=True),
     Output("indicator-dropdown", "value", allow_duplicate=True),
     Output("data-store", "data", allow_duplicate=True),
     Output("imported-data-store", "data", allow_duplicate=True),
     Output("ui-state-store", "data", allow_duplicate=True),
     Output("chart-images-store", "data", allow_duplicate=True),
     Output("charts-container", "children", allow_duplicate=True),
     Output("export-section", "style", allow_duplicate=True),
     Output("upload-status", "children", allow_duplicate=True),
     Output("use-imported-btn", "disabled", allow_duplicate=True)], 
    Input("clear-all-btn", "n_clicks"),
    prevent_initial_call=True
)
def clear_all_data(n_clicks):
    """Resets all UI elements and stored data."""
    if n_clicks is None:
        return dash.no_update
    
    default_indicators = ["GDP (Current US$)", "GDP Growth (Annual %)"]
    empty_data = {}
    
    return (
        [],                                 
        default_indicators,                 
        empty_data,                         
        empty_data,                         
        empty_data,                         
        [],                                 
        html.Div([]),                       
        {"display": "none"},                
        "",                                 
        True                                
    )

# Run the app
if __name__ == "__main__":
    if not os.path.exists('exports/csv'):
        os.makedirs('exports/csv')
    if not os.path.exists('exports/pdf'):
        os.makedirs('exports/pdf')
    
    fetch_all_countries() 
    
    app.run_server(
        debug=SERVER_CONFIG.get('debug', True),
        host=SERVER_CONFIG.get('host', '127.0.0.1'),
        port=SERVER_CONFIG.get('port', 8050)
    )