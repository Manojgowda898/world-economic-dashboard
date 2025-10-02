# config.py - Enhanced Configuration for Global Economic Dashboard

# =============================================================================
# APPLICATION SETTINGS
# =============================================================================

# Server configuration
SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 8050,
    'debug': True,  # Set to False for production
}

# Cache settings
CACHE_CONFIG = {
    'countries_cache_hours': 24,  # Hours to cache countries list
    'data_cache_minutes': 30,     # Minutes to cache API responses
}

# =============================================================================
# WORLD BANK API SETTINGS
# =============================================================================

# API configuration
API_CONFIG = {
    'base_url': 'http://api.worldbank.org/v2',
    'timeout': 15,           # Request timeout in seconds
    'rate_limit_delay': 0.05,  # Delay between requests in seconds
    'per_page': 1000,        # Records per API call
    'max_retries': 3,        # Number of retry attempts
}

# Default data range
DEFAULT_YEARS = {
    'min_year': 2000,
    'max_year': 2023,
    'default_start': 2015,
    'default_end': 2023,
}

# =============================================================================
# ENHANCED ECONOMIC INDICATORS BY CATEGORY
# =============================================================================

# Comprehensive World Bank indicators organized by categories
ECONOMIC_INDICATORS = {
    # GDP and Growth Indicators
    'GDP (Current US$)': 'NY.GDP.MKTP.CD',
    'GDP Growth (Annual %)': 'NY.GDP.MKTP.KD.ZG', 
    'GDP Per Capita': 'NY.GDP.PCAP.CD',
    'GDP Per Capita Growth': 'NY.GDP.PCAP.KD.ZG',
    'GNI Per Capita': 'NY.GNP.PCAP.CD',
    'GNI Atlas Method': 'NY.GNP.PCAP.CD',
    'GDP Deflator': 'NY.GDP.DEFL.ZS',
    'Gross Capital Formation': 'NE.GDI.TOTL.ZS',
    'Final Consumption Expenditure': 'NE.CON.TOTL.ZS',
    
    # Inflation and Monetary Policy
    'Inflation Rate (Consumer Prices)': 'FP.CPI.TOTL.ZG',
    'Food Inflation': 'FP.CPI.FOOD.ZG',
    'Core Inflation': 'FP.CPI.TOTL.ZG',
    'Money Supply Growth': 'FM.LBL.BMNY.ZG',
    'Interest Rate': 'FR.INR.RINR',
    'Real Interest Rate': 'FR.INR.RINR',
    'Exchange Rate': 'PA.NUS.FCRF',
    'Official Exchange Rate': 'PA.NUS.FCRF',
    
    # Labor Market and Employment
    'Unemployment Rate': 'SL.UEM.TOTL.ZS',
    'Youth Unemployment': 'SL.UEM.1524.ZS',
    'Female Unemployment': 'SL.UEM.TOTL.FE.ZS',
    'Male Unemployment': 'SL.UEM.TOTL.MA.ZS',
    'Labor Force Participation': 'SL.TLF.CACT.ZS',
    'Employment in Services (%)': 'SL.SRV.EMPL.ZS',
    'Employment in Industry (%)': 'SL.IND.EMPL.ZS',
    'Employment in Agriculture (%)': 'SL.AGR.EMPL.ZS',
    'Labor Productivity': 'SL.GDP.PCAP.EM.KD',
    
    # Demographics and Population
    'Population': 'SP.POP.TOTL',
    'Population Growth': 'SP.POP.GROW',
    'Urban Population (%)': 'SP.URB.TOTL.IN.ZS',
    'Rural Population (%)': 'SP.RUR.TOTL.ZS',
    'Population Density': 'EN.POP.DNST',
    'Life Expectancy': 'SP.DYN.LE00.IN',
    'Female Life Expectancy': 'SP.DYN.LE00.FE.IN',
    'Male Life Expectancy': 'SP.DYN.LE00.MA.IN',
    'Fertility Rate': 'SP.DYN.TFRT.IN',
    'Birth Rate': 'SP.DYN.CBRT.IN',
    'Death Rate': 'SP.DYN.CDRT.IN',
    'Infant Mortality Rate': 'SP.DYN.IMRT.IN',
    'Child Mortality Rate (Under 5)': 'SH.DYN.MORT',
    'Age Dependency Ratio': 'SP.POP.DPND',
    
    # International Trade
    'Exports of Goods and Services': 'NE.EXP.GNFS.CD',
    'Imports of Goods and Services': 'NE.IMP.GNFS.CD',
    'Trade Balance': 'NE.RSB.GNFS.CD',
    'Trade (% of GDP)': 'NE.TRD.GNFS.ZS',
    'Current Account Balance': 'BN.CAB.XOKA.CD',
    'Current Account Balance (% GDP)': 'BN.CAB.XOKA.GD.ZS',
    'Merchandise Trade (% GDP)': 'TG.VAL.TOTL.GD.ZS',
    'Services Trade (% GDP)': 'BG.GSR.NFSV.GD.ZS',
    'Export Value Index': 'TX.QTY.MRCH.XD.WD',
    'Import Value Index': 'TM.QTY.MRCH.XD.WD',
    'Terms of Trade': 'TT.PRI.MRCH.XD.WD',
    
    # Foreign Investment and Capital Flows
    'Foreign Direct Investment': 'BX.KLT.DINV.CD.WD',
    'FDI Inflows (% GDP)': 'BX.KLT.DINV.WD.GD.ZS',
    'FDI Outflows': 'BM.KLT.DINV.CD.WD',
    'Portfolio Investment': 'BX.PEF.TOTL.CD.WD',
    'External Debt': 'DT.DOD.DECT.CD',
    'Total Reserves': 'FI.RES.TOTL.CD',
    'Reserves (Months of Imports)': 'FI.RES.TOTL.MO',
    
    # Government Finance
    'Government Debt (% of GDP)': 'GC.DOD.TOTL.GD.ZS',
    'Government Expenditure (% of GDP)': 'GC.XPN.TOTL.GD.ZS',
    'Government Revenue (% GDP)': 'GC.REV.TOTL.GD.ZS',
    'Tax Revenue (% of GDP)': 'GC.TAX.TOTL.GD.ZS',
    'Budget Balance (% GDP)': 'GC.BAL.TOTL.GD.ZS',
    'Military Expenditure (% of GDP)': 'MS.MIL.XPND.GD.ZS',
    'Public Debt Service': 'GC.DOD.TOTL.GD.ZS',
    
    # Infrastructure and Technology
    'Internet Users (%)': 'IT.NET.USER.ZS',
    'Mobile Subscriptions': 'IT.CEL.SETS.P2',
    'Fixed Broadband Subscriptions': 'IT.NET.BBND.P2',
    'Telephone Lines': 'IT.MLT.MAIN.P2',
    'Electric Power Consumption': 'EG.USE.ELEC.KH.PC',
    'Electricity Production': 'EG.ELC.PROD.KH',
    'Energy Use Per Capita': 'EG.USE.PCAP.KG.OE',
    'Railway Lines (km)': 'IS.RRS.TOTL.KM',
    'Road Density': 'IS.ROD.DNST.K2',
    'Air Transport Passengers': 'IS.AIR.PSGR',
    'Container Port Traffic': 'IS.SHP.GOOD.TU',
    
    # Environment and Energy
    'CO2 Emissions (kt)': 'EN.ATM.CO2E.KT',
    'CO2 Emissions Per Capita': 'EN.ATM.CO2E.PC',
    'Methane Emissions': 'EN.ATM.METH.KT.CE',
    'Nitrous Oxide Emissions': 'EN.ATM.NOXE.KT.CE',
    'Renewable Energy (%)': 'EG.FEC.RNEW.ZS',
    'Fossil Fuel Consumption': 'EG.USE.COMM.FO.ZS',
    'Forest Area (%)': 'AG.LND.FRST.ZS',
    'Agricultural Land (%)': 'AG.LND.AGRI.ZS',
    'Arable Land (%)': 'AG.LND.ARBL.ZS',
    'Water Resources': 'ER.H2O.INTR.PC',
    'PM2.5 Air Pollution': 'EN.ATM.PM25.MC.M3',
    
    # Education
    'Education Expenditure (% of GDP)': 'SE.XPD.TOTL.GD.ZS',
    'Primary Education Completion': 'SE.PRM.CMPT.ZS',
    'Secondary Education Enrollment': 'SE.SEC.NENR',
    'Tertiary Education Enrollment': 'SE.TER.ENRR',
    'Adult Literacy Rate': 'SE.ADT.LITR.ZS',
    'Youth Literacy Rate': 'SE.ADT.1524.LT.ZS',
    'Female Literacy Rate': 'SE.ADT.LITR.FE.ZS',
    'School Life Expectancy': 'SE.SCH.LIFE',
    'Primary School Enrollment': 'SE.PRM.NENR',
    'Pupil-Teacher Ratio': 'SE.PRM.ENRL.TC.ZS',
    
    # Health
    'Health Expenditure (% of GDP)': 'SH.XPD.CHEX.GD.ZS',
    'Health Expenditure Per Capita': 'SH.XPD.CHEX.PC.CD',
    'Hospital Beds (per 1000)': 'SH.MED.BEDS.ZS',
    'Physicians (per 1000)': 'SH.MED.PHYS.ZS',
    'Nurses and Midwives (per 1000)': 'SH.MED.NUMW.P3',
    'Immunization Rate (DPT)': 'SH.IMM.IDPT',
    'Immunization Rate (Measles)': 'SH.IMM.MEAS',
    'Maternal Mortality Rate': 'SH.STA.MMRT',
    'Malnutrition Prevalence': 'SH.STA.MALN.ZS',
    'HIV Prevalence': 'SH.DYN.AIDS.ZS',
    'Tuberculosis Incidence': 'SH.TBS.INCD',
    
    # Agriculture and Food Security
    'Food Production Index': 'AG.PRD.FOOD.XD',
    'Crop Production Index': 'AG.PRD.CROP.XD',
    'Livestock Production Index': 'AG.PRD.LVSK.XD',
    'Fertilizer Consumption': 'AG.CON.FERT.ZS',
    'Cereal Yield': 'AG.YLD.CREL.KG',
    'Agricultural Value Added': 'NV.AGR.TOTL.ZS',
    'Rural Population': 'SP.RUR.TOTL.ZS',
    'Permanent Cropland': 'AG.LND.CROP.ZS',
    
    # Innovation and Research
    'R&D Expenditure (% of GDP)': 'GB.XPD.RSDV.GD.ZS',
    'Researchers (per million)': 'SP.POP.SCIE.RD.P6',
    'Patent Applications': 'IP.PAT.RESD',
    'Trademark Applications': 'IP.TMK.RESD',
    'High-tech Exports (%)': 'TX.VAL.TECH.CD',
    'Scientific Publications': 'IP.JRN.ARTC.SC',
    
    # Social Protection and Poverty
    'Poverty Headcount ($1.90)': 'SI.POV.DDAY',
    'Poverty Headcount ($3.20)': 'SI.POV.LMIC',
    'Poverty Headcount ($5.50)': 'SI.POV.UMIC',
    'GINI Index': 'SI.POV.GINI',
    'Income Share - Bottom 10%': 'SI.DST.FRST.10',
    'Income Share - Top 10%': 'SI.DST.10TH.10',
    'Social Protection Coverage': 'per_si_allsi.cov_pop_tot',
}

