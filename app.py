import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

key_dict = "/tmp/google_creds.json"
with open(key_dict, "w") as f:
    f.write(os.getenv("GOOGLE_CREDS"))
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(key_dict, scope)
client = gspread.authorize(creds)

# # Setup


import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Open the Google Sheet by its URL or name
HSI = client.open_by_url("https://docs.google.com/spreadsheets/d/1D5V-B51Van2Vt1frrM8xkMyI9_3t-r26YFkuxv-B67M/edit")
                         
# Select a worksheet (e.g., the first sheet)
wsP = HSI.worksheet('P8')
#wsW = HSI.worksheet('W3')

# Convert to a Pandas DataFrame
dfP = pd.DataFrame(wsP.get_all_records())
#dfW = pd.DataFrame(wsW.get_all_records())

# # Dataframe Setup

Cats = ['SI', 'Index', 'Index 2', 'Type 2', 'VI']
Pera = ['SI', 'Index', 'Index 2', 'Type 2', 'VI',
         'ALL %', 'Ml %', 'Fl %', 'A %', 'M A %', 'F A %', 'J %', 'M J %', 'F J %', 'O %', 'M O %', 'F O %', 'M %', 'M M %', 'F M %']
Perz = ['SI', 'Index', 'Index 2', 'Type 2', 'VI', 'ALL %',
        'Z1 %', 'Z1 Ml %', 'Z1 Fl %', 'Z1 A %', 'Z1 J %', 'Z1 O %', 'Z1 M %', 'Z2 %', 'Z2 Ml %', 'Z2 Fl %', 'Z2 A %', 'Z2 J %', 'Z2 O %', 'Z2 M %', 
        'Z3 %', 'Z3 Ml %', 'Z3 Fl %', 'Z3 A %', 'Z3 J %', 'Z3 O %', 'Z3 M %', 'Z4 %', 'Z4 Ml %', 'Z4 Fl %', 'Z4 A %', 'Z4 J %', 'Z4 O %', 'Z4 M %' 
        ]

dfP1 = dfP[Pera]
dfP2 = dfP[Perz]

# Column renaming mapping
rename_map = {
    'A': 'Age 15-19', 'J': 'Age 20-29', 'O': 'Age 30-59', 'M': 'Age 60+', 
    'M A': 'Male(15-19)', 'M J': 'Male(20-29)', 'M O': 'Male(30-59)', 'M M': 'Male(60+)', 
    'F A': 'Female(15-19)', 'F J': 'Female(20-29)', 'F O': 'Female(30-59)', 'F M': 'Female(60+)', 
    'Ml': 'Male', 'Fl': 'Female',  'Z1': 'Zone 1', 'Z2': 'Zone 2', 'Z3': 'Zone 3', 'Z4': 'Zone 4', 
    'A %': 'Age 15-19 %', 'J %': 'Age 20-29 %', 'O %': 'Age 30-59 %', 'M %': 'Age 60+ %', 
    'M A %': 'Male(15-19) %', 'M J %': 'Male(20-29) %', 'M O %': 'Male(30-59) %', 'M M %': 'Male(60+) %', 
    'F A %': 'Female(15-19) %', 'F J %': 'Female(20-29) %', 'F O %': 'Female(30-59) %', 'F M %': 'Female(60+) %', 
    'Ml %': 'Male %', 'Fl %': 'Female %',  'Z1 %': 'Zone 1 %', 'Z2 %': 'Zone 2 %', 'Z3 %': 'Zone 3 %', 'Z4 %': 'Zone 4 %', 
    'Z1 A':'Zone 1 Age 15-19', 'Z1 A %':'Zone 1 Age 15-19 %', 'Z2 A':'Zone 2 Age 15-19', 'Z2 A %':'Zone 2 Age 15-19 %', 
    'Z3 A':'Zone 3 Age 15-19', 'Z3 A %':'Zone 3 Age 15-19 %', 'Z4 A':'Zone 4 Age 15-19', 'Z4 A %':'Zone 4 Age 15-19 %', 
    'Z1 J':'Zone 1 Age 20-29', 'Z1 J %':'Zone 1 Age 20-29 %', 'Z2 J':'Zone 2 Age 20-29', 'Z2 J %':'Zone 2 Age 20-29 %', 
    'Z3 J':'Zone 3 Age 20-29', 'Z3 J %':'Zone 3 Age 20-29 %', 'Z4 J':'Zone 4 Age 20-29', 'Z4 J %':'Zone 4 Age 20-29 %', 
    'Z1 O':'Zone 1 Age 30-59', 'Z1 O %':'Zone 1 Age 30-59 %', 'Z2 O':'Zone 2 Age 30-59', 'Z2 O %':'Zone 2 Age 30-59 %', 
    'Z3 O':'Zone 3 Age 30-59', 'Z3 O %':'Zone 3 Age 30-59 %', 'Z4 O':'Zone 4 Age 30-59', 'Z4 O %':'Zone 4 Age 30-59 %', 
    'Z1 M':'Zone 1 Age 60+', 'Z1 M %':'Zone 1 Age 60+ %', 'Z2 M':'Zone 2 Age 60+', 'Z2 M %':'Zone 2 Age 60+ %', 
    'Z3 M':'Zone 3 Age 60+', 'Z3 M %':'Zone 3 Age 60+ %', 'Z4 M':'Zone 4 Age 60+', 'Z4 M %':'Zone 4 Age 60+ %', 
    'Z1 Ml':'Zone 1 Male', 'Z1 Ml %':'Zone 1 Male %', 'Z2 Ml':'Zone 2 Male', 'Z2 Ml %':'Zone 2 Male %', 
    'Z3 Ml':'Zone 3 Male', 'Z3 Ml %':'Zone 3 Male %', 'Z4 Ml':'Zone 4 Male', 'Z4 Ml %':'Zone 4 Male %', 
    'Z1 Fl':'Zone 1 Female', 'Z1 Fl %':'Zone 1 Female %', 'Z2 Fl':'Zone 2 Female', 'Z2 Fl %':'Zone 2 Female %', 
    'Z3 Fl':'Zone 3 Female', 'Z3 Fl %':'Zone 3 Female %', 'Z4 Fl':'Zone 4 Female', 'Z4 Fl %':'Zone 4 Female %'
}

