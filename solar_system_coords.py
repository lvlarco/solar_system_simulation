import plotly.graph_objects as go


class CelestialBody:
    """Initializes the body object of interest. Creates two separate plots for all the timestamps
    in position and velocity (self.plot and self.line). Position and velocity two parameters must
    be the same length.
    :param name: str
    :param position: pandas df
    :param epochs: pandas df
    :param size: int
    :param color: str
    :param scale: int
    """

    def __init__(self, name, position, epochs, size, color, scale=1):
        self.name = name
        try:
            self.pos_x = position['x']
            self.pos_y = position['y']
            self.pos_z = position['z']
            self.date = epochs
        except KeyError:
            print('Empty return from this epoch for {}'.format(name))
        self.scale = scale
        if name == 'Sun':
            ini_size = 7
        else:
            ini_size = 1
        self.size = size
        self.lsize = 3.5
        self.color = color
        self.scatter = go.Scatter3d(x=scale * self.pos_x,
                                    y=scale * self.pos_y,
                                    z=scale * self.pos_z,
                                    mode='markers',
                                    marker=dict(size=ini_size,
                                                color=self.color),
                                    name=name,
                                    hovertemplate=name)
        self.line = go.Scatter3d(x=scale * self.pos_x,
                                 y=scale * self.pos_y,
                                 z=scale * self.pos_z,
                                 mode='lines',
                                 line=dict(width=self.lsize,
                                           color=self.color),
                                 name="{}'s orbit".format(name),
                                 # hovertemplate=name
                                 )


class CoordSystem:
    """Creates a map of all bodies passed onto self.orbit_bodies. Map uses 3-axes cartesian
    coordinates.
    """

    def __init__(self, center=None):
        self.center = center
        self.orbit_bodies = []

    def add_body(self, body):
        """Updates list of celestial bodies to animate"""
        self.orbit_bodies.append(body)

    def update_frames(self, days):
        """Creates a list of scatter and line plots for each celestial body in self.orbit_bodies. Iterates
        by the number of days passed, and returns a list of go.Frame to be animated
        :param days: int
        """
        frames = []
        for i in range(days + 1):
            frame_plots = []
            for ob in self.orbit_bodies:
                sct_plot = go.Scatter3d(
                    x=[ob.scale * ob.pos_x[i]],
                    y=[ob.scale * ob.pos_y[i]],
                    z=[ob.scale * ob.pos_z[i]],
                    mode='markers',
                    marker=dict(size=ob.size))
                line_plot = go.Scatter3d(
                    x=ob.scale * ob.pos_x[:i],
                    y=ob.scale * ob.pos_y[:i],
                    z=ob.scale * ob.pos_z[:i],
                    mode='lines',
                    line=dict(width=ob.lsize))
                frame_plots = frame_plots + [sct_plot, line_plot]
                date = ob.date[i]
            frames = frames + [go.Frame(data=frame_plots, name=str(date))]
        return frames