# =============================================================================
# ENHANCED COUNTRY GROUPS
# =============================================================================

# Comprehensive country groups for analysis
COUNTRY_GROUPS = {
    'G7': {
        'name': 'G7 Advanced Economies',
        'countries': ['USA', 'JPN', 'DEU', 'GBR', 'FRA', 'ITA', 'CAN'],
        'color': 'primary',
        'description': 'Group of Seven most advanced economies'
    },
    'G20': {
        'name': 'G20 Major Economies',
        'countries': ['USA', 'CHN', 'JPN', 'DEU', 'IND', 'GBR', 'FRA', 'ITA', 'BRA', 
                     'CAN', 'RUS', 'KOR', 'AUS', 'MEX', 'IDN', 'SAU', 'TUR', 'ARG', 'ZAF'],
        'color': 'info',
        'description': 'Group of Twenty major economies'
    },
    'BRICS': {
        'name': 'BRICS Emerging Markets',
        'countries': ['BRA', 'RUS', 'IND', 'CHN', 'ZAF'],
        'color': 'warning',
        'description': 'Brazil, Russia, India, China, South Africa'
    },
    'EU_MAJOR': {
        'name': 'Major EU Economies',
        'countries': ['DEU', 'FRA', 'ITA', 'ESP', 'NLD', 'BEL', 'POL', 'GRC', 'PRT', 'AUT'],
        'color': 'info',
        'description': 'Largest European Union economies'
    },
    'ASEAN_MAJOR': {
        'name': 'Major ASEAN Economies',
        'countries': ['IDN', 'THA', 'SGP', 'MYS', 'PHL', 'VNM'],
        'color': 'success',
        'description': 'Association of Southeast Asian Nations - Major economies'
    },
    'NORDIC': {
        'name': 'Nordic Countries',
        'countries': ['SWE', 'NOR', 'DNK', 'FIN', 'ISL'],
        'color': 'secondary',
        'description': 'Northern European countries'
    },
    'MIDDLE_EAST_OIL': {
        'name': 'Middle East Oil Producers',
        'countries': ['SAU', 'ARE', 'KWT', 'QAT', 'BHR', 'OMN'],
        'color': 'dark',
        'description': 'Major oil-producing countries in the Middle East'
    },
    'AFRICA_MAJOR': {
        'name': 'Major African Economies',
        'countries': ['ZAF', 'NGA', 'EGY', 'KEN', 'ETH', 'GHA', 'TUN', 'MAR', 'AGO', 'TZA'],
        'color': 'success',
        'description': 'Largest economies in Africa'
    },
    'LATIN_AMERICA': {
        'name': 'Major Latin American Economies',
        'countries': ['BRA', 'MEX', 'ARG', 'COL', 'CHL', 'PER', 'URY', 'ECU'],
        'color': 'warning',
        'description': 'Largest economies in Latin America'
    },
    'TRANSITION_ECONOMIES': {
        'name': 'Transition Economies',
        'countries': ['RUS', 'UKR', 'KAZ', 'BLR', 'UZB', 'AZE', 'GEO', 'ARM'],
        'color': 'secondary',
        'description': 'Post-Soviet transition economies'
    },
    'SMALL_ISLAND_STATES': {
        'name': 'Small Island Developing States',
        'countries': ['FJI', 'MDV', 'MHL', 'FSM', 'NRU', 'PLW', 'SLB', 'TON', 'TUV', 'VUT'],
        'color': 'info',
        'description': 'Small island developing states facing unique challenges'
    }
}

