import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

#?map
import os
import plotly.graph_objs as go
from dash.dependencies import Input, Output


#data preprocessing
data = pd.read_csv("DOHMH_New_York_City_Restaurant_Inspection_Results.csv")
x_1 = ["A", "B", "C", "Not Yet Graded", "Grade Pending"]
x_2 = ["Manhattan", "Bronx", "Brooklyn", "Queens", "Staten Island"]

y_1 = data.groupby(['BORO', 'GRADE']).size()






#visualization
app = dash.Dash()
app.title = 'Visualization'

app.layout = html.Div([
                #barchart
                dcc.Graph(
                    id='inspection_grade',
                    figure={
                        
                        'data': [
                            {'x': x_1, 'y': y_1.Manhattan, 'type': 'bar', 'name': 'Manhattan'},
                            {'x': x_1, 'y': y_1.Brooklyn, 'type': 'bar', 'name': 'Brooklyn'},    
                            {'x': x_1, 'y': y_1.Queens, 'type': 'bar', 'name': 'Queens'},
                            {'x': x_1, 'y': y_1.Bronx, 'type': 'bar', 'name': 'Bronx'},                                       
                            {'x': x_1, 'y': y_1["Staten Island"], 'type': 'bar', 'name': 'Staten Island'},

                        ],
                        'layout': {
                            'title': 'Inspection Grade by Borough',
                            'xaxis' : dict(
                                title='Borough',
                                titlefont=dict(
                                family='Courier New, monospace',
                                size=20,
                                color='#7f7f7f'
                            )),
                            'yaxis' : dict(
                                title='# of restaurants',
                                titlefont=dict(
                                family='Helvetica, monospace',
                                size=20,
                                color='#7f7f7f'
                            ))
                        }
                    }
                ),
                #100% Stacked barchart
                dcc.Graph(
                    id='stacked bar',
                    figure={
                        
                        'data': [
                            {'x': x_2, 'y': [len(data[(data.BORO == "Manhattan") & (data.GRADE == 'A')])/len(data[(data.BORO == "Manhattan") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Bronx") & (data.GRADE == 'A')])/len(data[(data.BORO == "Bronx") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Brooklyn") & (data.GRADE == 'A')])/len(data[(data.BORO == "Brooklyn") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Queens") & (data.GRADE == 'A')])/len(data[(data.BORO == "Queens") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Staten Island") & (data.GRADE == 'A')])/len(data[(data.BORO == "Staten Island") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                                ], 'type': 'bar', 'name': 'A'},
                                                
                            {'x': x_2, 'y': [len(data[(data.BORO == "Manhattan") & (data.GRADE == 'B')])/len(data[(data.BORO == "Manhattan") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Bronx") & (data.GRADE == 'B')])/len(data[(data.BORO == "Bronx") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Brooklyn") & (data.GRADE == 'B')])/len(data[(data.BORO == "Brooklyn") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Queens") & (data.GRADE == 'B')])/len(data[(data.BORO == "Queens") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Staten Island") & (data.GRADE == 'B')])/len(data[(data.BORO == "Staten Island") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                                ], 'type': 'bar', 'name': 'B'},
                            {'x': x_2, 'y': [len(data[(data.BORO == "Manhattan") & (data.GRADE == 'C')])/len(data[(data.BORO == "Manhattan") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Bronx") & (data.GRADE == 'C')])/len(data[(data.BORO == "Bronx") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Brooklyn") & (data.GRADE == 'C')])/len(data[(data.BORO == "Brooklyn") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Queens") & (data.GRADE == 'C')])/len(data[(data.BORO == "Queens") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                             len(data[(data.BORO == "Staten Island") & (data.GRADE == 'C')])/len(data[(data.BORO == "Staten Island") & ((data.GRADE == 'A') | (data.GRADE == 'B') | (data.GRADE == 'C'))]),
                                                ], 'type': 'bar', 'name': 'C'},
                        ],
                        'layout': {
                            'title': 'Inspection Grade by Borough',
                            'xaxis' : dict(
                                title='Borough',
                                titlefont=dict(
                                family='Courier New, monospace',
                                size=20,
                                color='#7f7f7f'
                            )),
                            'yaxis' : dict(
                                title='# of restaurants',
                                titlefont=dict(
                                family='Helvetica, monospace',
                                size=20,
                                color='#7f7f7f'
                            )),
                            'barmode' : 'stack'
                        }
                    }
                ),
                
                ]
                )
                              
            
if __name__ == '__main__':
    app.run_server(debug=True)