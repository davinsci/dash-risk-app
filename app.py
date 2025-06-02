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
        'Extreme': 'Extrema', 'High': 'Alta', 'Medium': 'Media', 'Low': 'Baja'
    })
    
    df['VI_desc (EN)'] = df['VI (EN)'].map({
        'Extreme': 'Exposure to a high number of threats and lack of means of protection against them.',
        'High': 'Exposure to multiple risk factors and limited access to protection mechanisms.',
        'Medium': 'Some threat factors present, but partial access to means to mitigate them.',
        'Low': 'Certain risks may exist, but threats are neither imminent nor severe.'
    })
    df['VI_desc (ES)'] = df['VI (EN)'].map({
        'Extreme': 'Existe gran cantidad de amenazas y no se cuenta con medios efectivos para protegersede estas.',
        'High': 'Exposición a varios factores de riesgo y acceso limitado a mecanismos de protección.',
        'Medium': 'Existen factores de amenaza y hay acceso parcial a medios para mitigar dichas amenazas.',
        'Low': 'Existen ciertos riesgos, pero las amenazas no son inminentes o severas.'
    })
    
translations = {
    '(EN)': {
        'title': 'Vulnerability Level per Dimension',
        'yaxis': 'Percentage',
        'dimensions': {'D1': 'Personal Security', 'D2': 'Economic Security', 'D3': 'Food Security', 
                     'D4': 'Health Security', 'D5': 'Political Security', 'D6': 'Community Security', 
                     'D7': 'Environmental Security', 'D8': 'Ontological Security', 'D9': 'Technological Security'},
        'components': {
            'Average': 'Level of Vulnerability', 'Exposure': 'Level of Exposure to Threats',
            'Protection': 'Level of Access to Protection Mechanisms', 'Rights': 'Level of Freedom to Exercise Rights'
        }
    },
    '(ES)': {
        'title': 'Nivel de vulnerabilidad por dimensión',
        'yaxis': 'Porcentaje',
        'dimensions': {'D1': 'Seguridad Personal', 'D2': 'Seguridad Económica', 'D3': 'Seguridad Alimentaria', 
                     'D4': 'Seguridad Sanitaria', 'D5': 'Seguridad Política', 'D6': 'Seguridad Comunitaria', 
                     'D7': 'Seguridad Ambiental', 'D8': 'Seguridad Ontológica', 'D9': 'Seguridad Tecnológica'},
        'components': {
            'Average': 'Nivel de Vulnerabilidad', 'Exposure': 'Nivel de Exposición a Amenazas',
            'Protection': 'Nivel de Acceso a Mecanismos de Protección', 'Rights': 'Nivel de Libertad para Ejercer Derechos'
        }
    }
}

vi_order = ['Extreme', 'High', 'Medium', 'Low']
vi_colors = {'Extreme': 'red', 'High': 'orange', 'Medium': 'yellow', 'Low': 'green'}

intro_descriptions = {
    '(EN)': "The Glocal Human Security Index measures individuals' levels of vulnerability\
        across nine dimensions by integrating the scores of three components: \
        Exposure to Threats; Access to Protection Mechanisms; and Freedom to Exercise Rights.",
    '(ES)': "El Índice Glocal de Seguridad Humana mide el nivel de vulnerabilidad \
        de las personas en nueve dimensiones, integrando los puntajes de tres componentes:\
        Exposición a Amenazas; Acceso a Mecanismos de Protección; y Libertad para Ejercer Derechos."
}

component_descriptions = {
    '(EN)': {
        'Average': 'Weighted average of scores for exposure to threats, access to protection, and freedom to exercise rights.',
        'Exposure': 'Exposure to threats: How exposed was the person to factors and situations that endangered their life, livelihood, or rights?',
        'Protection': 'Access to protection mechanisms: How accessible and effective were the resources, services, or support systems to protect against or recover from those threats?',
        'Rights': 'Freedom to exercise rights: To what extent was the person able to fully and freely exercise their rights without restrictions?'
    },
    '(ES)': {
        'Average': 'Promedio ponderado de las puntuaciones sobre la exposición a amenazas, el acceso a protección y la libertad para ejercer derechos.',
        'Exposure': 'Exposición a amenazas: ¿Qué tan expuesta estuvo la persona a situaciones que ponen en riesgo su vida, sustento o derechos?',
        'Protection': 'Acceso a mecanismos de protección: ¿Qué tan accesibles y eficaces fueron los recursos, servicios o apoyos para protegerse o recuperarse frente a esas amenazas?',
        'Rights': 'Libertad para ejercer derechos: ¿Qué tanto margen tuvo la persona para ejercer sus derechos de manera plena y sin restricciones?'
    }
}

