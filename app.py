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

# Access Google Sheet
HSI = client.open_by_url("https://docs.google.com/spreadsheets/d/1D5V-B51Van2Vt1frrM8xkMyI9_3t-r26YFkuxv-B67M")
dfP = pd.DataFrame(HSI.worksheet('P8').get_all_records())

# Dataframe Setup
Pera = [ 'Index','Type 2','VI',
         'ALL %', 'Ml %', 'Fl %',
         'A %', 'M A %', 'F A %', 
         'J %', 'M J %', 'F J %', 
         'O %', 'M O %', 'F O %', 
         'M %', 'M M %', 'F M %', 
         ]
dfP1 = dfP[Pera]

# Column mapping
rename_map = {
    'ALL %': 'ALL', 'A %': 'Age 15-19', 'J %': 'Age 20-29', 'O %': 'Age 30-59', 'M %': 'Age 60+', 
    'M A %': 'Male(15-19)', 'M J %': 'Male(20-29)', 'M O %': 'Male(30-59)', 'M M %': 'Male(60+)', 
    'F A %': 'Female(15-19)', 'F J %': 'Female(20-29)', 'F O %': 'Female(30-59)', 'F M %': 'Female(60+)', 
    'Ml %': 'Male', 'Fl %': 'Female'
}
dfP1 = dfP1.rename(columns=rename_map, errors='ignore')
dfP1 = dfP1.melt(id_vars=['Index','Type 2','VI'], var_name='Category', value_name='Value')
dfP1['Category'] = dfP1['Category'].astype('category')

# Dataset Configuration
dimensions = {}

for index_value in dfP1["Index"].unique():
    dimensions[index_value] = dfP1[dfP1["Index"] == index_value]

D1 = dimensions["D1"].reset_index().copy()
D2 = dimensions["D2"].reset_index().copy()
D3 = dimensions["D3"].reset_index().copy()
D4 = dimensions["D4"].reset_index().copy()
D5 = dimensions["D5"].reset_index().copy()
D6 = dimensions["D6"].reset_index().copy()
D7 = dimensions["D7"].reset_index().copy()
D8 = dimensions["D8"].reset_index().copy()
D9 = dimensions["D9"].reset_index().copy()

dimensions = {
    'D1': D1,
    'D2': D2,
    'D3': D3,
    'D4': D4,
    'D5': D5,
    'D6': D6,
    'D7': D7,
    'D8': D8,
    'D9': D9
}

# Translated columns
for name, df in dimensions.items():
    df['Category (EN)'] = df['Category']
    df['Category (ES)'] = df['Category'].map({
            'ALL':'TODO',
            'Age 15-19': 'Edad 15-19','Age 20-29': 'Edad 20-29','Age 30-59': 'Edad 30-59','Age 60+': 'Edad 60+',
            'Male': 'Hombre','Female': 'Mujer',
            'Male(15-19)': 'Hombre(15-19)','Male(20-29)': 'Hombre(20-29)',
            'Male(30-59)': 'Hombre(30-59)','Male(60+)': 'Hombre(60+)',
            'Female(15-19)': 'Mujer(15-19)','Female(20-29)': 'Mujer(20-29)',
            'Female(30-59)': 'Mujer(30-59)','Female(60+)': 'Mujer(60+)',
    })

    df['VI (EN)'] = df['VI']
    df['VI (ES)'] = df['VI'].map({
        'Extreme': 'Extremo', 'High': 'Alto', 'Medium': 'Medio', 'Low': 'Bajo'
    })
    
