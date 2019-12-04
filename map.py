import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_caching import Cache
from csv import DictReader
from toolz import compose, pluck, groupby, valmap, first, unique, get, countby
import datetime as dt
import os

import pandas as pd


################################################################################
# HELPERS
################################################################################
listpluck = compose(list, pluck)
listfilter = compose(list, filter)
listmap = compose(list, map)
listunique = compose(list, unique)

TIMESTAMP_FORMAT = "%m/%d/%Y"
'''
# Datetime helpers.
def sighting_year(sighting):
    return dt.datetime.strptime(sighting['INSPECTION DATE'], TIMESTAMP_FORMAT).year

def sighting_dow(sighting):
    return dt.datetime.strptime(sighting['timestamp'], TIMESTAMP_FORMAT)\
                      .strftime("%a")
'''

################################################################################
# DATA
################################################################################
# Read the data.
'''
fin = open('DOHMH_New_York_City_Restaurant_Inspection_Results.csv', 'r', encoding = 'UTF8')
reader = DictReader(fin)
RESTAURANT_DATA = [
                    line for line in reader 
                    if (sighting_year(line) <= 2019) and (sighting_year(line) >= 2019)
                  ]
fin.close()
'''

data = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
data['INSPECTION DATE'] = pd.to_datetime(data['INSPECTION DATE'])
temp = data.groupby('DBA').apply(lambda x: x.sort_values(['INSPECTION DATE'],ascending=False).head(1))
RESTAURANT_DATA = temp.T.to_dict().values()


################################################################################
# PLOTS
################################################################################
def bigfoot_map(sightings):
    classifications = groupby('GRADE', sightings)
    return {
        "data": [
                {
                    "type": "scattermapbox",
                    "lat": listpluck("Latitude", class_sightings),
                    "lon": listpluck("Longitude", class_sightings),
                    "text": listpluck("DBA", class_sightings),
                    "mode": "markers",
                    "name": classification,
                    "marker": {
                        "size": 5,
                        "opacity": 1.0
                    }
                }
                for classification, class_sightings in classifications.items()
            ],
        "layout": {
            "autosize": True,
            "hovermode": "closest",
            "mapbox": {
                "accesstoken": "pk.eyJ1IjoiZmllcmZlayIsImEiOiJjazNudjFteHIwYmZpM21xbnJ4MHY0YmlnIn0.T6k_p6zQAkjtpFEf58iyog",
                "bearing": 0,
                "center": {
                    "lat": 40.70,
                    "lon": -73.95
                },
                "pitch": 0,
                "zoom": 9,
                "style": "outdoors"
            }
        }
    }
'''
def bigfoot_by_year(sightings):
    # Create a dict mapping the 
    # classification -> [(year, count), (year, count) ... ]
    sightings_by_year = {
        classification: 
            sorted(
                list(
                    # Group by year -> count.
                    countby(sighting_year, class_sightings).items()
                ),
                # Sort by year.
                key=first
            )
        for classification, class_sightings 
        in groupby('classification', sightings).items()
    }

    # Build the plot with a dictionary.
    return {
        "data": [
            {
                "type": "scatter",
                "mode": "lines+markers",
                "name": classification,
                "x": listpluck(0, class_sightings_by_year),
                "y": listpluck(1, class_sightings_by_year)
            }
            for classification, class_sightings_by_year 
            in sightings_by_year.items()
        ],
        "layout": {
            "title": "Sightings by Year",
            "showlegend": False
        }
    }

def bigfoot_dow(sightings):
    
    # Produces a dict (year, dow) => count.
    sightings_dow = countby("dow",
        [
            {
                "dow": sighting_dow(sighting)
            } 
            for sighting in sightings
        ]
    )

    dows =  ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    return {
        "data": [
            {
                "type": "bar",
                "x": dows,
                "y": [get(d, sightings_dow, 0) for d in dows]
            }
        ],
        "layout": {
            "title": "Sightings by Day of Week",
        }
    }

def bigfoot_class(sightings):
    sightings_by_class = countby("classification", sightings)

    return {
        "data": [
            {
                "type": "pie",
                "labels": list(sightings_by_class.keys()),
                "values": list(sightings_by_class.values()),
                "hole": 0.4
            }
        ],
        "layout": {
            "title": "Sightings by Class"
        }
    }
'''
################################################################################
# APP INITIALIZATION
################################################################################


app = dash.Dash()
# For Heroku deployment.
server = app.server

app.title = "New York City Restaurant Inspection"
cache = Cache(app.server, config={"CACHE_TYPE": "simple"})


# This function can be memoized because it's called for each graph, so it will
# only get called once per filter text.
@cache.memoize(10)
def filter_sightings(filter_text):
    return listfilter(
            lambda x: filter_text.lower() in x['BORO'].lower(),
            RESTAURANT_DATA
        )

################################################################################
# LAYOUT
################################################################################
app.layout = html.Div([
    # Row: Title
    html.Div([
        # Column: Title
        html.Div([
            html.H1("New York City Restaurant Inspection", className="text-center")
        ], className="col-md-12")
    ], className="row"),
    # Row: Filter + References
    html.Div([
        # Column: Filter
        html.Div([
            html.P([
                html.B("Filter the borough:  "),
                dcc.Input(
                    placeholder="Try 'heard'",
                    id="bigfoot-text-filter",
                    value="")
            ]),
        ], className="col-md-6"),
    ], className="row"),
    # Row: Map + Bar Chart
    html.Div([
        # Column: Map
        html.Div([
            dcc.Graph(id="bigfoot-map")
        ], className="col-md-8"),
        # Column: Bar Chart
        html.Div([
            dcc.Graph(id="bigfoot-dow")
        ], className="col-md-4")
    ], className="row"),
    # Row: Line Chart + Donut Chart
    html.Div([
        # Column: Line Chart
        html.Div([
            dcc.Graph(id="bigfoot-by-year")
        ], className="col-md-8"),
        # Column: Donut Chart
        html.Div([
            dcc.Graph(id="bigfoot-class")
        ], className="col-md-4")
    ], className="row"),
    # Row: Footer
    html.Div([
        html.Hr(),
        html.P([
            "Built with ",
            html.A("Dash", href="https://plot.ly/products/dash/"),
            ". Check out the code on ",
            html.A("GitHub", href="https://github.com/timothyrenner/bigfoot-dash-app"),
            "."
        ])      
    ], className="row",
        style={
            "textAlign": "center",
            "color": "Gray"
        })
], className="container-fluid")

################################################################################
# INTERACTION CALLBACKS
################################################################################
@app.callback(
    Output('bigfoot-map', 'figure'),
    [
        Input('bigfoot-text-filter', 'value')
    ]
)
def filter_bigfoot_map(filter_text):
    return bigfoot_map(filter_sightings(filter_text))
    
    
'''   
@app.callback(
    Output('bigfoot-by-year', 'figure'),
    [
        Input('bigfoot-text-filter', 'value')
    ]
)
def filter_bigfoot_by_year(filter_text):
    return bigfoot_by_year(filter_sightings(filter_text))

@app.callback(
    Output('bigfoot-dow', 'figure'),
    [
        Input('bigfoot-text-filter', 'value')
    ]
)
def filter_bigfoot_dow(filter_text):
    return bigfoot_dow(filter_sightings(filter_text))

@app.callback(
    Output('bigfoot-class', 'figure'),
    [
        Input('bigfoot-text-filter', 'value')
    ]
)
def filter_bigfoot_class(filter_text):
    return bigfoot_class(filter_sightings(filter_text))
'''
if __name__ == "__main__":
    app.run_server(debug=True)