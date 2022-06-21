import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State

import simulator as sim
import dash_bootstrap_components as dbc
import dash_daq as daq
from datetime import datetime, timedelta

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = 'Solar System Simulator'

app.layout = html.Div(
    id='app-container',
    style={'padding': '3rem 16rem 8rem 16rem'},
    children=[
        html.Div([
            html.H1(
                id='header-title',
                children='Solar System Simulator'
            ),
            html.P([
                "Welcome! This simulator allows modeling of every planet of our Solar System. It uses JPL's "
                "Horizons API to locate every celestial body with respect to another at any given time in space. "
                "The app defaults the Sun as the center of the simulation, but you will be able to select other "
                "'centers' in future iterations.",
                html.Br(),
                "Units are in AU and the planet sizes are not to scale."
            ]),
            html.H4('Instructions: ', className='list-group'

                    ),
            html.Ol([
                html.Li("Select between Terrestrial or Jovian planets. Note: Jovian planets (Jupiter, Saturn, Uranus, "
                        "Neptune) "
                        "are significantly farther away from the Sun, thus selecting 'All' might distort the plot"),
                html.Li('Pick a date range. The simulation will individually parse every date as a 3-ax '
                        'cartesian plot'),
                html.Li('Use Play/Stop buttons to animate the simulation. You can only start the animation from '
                        'the beginning of the date range'),
                html.Li('Simulation is built using Plotly, and it is highly interactive. However, you cannot '
                        'interact with it once animation starts. Set up view before starting it'),
                html.Li('You can toggle the background, and use the slider to stop at a specific date')
            ])
        ],
            style={
                "margin-bottom": "70px",
            }
        ),
        html.Div(
            [
                dbc.Col(
                    dbc.RadioItems(
                        id="planets-radio",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Terrestrial (Mercury, Venus, Earth & Mars)", "value": 1},
                            {"label": "Jovian (Jupiter, Saturn, Uranus, Neptune)", "value": 2},
                            {"label": "All", "value": 3},
                        ],
                        value=1,
                    ),
                    width=dict(size=8, offset=2)
                ),
            ],
            className="radio-group",
            style={
                "margin-bottom": "10px",
            }
        ),
        dbc.Row([
            dbc.Col(
                dcc.DatePickerRange(id="date-range",
                                    display_format='YYYY/MM/DD',
                                    calendar_orientation='horizontal',
                                    min_date_allowed='2010-01-01',
                                    max_date_allowed='2029-12-31',
                                    start_date=datetime.today().strftime('%Y-%m-%d'),
                                    end_date=(datetime.today() + timedelta(days=365)).strftime('%Y-%m-%d')),
                width=dict(size=3, offset=3),
                align='center'
            ),
            dbc.Col(
                dbc.Button('Search',
                           id='button-search',
                           # className='btn btn-outline-dark',
                           color='primary',
                           n_clicks=0)
                ,
                width=dict(size=1, offset=0),
                align='center'
            )
        ], style={
            "margin-bottom": "50px",
        }
        ),
        html.Div([
            dbc.Col(daq.BooleanSwitch(
                id='axes-switch',
                on=True,
                label="Turn on/off background",
                labelPosition="right",
                color='rgb(55, 90, 127)'
            ),
                width=dict(size=2, offset=2)),
            html.Center(
                dcc.Loading(
                    id='loading-plot',
                    children=dcc.Graph(
                        id='simulation-plot')))
        ], style={
            "margin-bottom": "40px",
        }
        ),
        html.Center([
            html.H6(['Created by ',
                     html.A('me', href='https://lvlarco.github.io/', target='_blank'),
                     html.Br(),
                     'If you find this useful help me pay for the server and ',
                     dcc.Link('buy me a coffee', href='https://www.buymeacoffee.com/lvlarco', target='_blank')],
                    style={
                        'color': 'rgba(255, 255, 255, 0.5)',
                        'font-size': '0.75em'
                    }
                    ),
        ],
            id='credits',

        )
    ]
)


@app.callback(
    Output(component_id='simulation-plot', component_property='figure'),
    Input(component_id='button-search', component_property='n_clicks'),
    Input(component_id='axes-switch', component_property='on'),
    State(component_id='planets-radio', component_property='value'),
    State(component_id='date-range', component_property='start_date'),
    State(component_id='date-range', component_property='end_date')
)
def update_simulation(_, axes, radio_value, start_date, end_date):
    if radio_value == 2:
        planets = 'jovian'
    elif radio_value == 3:
        planets = 'all'
    else:
        planets = 'terrestrial'
    if isinstance(start_date, str) and isinstance(end_date, str):
        start_date = start_date[:18]
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = end_date[:18]
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    return sim.run_simulation(start_date, end_date, planets, axes)


if __name__ == '__main__':
    app.run_server(debug=True)