translations = {
    '(EN)': {
        'title': 'Vulnerability Level per Dimension',
        'yaxis': 'Percentage',
        'dimensions': {'D1': 'Personal Security', 'D2': 'Economic Security', 'D3': 'Food Security', 
                     'D4': 'Health Security', 'D5': 'Political Security', 'D6': 'Community Security', 
                     'D7': 'Environmental Security', 'D8': 'Ontological Security', 'D9': 'Technological Security'},
        'components': {
            'Average': 'Average', 'Exposure': 'Exposure',
            'Protection': 'Protection', 'Rights': 'Rights'
        }
    },
    '(ES)': {
        'title': 'Nivel de vulnerabilidad por dimensión',
        'yaxis': 'Porcentaje',
        'dimensions': {'D1': 'Seguridad Personal', 'D2': 'Seguridad Económica', 'D3': 'Seguridad Alimentaria', 
                     'D4': 'Seguridad Sanitaria', 'D5': 'Seguridad Política', 'D6': 'Seguridad Comunitaria', 
                     'D7': 'Seguridad Ambiental', 'D8': 'Seguridad Ontológica', 'D9': 'Seguridad Tecnológica'},
        'components': {
            'Average': 'Promedio', 'Exposure': 'Exposición',
            'Protection': 'Protección', 'Rights': 'Derechos'
        }
    }
}

vi_order = ['Extreme', 'High', 'Medium', 'Low']
vi_colors = {'Extreme': 'red', 'High': 'orange', 'Medium': 'yellow', 'Low': 'green'}


# DASH Bar Plot - By Age & Gender
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2(id='chart-title', style={'textAlign': 'center', 'fontFamily': 'Avenir Book'}),

    html.Div([
        html.Label('Dimension:', style={'fontFamily': 'Avenir Book'}),
        dcc.Dropdown(id='dimension-select', style={'fontFamily': 'Avenir Book'}),

        html.Label('Component:', style={'fontFamily': 'Avenir Book'}),
        dcc.Dropdown(id='component-select', style={'fontFamily': 'Avenir Book'}),

        html.Label('Language:', style={'fontFamily': 'Avenir Book'}),
        dcc.RadioItems(
        id='language-select',
        options=[
        {'label': 'English', 'value': '(EN)'},
        {'label': 'Español', 'value': '(ES)'}
        ],
        value='(EN)',
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
    Output('dimension-select', 'options'),
    Output('dimension-select', 'value'),
    Output('component-select', 'options'),
    Output('component-select', 'value'),
    Input('language-select', 'value')
)
def update_dropdowns(lang):
    dimension_options = [{'label': translations[lang]['dimensions'][k], 'value': k} for k in dimensions.keys()]
    component_options = [{'label': translations[lang]['components'][k], 'value': k} for k in ['Average', 'Exposure', 'Protection', 'Rights']]
    return dimension_options, 'D1', component_options, 'Average'

@app.callback(
    Output('bar-chart', 'figure'),
    Output('chart-title', 'children'),
    Input('dimension-select', 'value'),
    Input('component-select', 'value'),
    Input('language-select', 'value')
)
def update_chart(dimension_key, component_key, lang):
    df = dimensions[dimension_key]
    df = df[df['Type 2'] == component_key].copy()
    df['Percentage'] = df['Value'] * 100
#    df['Percentage'] = pd.to_numeric(df['Percentage'], errors='coerce')

    # Use translated columns
    x_column = 'Category ' + lang
    color_column = 'VI ' + lang

    # Build legend order and color map in target language
    # vi_labels = {translations[lang]['VI'][vi] for vi in vi_order}
    vi_labels = [df[f'VI {lang}'][df['VI'] == vi].iloc[0] for vi in vi_order]
    # color_map = {translations[lang]['VI'][vi]: vi_colors[vi] for vi in vi_order}
    color_map = {df[f'VI {lang}'][df['VI'] == vi].iloc[0]: vi_colors[vi] for vi in vi_order}

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
            text=f"{translations[lang]['title']} – {translations[lang]['components'][component_key]} ({translations[lang]['dimensions'][dimension_key]})",
            x=0.5
        ),
        font=dict(
        family="Avenir Book",
        size=14,
        color='black'
        ),
        legend_title_text='',
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    return fig, translations[lang]['title']

if __name__ == '__main__':
    app.run_server(debug=False, port=8000, host='0.0.0.0')