dimension_descriptions = {
    '(EN)': {
        'D1': 'Protection from harm caused by any form of violence.', 
        'D2': 'Protection of livelihoods.', 
        'D3': 'Protection of reliable access to food and adequate nutrition.', 
        'D4': 'Protection of physical and mental health and access to quality medical services.', 
        'D5': 'Protection of fundamental rights, including the right to participate in public affairs.', 
        'D6': 'Protection of peaceful coexistence among community members and their ability to function as support systems.', 
        'D7': 'Protection from disasters, environmental threats, and hazardous conditions in the built environment.', 
        'D8': "Protection of dignity and a person's sense of social relevance.", 
        'D9': 'Protection from risks associated with technology use and access to its benefits.'
    },
    '(ES)': {
        'D1': 'Protección frente a daños causados por cualquier forma de violencia.', 
        'D2': 'Protección de los medios de vida', 
        'D3': 'Protección del acceso confiable a alimentos y a una nutrición adecuada.', 
        'D4': 'Protección de la salud mental y física y del acceso a servicios médicos de calidad.', 
        'D5': 'Protección de los derechos fundamentales, incluido el derecho a participar en asuntos públicos.', 
        'D6': 'Protección de la convivencia pacífica entre miembros de una comunidad y su capacidad para funcionar como sistemas de apoyo.', 
        'D7': 'Protección frente a desastres, amenazas ambientales y condiciones peligrosas del entorno construido.', 
        'D8': 'Protección de la dignidad y el sentido de relevancia social de las personas.', 
        'D9': 'Protección frente a los riesgos derivados del uso de tecnologías y acceso a sus beneficios.'
    }
}

# DASH Bar Plot - By Age & Gender
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2(id='chart-title', style={'textAlign': 'center', 'fontFamily': 'Avenir Book'}),

    html.Div(id='intro-description', style={
        'textAlign': 'center', 'fontFamily': 'Avenir Book',
        'marginBottom': '10px', 'fontSize': '16px', 'fontStyle': 'italic'
        }),

    html.Div([
        html.Label('Dimension:', style={'fontFamily': 'Avenir Book'}),
        dcc.Dropdown(id='dimension-select', style={'fontFamily': 'Avenir Book'}),

        html.Div(id='dimension-description', style={
        'marginBottom': '10px', 'fontSize': '16px', 'fontStyle': 'italic'
        }),

        html.Label('Component:', style={'fontFamily': 'Avenir Book'}),
        dcc.Dropdown(id='component-select', style={'fontFamily': 'Avenir Book'}),

        html.Div(id='component-description', style={
        'marginBottom': '10px', 'fontSize': '16px', 'fontStyle': 'italic'
        }),

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

    dcc.Graph(id='bar-chart'),
    html.Img(src='/assets/DVS Logo 23.png', className="bottom-right-logo"
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
    Output('dimension-description', 'children'),
    Output('component-description', 'children'),
    Output('intro-description', 'children'),
    Input('dimension-select', 'value'),
    Input('component-select', 'value'),
    Input('language-select', 'value')
)
def update_chart(dimension_key, component_key, lang):
    df = dimensions[dimension_key]
    df = df[df['Type 2'] == component_key].copy()
    df['Percentage'] = df['Value'] * 100
    df['VI_desc'] = df[f'VI_desc {lang}']
    df['VI_hover'] = df[f'VI {lang}'] + '<br>' + df['VI_desc']

    # Using translated columns
    x_column = 'Category ' + lang
    color_column = 'VI ' + lang

    # Building legend order and color map
    vi_labels = [df[f'VI {lang}'][df['VI'] == vi].iloc[0] for vi in vi_order]
    color_map = {df[f'VI {lang}'][df['VI'] == vi].iloc[0]: vi_colors[vi] for vi in vi_order}

    fig = px.bar(
        df,
        x=x_column,
        y='Percentage',
        color=color_column,
        category_orders={color_column: vi_labels},
        color_discrete_map=color_map,
            text=df['Percentage'].round(1).astype(str) + '%',
        custom_data=['VI_hover'],
        hover_data=[]
    )

    fig.update_traces(
        hovertemplate='<b>%{x}<br>%{y}</b><br>%{customdata[0]}<extra></extra>')

    fig.update_layout(
        barmode='stack',
        yaxis=dict(
            title=translations[lang]['yaxis'],
            range=[0, 100],
            ticksuffix='%'
        ),
        title=dict(
            text=f"{translations[lang]['components'][component_key]} ({translations[lang]['dimensions'][dimension_key]})",
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

    description = dimension_descriptions[lang][dimension_key]
    cescription = component_descriptions[lang][component_key]
    intro_text = intro_descriptions[lang]

    return fig, translations[lang]['title'], description, cescription, intro_text

if __name__ == '__main__':
    app.run_server(debug=False, port=8000, host='0.0.0.0')

