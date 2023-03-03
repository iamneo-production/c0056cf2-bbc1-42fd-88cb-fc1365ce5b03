import pandas as pd
import plotly.express as px

import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from datetime import date, datetime
import geopandas as gpd
import pyproj
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")


app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LUX])

app.title = "Heat Wave and Air Index Prediction"
data22 = pd.read_csv('weather_data_2022.csv')
list_of_districts = set(data22['District'])
list_of_districts = [{'label': i, 'value': i} for i in list_of_districts]
list_of_districts = ['Adilabad', 'Karimnagar',
                     'Khammam', 'Nizamadad', 'Warangal']
pred_heat_wave = pd.read_csv("Heat Wave.csv")


def pred_plot(dataframe,value):
    upper_bound = go.Scatter(
        name='Upper Bound',
        x=dataframe['Date'],
        y=dataframe[value+'_Upper_Limit'],
        mode='lines',
        line=dict(width=0.5,
                  color="rgb(255, 188, 0)"),
        fillcolor='rgba(68, 68, 68, 0.1)',
        fill='toself')

    trace1 = go.Scatter(
        name='Temperature',
        x=dataframe['Date'],
        y=dataframe[value+'_Temp'],
        mode='lines',
        line=dict(color='rgb(31, 119, 180)'),
        fillcolor='rgba(68, 68, 68, 0.2)',
        fill='tonexty')

    lower_bound = go.Scatter(
        name='Lower Bound',
        x=dataframe['Date'],
        y=dataframe[value+'_Lower_Limit'],
        mode='lines',
        line=dict(width=0.5, color="rgb(141, 196, 26)"),)

    data = [lower_bound, upper_bound, trace1]

    layout = go.Layout(
        yaxis=dict(title='Temperature'),
        title='Predicted Temperature Range 2023',
    )

    fig = go.Figure(data=data, layout=layout)

    return fig


adilabad_card = dbc.Card(
    [
        dbc.CardImg(src=r"/static/Photo/Adilabad.png", top=True,
                    style={"width": "150px", "height": "150px", 'margin': '20px 55px 0px 55px'}),
        dbc.CardBody(
            [
                html.H4("Adilabad", className="card-title"),
                html.Div("Temperature : ",
                         id="adilabad_temp",
                         ),
            ],
        ),
    ],
    style={"font-family": "Garamond, serif",
           "width": "18rem", "margin": "5px"},
)

karimnagar_card = dbc.Card(
    [
        dbc.CardImg(src=r"/static/Photo/Karimnagar.png", top=True,
                    style={"width": "150px", "height": "150px", 'margin': '20px 55px 0px 55px'}),
        dbc.CardBody(
            [
                html.H4("Karimnagar", className="card-title"),
                html.Div("Temperature : ",
                         id="karimnagar_temp",
                         ),
            ]
        ),
    ],
    style={"font-family": "Garamond, serif",
           "width": "18rem", "margin": "5px"},
)

khammam_card = dbc.Card(
    [
        dbc.CardImg(src=r"/static/Photo/Khammam.png", top=True,
                    style={"width": "150px", "height": "150px", 'margin': '20px 55px 0px 55px'}),
        dbc.CardBody(
            [
                html.H4("Khammam", className="card-title"),
                html.Div("Temperature : ",
                         id="khammam_temp",
                         ),
            ]
        ),
    ],
    style={"font-family": "Garamond, serif",
           "width": "18rem", "margin": "5px"},
)

nizamabad_card = dbc.Card(
    [
        dbc.CardImg(src=r"/static/Photo/Nizamabad.png", top=True,
                    style={"width": "150px", "height": "150px", 'margin': '20px 55px 0px 55px'}),
        dbc.CardBody(
            [
                html.H4("Nizamabad", className="card-title"),
                html.Div("Temperature : ",
                         id="nizamabad_temp",
                         ),
            ]
        ),
    ],
    style={"font-family": "Garamond, serif",
           "width": "18rem", "margin": "5px"},
)

