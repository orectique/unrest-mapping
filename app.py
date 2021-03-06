import dash
#import dash_core_components as dcc
from dash import dcc
#from dash_core_components.Markdown import Markdown
#import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


import pandas as pd
import random

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}], external_stylesheets=[dbc.themes.SUPERHERO])
app.title = 'Unrest Evaluation Mapping'
server = app.server

#
df = pd.read_csv('https://raw.githubusercontent.com/orectique/unrest-mapping/main/Factors.csv')

available_countries = df['Country'].unique()
rand_country = random.choice(available_countries)



########################################################

app.layout = html.Div([

    html.Div([
        #Title, subtitle, button
        dcc.Markdown(
                            """
                ### Quantifying events of Social Unrest: Unrest Evaluation Mapping (UEM)
                """.replace(
                                "  ", ""
                            ),
                            style = {'font-family' : '"Times New Roman", Times, serif', 'padding': '65px 10px 20px 30px'},
                        ),
        dcc.Markdown(
                            """This interactive graph is a rendition of a study which explored the creation
                            of a new mapping system to effectively capture the scale and hence enable the comparison of social unrest across countries
                            and years. Unrest Severity captures the fatality and peacefulness of protests in a country-year and Unrest Intensity represents the number of 
                            days of protest in a year. A high Unrest Severity value indicates that the events in the country-year were more violent than peaceful and saw a lot of fatalities
                            and a low Unrest Severity value implies that events in the country-year were more peaceful than violent and saw a relatively low number of fatilites.
                            
                            To use the graph, choose countries from the dropdown menu and select the range of years using the slider below. """.replace(
                                "  ", ""
                            ),
                            style = {'font-family' : '"Times New Roman", Times, serif', 'padding': '20px 10px 10px 20px'},
                        ),

        html.Div([
            html.A(
                            html.Button("View the Code Notebook on GitHub.", className="learn-more-button"),
                            href= 'https://raw.githubusercontent.com/orectique/unrest-mapping/main/Code%20Notebook',
                            target="_blank",
                        )
                    ],
                    style = {'font-family' : '"Times New Roman", Times, serif', 'float':'left','display':'inline-block', 'padding':'20px 10px 30px 20px' },
                ),

         html.Div([
        dcc.RadioItems(
            id = 'theme',
            options=[
        {'label': 'Light', 'value': 'seaborn'},
        {'label': 'Dark', 'value': 'plotly_dark'}
         ],
            value='plotly_dark',
            inputStyle={"margin-left": "10px"}),
            ], style = {'font-family' : '"Times New Roman", Times, serif', 'float': 'right', 'display': 'inline', 'padding':'25px 30px 30px 20px', 'color': 'white' }),


        html.Div([
        #country select
       
        dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= [rand_country],
                multi = True,
                clearable=False
            ),
    ], style = {'font-family' : '"Times New Roman", Times, serif', 'width' : '100%', 'float':'left', 'display': 'inline-block', 'padding': '20px 10px 30px 20px', 'color':'black'}),

    ], style = {'width' : '30%', 'float': 'left', 'display': 'inline-block'}),


    html.Div([
        #graph
        dcc.Graph(id='indicator-graphic'),

            html.Div([
        #timeline
        dcc.RangeSlider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=[df['Year'].min(), df['Year'].max()],
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    )
    ], style = {'width' : '100%', 'margin':'auto', 'display': 'inline-block', 'padding': '100px 20px 25px 20px', 'color': 'white'})
    ], style = {'width' : '70%', 'height':'100%', 'float': 'right', 'display': 'inline-block', 'padding': '70px 20px 25px 10px'}),


  
])

########################################################

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('country', 'value'),
    Input('year--slider', 'value'),
    Input('theme', 'value'),
)
def update_graph(country_names, year_value, theme_val):
    year_list = list( i for i in range(year_value[0], year_value[1] + 1))
    df1 = df[df['Country'].isin(list(country_names))]
    dff = df1[df1['Year'].isin(year_list)]
    
    if len(list(country_names)) == 0:
        df0 = pd.DataFrame({"Unrest Severity":[], "Unrest Intensity": []})
        fig = px.scatter(df0, x="Unrest Severity", y="Unrest Intensity", template = theme_val, title = "UEM Across Years")
        
    else:
        fig = px.scatter(dff, x="Unrest Severity", y="Unrest Intensity", template = theme_val, color = 'Country', hover_data=['Year'], title = "UEM Across Years")

    fig.update_xaxes(range=[-7, 7])
    fig.update_yaxes(range=[-2, 3.5])
    
    fig.update_layout(
    font_family="Times New Roman",
    title_font_family="Times New Roman")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