# =============================================================================
# ENHANCED VISUALIZATION SETTINGS
# =============================================================================

# Chart configuration with modern styling
CHART_CONFIG = {
    'default_height': 500,
    'default_template': 'plotly_white',
    'color_palette': [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
    ],
    'background_color': 'rgba(248,249,250,0.8)',
    'grid_color': '#e5e5e5',
    'font_family': 'Arial, sans-serif',
    'title_font_size': 16,
    'axis_font_size': 12,
    'legend_font_size': 10,
}

# Export settings
EXPORT_CONFIG = {
    'pdf_format': 'A4',
    'pdf_margin': 20,
    'image_dpi': 300,
    'temp_dir': 'temp_exports',
    'exports_dir': 'exports',
    'max_data_points_table': 1000,
    'csv_encoding': 'utf-8',
}

# =============================================================================
# ENHANCED UI CUSTOMIZATION
# =============================================================================

# Modern Bootstrap theme and styling
UI_CONFIG = {
    'theme': 'BOOTSTRAP',
    'title': '🌍 Global Economic Dashboard',
    'subtitle': 'Comprehensive economic analysis with World Bank data',
    'show_data_table': False,  # Disabled as per requirements
    'max_table_rows': 100,
    'enable_exports': True,
    'enable_data_import': True,
    'chart_types_per_indicator': True,  # New feature
    'responsive_design': True,
    'modern_cards': True,
}