warangal_card = dbc.Card(
    [
        dbc.CardImg(src=r"/static/Photo/Warangal.png", top=True,
                    style={"width": "150px", "height": "150px", 'margin': '20px 55px 0px 55px'}),
        dbc.CardBody(
            [
                html.H4("Warangal", className="card-title"),
                html.Div("Temperature : ",
                         id="warangal_temp",
                         ),
            ]
        ),
    ],
    style={"font-family": "Garamond, serif",
           "width": "18rem", "margin": "5px"},
)


def func(dist):
    geo_data = gpd.read_file(
        "Telangana_Shape_Files\TS_MANDAL_BOUNDARIES_612.shp")
    geo_data.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
    dis1 = data22[data22['District'] == dist]

    dist_geo = geo_data[geo_data["Dist_Name"] == dist]
    poly_data = dist_geo['geometry']
    dist_geo.drop(columns=['geometry'], inplace=True)
    data_merged = pd.merge(
        dis1, dist_geo, left_on="Mandal", right_on="Mandal_Nam")
    # data_merged = data_merged.to_json(default_handler=str)
    # data_merged = data_merged.iloc[10::30,:]

    fig = px.choropleth(data_merged,
                        geojson=poly_data,
                        locations=data_merged.index,
                        hover_name="Mandal_Nam",
                        height=600
                        )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig


graph = dbc.Card(
    dbc.CardBody([
        dcc.Graph(
            id="graph_temp_1",
        ), ],
    ),
)

app.layout = html.Div(
    children=[
        html.Div(children=[
            html.Img(src="static/nasscom.png",
                    style={"display": "block", "margin-left": "auto", "margin-right": "auto", "padding": "50px"}),
            html.H1("TELANGANA ACADEMIC GRAND CHALLENGE ON CLIMATE CHANGE",
                    style={"font-family": "Garamond, serif", "text-align": "center"}),
            html.Br(),
            html.H4("Team WaterCooler",
                    style={"font-family": "Garamond, serif", "text-align": "center"}),
            html.Ul(
                children=[html.Li("Manav Karthikeyan"),
                        html.Li("Surya Narayan K"),
                        html.Li("Prathosh V"),
                        html.Li("RahulRam P")],
                style={"font-family": "Garamond, serif", "font-size": "20px",
                    "text-align": "center", "list-style-type": "none", "padding": "8px"}
            )
        ]),
        html.Div([
            html.H3("Predicted Heat wave values for the year 2023"),
            html.Div([
                dcc.DatePickerSingle(
                    id='date-heat',
                    initial_visible_month=date(2022, 9, 30),
                    min_date_allowed=date(2022, 9, 30),
                    max_date_allowed=date(2023, 9, 24),
                    style={"margin": "10px"},
                    date=date(2022, 9, 30),
                )]
            ),
            html.Br(),
            html.Div([
                              
                adilabad_card,
                karimnagar_card,
                khammam_card,
                nizamabad_card,
                warangal_card,
            ],
                style={"display": "flex", 'padding': "10px"},
            ),
            
        ],
            style={
            "margin": "200px", "padding": "20px"
        }),
        # html.Div(
        #     children=[
        #         html.H3("District heatmaps"),
        #         html.H6('Choose a district'),
        #         dcc.Dropdown(
        #             id="district_drp",
        #             options=list_of_districts,
        #             placeholder="Choose a district",
        #             value="Adilabad"
        #         ),
        #         dcc.Graph(id='district_graph', figure=func('Adilabad')),
        #         dcc.Graph(id='district_graph2', figure=func('Karimnagar')),
        #         dcc.Graph(id='district_graph3', figure=func('Khammam')),
        #         dcc.Graph(id='district_graph4', figure=func('Nizamadad')),
        #         dcc.Graph(id='district_graph5', figure=func('Warangal'))
        #     ],
        #     style={
        #         "margin": "200px", "padding": "20px"
        #     }
        # ),

        html.Div(
            children=[
                html.H3("Predicted Heat wave values for the year 2023"),
                html.H6('Red region denotes the occurence of heatwave'),
                dcc.Dropdown(
                    id="drop",
                    options=[
                        {'label': 'Adilabad', 'value': 'Adilabad'},
                        {'label': 'Karimnagar', 'value': 'Karimnagar'},
                        {'label': 'Khammam', 'value': 'Khammam'},
                        {'label': 'Nizamadad', 'value': 'Nizamabad'},
                        {'label': 'Warangal', 'value': 'Warangal'},
                    ],
                    value="Adilabad",
                    placeholder="Select a city",
                    style={"margin-right": "100px", "height": "45px"}
                ),

                dcc.DatePickerRange(
                    id='date_range',
                    initial_visible_month=date(2022, 9,30),
                    min_date_allowed=date(2022, 9, 30),
                    max_date_allowed=date(2023, 9, 24),
                    start_date=date(2022, 9, 30),
                    end_date=date(2023, 9, 24),
                ),
                dcc.Graph(
                    id="graph_temp",
                )
            ],

            style={
                "margin": "200px", "padding": "20px"
            }
        )
        
    ]

)


