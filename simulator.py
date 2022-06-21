import pandas as pd
import plotly.graph_objects as go
from solar_system_coords import CelestialBody, CoordSystem
from bodies_info import celestial_bodies, planets_plot_settings
from astroquery.jplhorizons import Horizons
from datetime import datetime, timedelta


def define_timestamps(start, end, step=1):
    """Creates a list of timestamps from start to end at the step interval
    :param start: datetime
    :param end: datetime
    :param step: int. Defaults to 1 (day)
    :return: list
    """
    delta_time = end - start
    timestamp_list = [datetime.strftime(start, '%Y-%m-%d')]
    for i in range(delta_time.days):
        start += timedelta(step)
        t_str = datetime.strftime(start, '%Y-%m-%d')
        timestamp_list.append(t_str)
    return timestamp_list


def frame_args(duration):
    return {
        "frame": {"duration": duration},
        "mode": "immediate",
        "fromcurrent": True,
        "transition": {"duration": duration, "easing": "linear"}
    }


def run_simulation(initial_date, end_date, planets_type='terrestrial', axes=True, step=1, center='Sun'):
    total_days = end_date - initial_date
    center_iau = celestial_bodies.get(center).get('iau_code')
    planets_list = planets_plot_settings.get(planets_type).get('planets')
    # planets_list = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars']
    cs = CoordSystem(center=center)
    timestamp_dict = {'start': datetime.strftime(initial_date, '%Y-%m-%d'),
                      'stop': datetime.strftime(end_date, '%Y-%m-%d'),
                      'step': '{}d'.format(str(step))}
    df = pd.DataFrame()
    for body in planets_list:
        orbit_iau = celestial_bodies.get(body).get('id')
        size = celestial_bodies.get(body).get('size')
        color = celestial_bodies.get(body).get('color')
        data = {col: Horizons(id=orbit_iau,
                              location=center_iau,
                              epochs=timestamp_dict,
                              ).vectors()[col]
                for col in
                ['datetime_str', 'x', 'y', 'z']}
        temp_df = pd.DataFrame(data=data)
        temp_df['body'] = body
        temp_df['datetime_str'] = pd.to_datetime(temp_df['datetime_str'], format='A.D. %Y-%b-%d %H:%M:%S.0000')
        temp_df['datetime_str'] = temp_df['datetime_str'].dt.strftime('%Y/%m/%d')
        temp_df['size'] = size * 100
        temp_df['color'] = color
        position = temp_df[['x', 'y', 'z']]
        cs.add_body(CelestialBody(
            body, position, temp_df['datetime_str'],
            size, color)
        )
        df = pd.concat([df, temp_df], axis=0, ignore_index=True)
    df.rename(columns={'datetime_str': 'Date', 'body': 'Planet'}, inplace=True)
    traces = []
    for obj in cs.orbit_bodies:
        trace = [obj.scatter, obj.line]
        traces = traces + trace
    frames = cs.update_frames(total_days.days)
    layout = go.Layout(
        font=dict(color='#8B9397'),
        plot_bgcolor='yellow',
        paper_bgcolor='#222',
        width=1250,
        height=900,
        showlegend=True,
        # legend=dict(font=dict(color='white')),
        updatemenus=[
            dict(
                type='buttons',
                showactive=True,
                y=0,
                x=0.1,
                xanchor='right',
                yanchor='top',
                pad=dict(t=0, r=10),
                direction='left',
                buttons=[dict(label="&#9654;",
                              method='animate',
                              args=[None, frame_args(50)
                                    # dict(frame=
                                    # dict(duration=50,
                                    #            # redraw=False
                                    #            ),
                                    # transition=dict(duration=5,
                                    #                 # easing='quadratic-in-out'
                                    #                 ),
                                    # fromcurrent=True,
                                    # mode='immediate'
                                    # )
                                    ]
                              ),
                         dict(label="&#9724;",
                              method='animate',
                              args=[[None], frame_args(0)]
                              ),
                         ]
            )
        ],
        sliders=[
            {
                "pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], frame_args(0)],  # f.name needs to be a list
                        "label": str(f.name),
                        "method": "animate",
                    }
                    for k, f in enumerate(frames)],
            }
        ],
        # Shows axes

        # scene=dict(aspectratio=dict(x=1, y=1, z=1))
        # dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)
        #            )
    )
    fig = go.Figure(data=traces,
                    frames=frames,
                    layout=layout)
    range_val = planets_plot_settings.get(planets_type).get('axes_range')
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-range_val, range_val]),
            yaxis=dict(range=[-range_val, range_val]),
            zaxis=dict(range=[-range_val, range_val])
        ))
    # Show/Hide 3d axis
    show = axes
    fig.update_scenes(xaxis_visible=show, yaxis_visible=show, zaxis_visible=show)
    return fig

# initial_date = datetime.now() - timedelta(days=90)
# end_date = datetime.now()
# total_days = end_date - initial_date
# step = 1
# figure = run_simulation(initial_date, end_date, 'terrestrial', step)
# figure.show()