# Enhanced custom CSS
CUSTOM_CSS = """
/* Main header styling */
.bg-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

/* Card hover effects */
.card {
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

/* Chart type dropdown styling */
.chart-type-dropdown .Select-control {
    border: 1px solid #dee2e6;
    border-radius: 0.375rem;
}

/* Button enhancements */
.btn {
    border-radius: 0.5rem;
    font-weight: 500;
    transition: all 0.2s ease-in-out;
}

.btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Upload area styling */
.upload-area {
    background: linear-gradient(45deg, #f8f9fa, #e9ecef);
    border: 2px dashed #6c757d;
    transition: all 0.3s ease;
}

.upload-area:hover {
    border-color: #0d6efd;
    background: linear-gradient(45deg, #e7f3ff, #cce7ff);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .display-4 {
        font-size: 2rem;
    }
    
    .btn-group {
        flex-direction: column;
    }
    
    .btn-group .btn {
        margin-bottom: 0.5rem;
    }
}

/* Loading animation */
.dash-spinner {
    border-color: #667eea;
}

/* Alert styling */
.alert {
    border-radius: 0.75rem;
    border: none;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* Card header improvements */
.card-header {
    background: linear-gradient(90deg, #f8f9fa, #ffffff);
    border-bottom: 2px solid #e9ecef;
    font-weight: 600;
}

/* Range slider improvements */
.rc-slider-track {
    background: linear-gradient(90deg, #667eea, #764ba2);
}

.rc-slider-handle {
    border-color: #667eea;
}
"""

