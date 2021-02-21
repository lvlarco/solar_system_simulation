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
    def __init__(self, name, position, velocity, size, color, scale=1):
        self.name = name
        self.pos = position
        self.vel = velocity
        self.scale = scale
        self.plot = ax.scatter(self.scale * self.pos[0], self.scale * self.pos[1], self.scale * self.pos[2],
                               s=100 * size, color=color)  # , zorder=10)
        self.line, = ax.plot(self.scale * self.pos[0], self.scale * self.pos[1], self.scale * self.pos[2], color=color,
                             linestyle="-", linewidth=2)
        # self.line, = ax.plot([],[],[], color=color,
        #                      linestyle="-", linewidth=4, zorder=10)


class CoordSystem:
    def __init__(self, center):
        self.center = center
        self.orbit_bodies = []
        self.time = None
        # self.timestamp = ax.text(.03, .94, 'Date: ', color='w', transform=ax.transAxes, fontsize='x-large')

    def add_body(self, body):
        self.orbit_bodies.append(body)

    def update_plot(self, i):  # evolve the trajectories
        plots = []
        
        lines = []
        for ob in self.orbit_bodies:
            ob.plot._offsets3d = (ob.scale * pd.Series(ob.pos[0][i]), ob.scale * pd.Series(ob.pos[1][i]),
                                  ob.scale * pd.Series(ob.pos[2][i]))
            plots.append(ob.plot)
            # ob.line.set_data(ob.scale * pd.Series(ob.vel[0][i]), ob.scale * pd.Series(ob.vel[1][i]))
            # ob.line.set_3d_properties(ob.scale * pd.Series(ob.vel[2][i]))
            ob.line.set_data(np.array([pd.Series(ob.pos[0][:i]), pd.Series(ob.pos[1][:i])]))
            ob.line.set_3d_properties(ob.scale * pd.Series(ob.pos[2][:i]))
            lines.append(ob.line)
        return plots + lines
        #     plots.append(ob.plot)
        #     lines.append(ob.line)
        # # self.timestamp.set_text('Date: {}'.format(Time(self.time, format='jd', out_subfmt='date').iso))
        # return plots + lines  # + [self.timestamp]


day_step = 1
days_no = 365
t = datetime.now()

timestamp_dict = {'start': datetime.strftime(t, '%Y-%m-%d'),
                  'stop': datetime.strftime(t + timedelta(days=days_no), '%Y-%m-%d'),
                  'step': '1d'}

timestamps = [datetime.strftime(t, '%Y-%m-%d')]
for i in range(days_no):
    t += timedelta(day_step)
    t_str = datetime.strftime(t, '%Y-%m-%d')
    timestamps.append(t_str)

plt.style.use('dark_background')
fig = plt.figure()
# ax = plt.axes()  # ([0., 0., 1., 1.], xlim=(-4, 4), ylim=(-4, 4))
# ax = fig.add_subplot(111, projection='3d')
ax = plt.axes(projection='3d')
# ax = Axes3D(fig)

# ax.set_aspect('equal')
ax.axis('off')

scale = 1

center = 'Sun'
center_iau = celestial_bodies[center][1]
sizes = [5, 0.27, 0.376, 0.949, 1, 0.533, 3]
orbit_list = ['Sun', 'Moon', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter']
# orbit_list = ['Sun']  # 'Earth', 'Moon', 'Mercury']
# sizes = [1]  # ,1, 0.27, 0.5]
colors = ['yellow', 'whitesmoke', 'orange', 'limegreen', 'royalblue', 'indianred', 'coral']
# c_coords = Horizons(id=celestial_bodies['Sun'][0], location=center_iau, epochs=timestamp_dict, id_type='id').vectors()
# cs = CoordSystem(CelestialBody(center, [0, 0, 0], 1, 'yellow', scale=scale))
cs = CoordSystem(center='Solar System')

cs.time = Time(timestamps).jd
coord_array = np.empty((0, days_no + 1), float)
for cb, s, c in zip(orbit_list, sizes, colors):
    orbit_body = cb
    orbit_iau = celestial_bodies[orbit_body][0]
    coords = [Horizons(id=orbit_iau, location=center_iau, epochs=timestamp_dict, id_type='id').vectors()[c]
              for c in
              ['x', 'y', 'z', 'vx', 'vy', 'vz']]
    pos_coord = coords[:3]
    vel_coord = coords[3:]
    cs.add_body(CelestialBody(orbit_body, pos_coord, vel_coord, s, c))


def animate(i):
    return cs.update_plot(i)


# cs.update_plot(30)
ani = animation.FuncAnimation(fig, animate, repeat=True, frames=days_no, blit=False, interval=100)
# http://matplotlib.sourceforge.net/api/animation_api.html
s = ani.to_jshtml()
with open('ss_simulation.html', "w") as f:
    f.write(s)
# ani.save('ss_simulation.html')#, fps=30, extra_args=['-vcodec', 'libx264'])
# ani.to_jshtml()
# plt.show()