dfP = dfP.rename(columns=rename_map, errors='ignore')
dfP1 = dfP1.rename(columns=rename_map, errors='ignore')
dfP2 = dfP2.rename(columns=rename_map, errors='ignore')

dfP1 = dfP1.melt(id_vars=Cats, var_name='Category', value_name='Value')
#dfP1['Value'] = dfP1['Value'].astype(float)
dfP1['Category'] = dfP1['Category'].astype('category')

dfP2 = dfP2.melt(id_vars=Cats, var_name='Category', value_name='Value')
#dfP2['Value'] = dfP2['Value'].astype(float)
dfP2['Category'] = dfP2['Category'].astype('category')


# Dataset Configuration

dfS = {}

for index_value in dfP1["Index"].unique():
    dfS[index_value] = dfP1[dfP1["Index"] == index_value]

D1 = dfS["D1"].reset_index().copy()
D2 = dfS["D2"].reset_index().copy()
D3 = dfS["D3"].reset_index().copy()
D4 = dfS["D4"].reset_index().copy()
D5 = dfS["D5"].reset_index().copy()
D6 = dfS["D6"].reset_index().copy()
D7 = dfS["D7"].reset_index().copy()
D8 = dfS["D8"].reset_index().copy()
D9 = dfS["D9"].reset_index().copy()


dfZ = {}

for index_value in dfP2["Index"].unique():
    dfZ[index_value] = dfP2[dfP2["Index"] == index_value]

DZ1 = dfZ["D1"].reset_index().copy()
DZ2 = dfZ["D2"].reset_index().copy()
DZ3 = dfZ["D3"].reset_index().copy()
DZ4 = dfZ["D4"].reset_index().copy()
DZ5 = dfZ["D5"].reset_index().copy()
DZ6 = dfZ["D6"].reset_index().copy()
DZ7 = dfZ["D7"].reset_index().copy()
DZ8 = dfZ["D8"].reset_index().copy()
DZ9 = dfZ["D9"].reset_index().copy()


# DASH D Plot

# Full translation attempt
for name, df in dfS.items():
# Translated columns
    df['Category_en'] = df['Category']
    df['Category_es'] = df['Category'].map({
            'ALL %':'TODO %',
            'Age 15-19 %': 'Edad 15-19 %','Age 20-29 %': 'Edad 20-29 %','Age 30-59 %': 'Edad 30-59 %','Age 60+ %': 'Edad 60+ %',
            'Male %': 'Hombre %','Female %': 'Mujer %',
            'Male(15-19) %': 'Hombre(15-19) %','Male(20-29) %': 'Hombre(20-29) %',
            'Male(30-59) %': 'Hombre(30-59) %','Male(60+) %': 'Hombre(60+) %',
            'Female(15-19) %': 'Mujer(15-19) %','Female(20-29) %': 'Mujer(20-29) %',
            'Female(30-59) %': 'Mujer(30-59) %','Female(60+) %': 'Mujer(60+) %',
    })

    df['VI_en'] = df['VI']
    df['VI_es'] = df['VI'].map({
        'Extreme': 'Extremo', 'High': 'Alto', 'Medium': 'Medio', 'Low': 'Bajo'
    })
    
