import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation
from bodies_info import celestial_bodies
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime, timedelta
from astropy.time import Time
from astroquery.jplhorizons import Horizons


class CelestialBody:
    def __init__(self, name, coords, size, color, scale=1):
        self.name = name
        self.coords = coords
        self.scale = scale
        self.plot = ax.scatter(self.scale * self.coords[0], self.scale * self.coords[1], self.scale * self.coords[2],
                               s=50*(size**2), color=color, zorder=10)


class CoordSystem:
    def __init__(self, center):
        self.center = center
        self.orbit_bodies = []
        self.time = None
        # self.timestamp = ax.text(.03, .94, 'Date: ', color='w', transform=ax.transAxes, fontsize='x-large')

    def add_body(self, body):
        self.orbit_bodies.append(body)

    def update_plot(self, i):  # evolve the trajectories
        dt = 1.0
        self.time += dt
        plots = []
        # lines = []
        for ob in self.orbit_bodies:
            ob.plot._offsets3d = (ob.scale * pd.Series(ob.coords[0][i]), ob.scale * pd.Series(ob.coords[1][i]),
                                  ob.scale * pd.Series(ob.coords[2][i]))
            plots.append(ob.plot)
        return plots
        #     plots.append(ob.plot)
        #     lines.append(ob.line)
        # # self.timestamp.set_text('Date: {}'.format(Time(self.time, format='jd', out_subfmt='date').iso))
        # return plots + lines  # + [self.timestamp]


day_step = 1
days_no = 365
t = datetime.now()
timestamps = [datetime.strftime(datetime.now(), '%Y-%m-%d')]
for i in range(days_no):
    t += timedelta(day_step)
    t_str = datetime.strftime(t, '%Y-%m-%d')
    timestamps.append(t_str)

timestamp_dict = {'start': datetime.strftime(datetime.now(), '%Y-%m-%d'),
                  'stop': datetime.strftime(datetime.now() + timedelta(days=days_no), '%Y-%m-%d'),
                  'step': '1d'}

plt.style.use('dark_background')
fig = plt.figure()
# ax = plt.axes()  # ([0., 0., 1., 1.], xlim=(-4, 4), ylim=(-4, 4))
# ax = fig.add_subplot(111, projection='3d')
ax = plt.axes(projection='3d')

# ax.set_aspect('equal')
# ax.axis('off')

scale = 1

center = 'Sun'
center_iau = celestial_bodies[center][1]
sizes = [0.376, 0.949, 1, 0.27, 0.533, 5.1]
colors = ['orange', 'limegreen', 'royalblue', 'whitesmoke', 'indianred', 'coral']
cs = CoordSystem(CelestialBody(center, [0, 0, 0], 10, 'yellow', scale=scale))
cs.time = Time(timestamps).jd
orbit_list = ['Mercury', 'Venus', 'Earth', 'Moon', 'Mars', 'Jupiter']
# orbit_list = ['Moon', 'Earth']
# sizes = [0.25,1.]
for cb, s, c in zip(orbit_list, sizes, colors):
    orbit_body = cb
    orbit_iau = celestial_bodies[orbit_body][0]

    coordinates = [Horizons(id=orbit_iau, location=center_iau, epochs=timestamp_dict, id_type='id').vectors()[c]
                   for c in
                   ['x', 'y', 'z']]
    cs.add_body(CelestialBody(orbit_body, coordinates, s, c))


def animate(i):
    return cs.update_plot(i)


# animate(points)
ani = animation.FuncAnimation(fig, animate, repeat=True, frames=days_no, blit=False, interval=10, )
plt.show()
