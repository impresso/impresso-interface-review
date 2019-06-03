"""
Small piece of code for creating radar charts.
Credits: from https://matplotlib.org/examples/api/radar_chart.html
"""

__author__ = "maudehrmann"

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import numpy as np


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):
        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels, fontsize):
            self.set_thetagrids(np.degrees(theta), labels, fontsize=fontsize)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def build_single_radar(labels, values, title, grid, figure_title):
    N = len(labels)
    theta = radar_factory(N, frame='polygon')

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)

    ax.set_rgrids(grid, labels=[str(i) for i in grid], size='large')
    ax.set_title(title, position=(0.5, 1.1), ha='center')

    for d in values:
        ax.plot(theta, d)
        ax.fill(theta, d, alpha=0.25)
    ax.set_varlabels(labels, fontsize=12)

    if figure_title is None:
        plt.show()
    else:
        plt.savefig(f'../charts/{figure_title}.pdf', format='pdf', quality=95)


def build_single_radar_free(labels, values, title, figure_title):
    N = len(labels)
    theta = radar_factory(N, frame='circle')
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)
    ax.set_title(title, position=(0.5, 1.1), ha='center')

    for d in values:
        ax.plot(theta, d)
        ax.fill(theta, d, alpha=0.25)
    ax.set_varlabels(labels, fontsize=12)

    if figure_title is None:
        plt.show()
    else:
        plt.savefig(f'../charts/{figure_title}.pdf', format='pdf', quality=95)


def build_multiple_radar(labels, values, titles, figure_title):
    N = len(labels)
    theta = radar_factory(N, frame='polygon')
    fig, axes = plt.subplots(figsize=(120, 80), nrows=4, ncols=6,
                             subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.50, hspace=0.20, top=0.85, bottom=0.05)
    for ax, case_data, title in zip(axes.flatten(), values, titles):
        ax.set_ylim(0, 30)
        ax.set_title(title, weight='bold', fontsize=42, position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        ax.plot(theta, case_data)
        ax.fill(theta, case_data, alpha=0.25)
        ax.set_varlabels(labels, fontsize=32)

    if figure_title is None:
        plt.show()
    else:
        plt.savefig(f'../charts/{figure_title}.pdf', format='pdf', quality=95)