@app.callback(
    Output(component_id="adilabad_temp", component_property="children"),
     Output(component_id="karimnagar_temp", component_property="children"),
     Output(component_id="khammam_temp", component_property="children"),
     Output(component_id="nizamabad_temp", component_property="children"),
     Output(component_id="warangal_temp", component_property="children"),
     Input(component_id='date-heat', component_property='date')
)
def update_temp(date):

    out = "Temperature : "

    if(date == None):
        return out, out, out, out, out

    # yyyy-mm-dd ==> dd-mm-yyyy
    l = date.split("-")
    l.reverse()
    date = "-".join(l)

    dff = pred_heat_wave.copy()
    dff = dff.set_index("Date")
    adilabad = out + str(dff.loc[date]["Adilabad_Temp"])
    karimnagar = out + str(dff.loc[date]["Karimnagar_Temp"])
    khammam = out + str(dff.loc[date]["Khammam_Temp"])
    nizamabad = out + str(dff.loc[date]["Nizamabad_Temp"])
    warangal = out + str(dff.loc[date]["Warangal_Temp"])
    
    return adilabad, karimnagar, khammam, nizamabad, warangal

@app.callback(
    Output(component_id="graph_temp",
           component_property="figure"),
    Input(component_id='drop',
          component_property='value'),
    Input(component_id='date_range',
          component_property='start_date'),
    Input(component_id='date_range',
          component_property='end_date')
)
def update_graph(value, start, end):

    # yyyy-mm-dd ==> dd-mm-yyyy
    l = start.split("-")
    l.reverse()
    start = "-".join(l)

    # yyyy-mm-dd ==> dd-mm-yyyy
    l = end.split("-")
    l.reverse()
    end = "-".join(l)
    dff = pred_heat_wave.copy()
    dff = dff.reset_index()

    start = dff[dff["Date"] == start].index[0]
    end = dff[dff["Date"] == end].index[0]

    dff = dff.iloc[start:end+1]
    
    fig = pred_plot(dff,value)
    dff_heatwave = dff[dff[value+"_HeatWave"]==1]
    for i in dff_heatwave["Date"].values:
        fig.add_vline(x=i,
                      line_width=2, opacity=0.25, line_color="red")
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Temperature",
        font=dict(
            family="Garamond, serif",
            size=18,
        ),
        paper_bgcolor='rgb(228,235,245)',
    )

    return fig


# @app.callback(
#     Output(component_id='district_graph',
#            component_property='figure'),
#     Input(component_id='district_drp',
#           component_property='value')
# )
# def function(selection):
#     district = "None selected"
#     if selection:
#         district = selection
#     fig = func(district)
#     return fig


if __name__ == "__main__":
    app.run_server(debug=True)
