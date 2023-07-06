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

app.layout = dbc.Container(
    id='app-container',
    style={'padding': '3vh 8vh 8vh 8vh'},
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
                html.Li(
                    "Choose either Terrestrial or Jovian planets"
                ),
                html.Li(
                    "Select a date range, and the simulation will plot each date as a three-axis Cartesian plot"
                ),
                html.Li(
                    "Use the Play/Stop buttons to animate the simulation, starting only from the beginning "
                    "of the date range"
                ),
                html.Li(
                    "The simulation is interactive but becomes non-interactive once the animation begins, "
                    "so set up your desired view beforehand"
                ),
                html.Li(
                    "Toggle the background and use the slider to pause the animation at a specific date"
                )
            ])
        ],
            style={
                "margin-bottom": "70px",
            }
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            html.H5("Select a group of planets"),
                            style={"margin-left": "20px"}
                        ),
                        dbc.RadioItems(
                            id="planets-radio",
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": "Terrestrial (Mercury, Venus, Earth & Mars)", "value": 1},
                                {"label": "Jovian (Jupiter, Saturn, Uranus, Neptune)", "value": 2},
                                # {"label": "All", "value": 3},
                            ],
                            value=1,
                        )
                    ],
                    width=dict(size="auto", order="first")
                ),
                dbc.Col(
                    [
                        html.Div(html.H5("Pick a date range")),
                        dcc.DatePickerRange(
                            id="date-range",
                            display_format='YYYY/MM/DD',
                            calendar_orientation='horizontal',
                            min_date_allowed='2010-01-01',
                            max_date_allowed='2029-12-31',
                            start_date=datetime.today().strftime('%Y-%m-%d'),
                            end_date=(datetime.today() + timedelta(days=365)).strftime('%Y-%m-%d')
                        ),
                    ],
                    width=dict(size="auto", order="last")
                ),

            ],
            className="p-0"
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button('Run simulation',
                           id='button-search',
                           color='info',
                           n_clicks=0
                           ),
                width=dict(size="auto", order="last"),
            ),
            className="p-4"
        ),
        dbc.Row(
            [
                dbc.Col(
                    daq.BooleanSwitch(
                        id='axes-switch',
                        on=True,
                        label="Turn on/off background",
                        labelPosition="right",
                        color='rgb(55, 90, 127)',
                    ),
                    width="auto",
                    className="px-5"
                ),
                dbc.Col(
                    dcc.Loading(
                        id='loading-plot',
                        children=dcc.Graph(
                            id='simulation-plot',
                            style={'height': '90vh'},
                        ),
                    ),
                    width=12
                )
            ],
        ),
    ]
)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <script src="https://kit.fontawesome.com/bec780fc18.js" crossorigin="anonymous"></script>
        {%metas%}
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div id="content-wrapper">
            {%app_entry%}
        </div>
        <footer>
            <div id="button-wrapper">
                <div id="icons">
                    <a href="https://github.com/lvlarco/solar_system_simulation" target="_blank" class="fa-brands fa-github"></a>
                    <a href="https://lvlarco.github.io/contact" target="_blank" class="fa-solid fa-envelope"></a>
                </div>
                <script type="text/javascript"src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" id="bmc-btn" data-name="bmc-button" data-slug="lvlarco" data-color="#FFDD00" data-emoji="" data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff"></script>
            </div>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <style>
            html, body {
                height: 100%;
                margin: 0;
                padding: 0;
            }
            #content-wrapper {
                min-height: calc(100% - 50px);
                padding-bottom: 50px;
            }
            #button-wrapper {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: #f8f8f8;
                padding: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            #icons {
                display: flex;
                align-items: center
            }
            #icons a.fa-github:before,
            #icons a.fa-envelope:before {
                color: rgb(55,90,127);
                font-size: 200%;
                margin-left: 30px;
                text-decoration: none;
            }
            a.bmc-btn:hover {
                color: rgb(55,90,127);
            }
        </style>
    </body>
</html>
'''


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
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    return sim.run_simulation(start_date, end_date, planets, axes)


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=False)
    # app.run_server(debug=True)