translations = {
    'en': {
        'title': 'Category Risk Breakdown',
        'yaxis': 'Percentage',
        'datasets': {'D1': 'Personal Security', 'D2': 'Economic Security', 'D3': 'Food Security', 
                     'D4': 'Health Security', 'D5': 'Political Security', 'D6': 'Community Security', 
                     'D7': 'Environmental Security', 'D8': 'Ontological Security', 'D9': 'Technological Security'},
        'type2': {
            'Average': 'Average', 'Exposure': 'Exposure',
            'Protection': 'Protection', 'Rights': 'Rights'
        }
    },
    'es': {
        'title': 'Distribución del Riesgo por Categoría',
        'yaxis': 'Porcentaje',
        'datasets': {'D1': 'Seguridad Personal', 'D2': 'Seguridad Económica', 'D3': 'Seguridad Alimentaria', 
                     'D4': 'Seguridad Sanitaria', 'D5': 'Seguridad Política', 'D6': 'Seguridad Comunitaria', 
                     'D7': 'Seguridad Ambiental', 'D8': 'Seguridad Ontológica', 'D9': 'Seguridad Tecnológica'},
        'type2': {
            'Average': 'Promedio', 'Exposure': 'Exposición',
            'Protection': 'Protección', 'Rights': 'Derechos'
        }
    }
}

vi_order = ['Extreme', 'High', 'Medium', 'Low']
vi_colors = {'Extreme': 'red', 'High': 'orange', 'Medium': 'yellow', 'Low': 'green'}

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2(id='chart-title', style={'textAlign': 'center', 'fontFamily': 'Avenir Book'}),

    html.Div([
        html.Label('Dataset:', style={'fontFamily': 'Avenir Book'}),
        dcc.Dropdown(id='dataset-select', style={'fontFamily': 'Avenir Book'}),

        html.Label('Dimension:', style={'fontFamily': 'Avenir Book'}),
        dcc.Dropdown(id='dimension-select', style={'fontFamily': 'Avenir Book'}),

        html.Label('Language:', style={'fontFamily': 'Avenir Book'}),
        dcc.RadioItems(
        id='language-select',
        options=[
        {'label': 'English', 'value': 'en'},
        {'label': 'Español', 'value': 'es'}
        ],
        value='en',
        labelStyle={
        'display': 'inline-block',
        'padding': '6px 12px',
        'margin': '4px',
        'borderRadius': '5px',
        'border': '1px solid #ccc',
        'backgroundColor': '#f8f8f8',
        'cursor': 'pointer',
        'fontFamily': 'Avenir Book'
        },
        style={'fontFamily': 'Avenir Book'}
        )
    ], style={'width': '60%', 'margin': 'auto', 'padding': '20px'}),

    dcc.Graph(id='bar-chart')
], style={'fontFamily': 'Avenir Book'})

@app.callback(
    Output('dataset-select', 'options'),
    Output('dataset-select', 'value'),
    Output('dimension-select', 'options'),
    Output('dimension-select', 'value'),
    Input('language-select', 'value')
)
def update_dropdowns(lang):
    dataset_options = [{'label': translations[lang]['datasets'][k], 'value': k} for k in datasets.keys()]
    dimension_options = [{'label': translations[lang]['type2'][k], 'value': k} for k in ['Average', 'Exposure', 'Protection', 'Rights']]
    return dataset_options, 'D1', dimension_options, 'Average'

@app.callback(
    Output('bar-chart', 'figure'),
    Output('chart-title', 'children'),
    Input('dataset-select', 'value'),
    Input('dimension-select', 'value'),
    Input('language-select', 'value')
)
def update_chart(dataset_key, dimension_key, lang):
    df = datasets[dataset_key]
    df = df[df['Type 2'] == dimension_key].copy()
    df['Percentage'] = df['Value'] * 100

    # Use translated columns
    x_column = 'Category_' + lang
    color_column = 'VI_' + lang

    # Build legend order and color map in target language
    vi_labels = [df[f'VI_{lang}'][df['VI'] == vi].iloc[0] for vi in vi_order]
    color_map = {df[f'VI_{lang}'][df['VI'] == vi].iloc[0]: vi_colors[vi] for vi in vi_order}

    fig = px.bar(
        df,
        x=x_column,
        y='Percentage',
        color=color_column,
        category_orders={color_column: vi_labels},
        color_discrete_map=color_map,
        text=df['Percentage'].round(1).astype(str) + '%'
    )

    fig.update_layout(
        barmode='stack',
        yaxis=dict(
            title=translations[lang]['yaxis'],
            range=[0, 100],
            ticksuffix='%'
        ),
        title=dict(
            text=f"{translations[lang]['title']} – {translations[lang]['type2'][dimension_key]} ({translations[lang]['datasets'][dataset_key]})",
            x=0.5
        ),
        font=dict(
        family="Avenir Book",  # Set font family here
        size=14,               # Optional: adjust font size
        color='black'          # Optional: adjust font color
        ),
        legend_title_text='',
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    return fig, translations[lang]['title']

if __name__ == '__main__':
    app.run_server(debug=False, port=8080, host='0.0.0.0')