# =============================================================================
# ADVANCED FEATURES CONFIGURATION
# =============================================================================

# Feature flags
FEATURES = {
    'enable_caching': True,
    'enable_data_validation': True,
    'enable_error_reporting': True,
    'enable_progress_tracking': True,
    'enable_data_export': True,
    'enable_data_import': True,  # New feature
    'enable_chart_download': True,
    'individual_chart_types': True,  # New feature
    'show_data_sources': True,
    'show_last_updated': True,
    'responsive_charts': True,
    'modern_ui': True,
}

# Enhanced data validation rules
DATA_VALIDATION = {
    'min_data_points': 3,
    'max_countries_per_request': 25,
    'max_indicators_per_request': 15,
    'outlier_detection': False,
    'required_csv_columns': ['country_code', 'country_name', 'indicator', 'year', 'value'],
    'valid_file_types': ['csv'],
    'max_file_size_mb': 50,
}

# =============================================================================
# PERFORMANCE AND MONITORING
# =============================================================================

# Enhanced logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'log_file': 'dashboard.log',
    'max_file_size': '10MB',
    'backup_count': 5,
    'log_api_calls': True,
    'log_user_interactions': True,
    'log_exports': True,
    'log_imports': True,
}

# Performance monitoring
MONITORING = {
    'track_load_times': True,
    'track_api_response_times': True,
    'track_chart_render_times': True,
    'track_export_times': True,
    'alert_slow_requests': True,
    'slow_request_threshold': 30,
    'memory_usage_tracking': True,
}

# =============================================================================
# API RATE LIMITING AND OPTIMIZATION
# =============================================================================

# Enhanced API management
API_OPTIMIZATION = {
    'use_connection_pooling': True,
    'max_connections': 10,
    'request_batch_size': 5,
    'retry_backoff_factor': 1.5,
    'enable_compression': True,
    'user_agent': 'GlobalEconomicDashboard/2.0',
}