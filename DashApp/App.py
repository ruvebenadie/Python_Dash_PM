# import libraries
import pandas as pd
import numpy as np
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input

# read file and set year column to date showing only year
df = pd.read_csv('C:/Users/ruveb/Desktop/pm (1).csv')
df.year = pd.to_datetime(df.year, format='%Y').dt.year

# link CSS
external_stylesheets = [
    {
        "href": "/assets"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
# create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Annual Mean Levels of Fine Particulate Matter in Urban Areas"

# set layout
app.layout = html.Div(
    children=[
        html.Div(
            children=[

                html.H1(
                    children="Annual Mean Levels of Fine Particulate Matter in Urban Areas in South Africa",
                    className="header-title"
                ),
                html.P(
                    children="Airborne particulate matter (PM) is not a single pollutant, but rather a mixture of "
                             "many chemical species. "
                             "It is a complex mixture of solids and aerosols composed of small droplets of liquid, "
                             "dry solid fragments, and solid cores with liquid coatings. "
                             "Particles vary widely in size, shape and chemical composition, and may contain "
                             "inorganic ions, metallic compounds, elemental carbon, organic compounds, and compounds "
                             "from the earth’s crust. "
                             " Particles are defined by their diameter for air quality regulatory purposes. "
                             "Those with a diameter of 10 microns or less (PM10) are inhalable and can "
                             "induce adverse health effects. "
                             "Fine particulate matter is defined as particles that are 2.5 microns or less in "
                             "diameter (PM2.5). "
                             " Therefore, PM2.5 comprises a portion of PM10."
                             " Adverse effects include: increased rates of chronic bronchitis, reduced lung function "
                             "and increased mortality from lung cancer and heart disease. "
                             "People with breathing and heart problems, children and the elderly may be particularly "
                             "sensitive to PM2.5. Save levels of PM2.5 are considered to be 12μg/m3 or less and 20μg/m3 or less for PM10."
                    ,
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Pick a City", className="menu-title"),
                        dcc.Dropdown(
                            id="city-filter",
                            options=[
                                {"label": city, "value": city}
                                for city in np.sort(df.city.unique())
                            ],
                            value="City Of Tshwane",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),

            ],

        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="pm25-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="pm10-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),

            ],
            className="wrapper",
        ),
        html.Div([
            html.H1('PM2.5 Heatmap (latest year available)', style={
                'text-align': 'center',
                'font-size': '18px'
            }),
            html.P('PM2.5 has the greatest affect on humans, especially infants and the elderly.'
                   ' PM2.5 are more dangerous because they can get into the deep parts of your lungs — or even into '
                   'your blood.', style={
                'text-align': 'center'
            }),
            html.Iframe(
                id='map',
                srcDoc=open('output.html', 'r').read(),
                title="PM2.5 For Latest Year",
                width='100%',
                height='600'

            )

        ]),

    ])


# interactivity
@app.callback(
    [Output(component_id="pm25-chart", component_property="figure"),
     Output(component_id="pm10-chart", component_property="figure")],
    [
        Input("city-filter", "value"),

    ],
)
def update_charts(city):
    mask = (
        (df.city == city)

    )
    filtered_data = df.loc[mask, :]
    pm25_chart_figure = {
        "data": [
            {
                "x": filtered_data["year"],
                "y": filtered_data["PM2.5 (μg/m3)"],
                "type": "lines",

            },
        ],
        "layout": {
            "title": {
                "text": "PM2.5 (μg/m3)",

            },
            "yaxis": {'range': [0, 130], "dtick": 10},
            "colorway": ["#17B897"],

        },
    }

    pm10_chart_figure = {
        "data": [
            {
                "x": filtered_data["year"],
                "y": filtered_data["PM10 (μg/m3)"],
                "type": "lines",

            },
        ],
        "layout": {
            "title": {
                "text": "PM10 (μg/m3)",

            },
            "yaxis": {'range': [0, 130], "dtick": 10},
            "colorway": ["#17B897"],

        },
    }
    return pm25_chart_figure, pm10_chart_figure

# deploy app
if __name__ == "__main__":
    app.run_server(debug=True)
