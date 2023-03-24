import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SliderBase,Slider, Button, RadioButtons
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Rectangle, Ellipse, Polygon
from matplotlib.transforms import TransformedPatchPath, Affine2D
import matplotlib as mpl

class RangeSlider(SliderBase):
    def __init__(
        self,
        ax,
        label,
        valmin,
        valmax,
        valinit=None,
        valfmt=None,
        closedmin=True,
        closedmax=True,
        dragging=True,
        valstep=None,
        orientation="horizontal",
        handle_style=None,
        color_left='green',
        color_middle='red',
        color_right='blue'
    ):
        super().__init__(ax, orientation, closedmin, closedmax,
                         valmin, valmax, valfmt, dragging, valstep)
        self.color_middle=color_middle
        # Set a value to allow _value_in_bounds() to work.
        self.val = (valmin, valmax)
        if valinit is None:
            # Place at the 25th and 75th percentiles
            extent = valmax - valmin
            valinit = np.array([valmin + extent * 0.25,
                                valmin + extent * 0.75])
        else:
            valinit = self._value_in_bounds(valinit)
        self.middle=0.7
        self.val = valinit
        self.valinit = valinit
        defaults = {'facecolor': 'white', 'edgecolor': '.75', 'size': 10}
        self.handle_st1={'facecolor':color_left,'size':53,'edgecolor':'1'}
        self.marker_props1 = {
            f'marker{k}': v for k, v in {**defaults, **self.handle_st1}.items()
        }
        self.handle_st2={'facecolor':color_right,'size':53,'edgecolor':'1'}
        self.marker_props2 = {
            f'marker{k}': v for k, v in {**defaults, **self.handle_st2}.items()
        }

        
        self.track = Rectangle(
            (0, .25), self.middle, .5,
            transform=ax.transAxes,
            facecolor=color_left
        )
        ax.add_patch(self.track)
        self.track = Rectangle(
            (self.middle, .25), 1-self.middle, .5,
            transform=ax.transAxes,
            facecolor=color_right
        )
        ax.add_patch(self.track)
        self.poly_transform = self.ax.get_xaxis_transform(which="grid")
        self.handleXY_1 = [valinit[0], .5]
        self.handleXY_2 = [valinit[1], .5]
        self.poly = Polygon(np.zeros([5, 2]), **{'color': self.color_middle})
        self._update_selection_poly(*valinit)
        self.poly.set_transform(self.poly_transform)
        self.poly.get_path()._interpolation_steps = 100
        self.ax.add_patch(self.poly)
        self.ax._request_autoscale_view()
        self._handles = [
            ax.plot(
                *self.handleXY_1,
                "s",
                **self.marker_props1,
                clip_on=False
            )[0],
            ax.plot(
                *self.handleXY_2,
                "s",
                **self.marker_props2,
                clip_on=False
            )[0]
        ]
        self.valtext = ax.text(
            1.02,
            0.5,
            self._format(valinit),
            transform=ax.transAxes,
            verticalalignment="center",
            horizontalalignment="left",
        )
        self._active_handle = None
        self.set_val(valinit)
    def _update_selection_poly(self, vmin, vmax):

        verts = self.poly.xy
        if self.orientation == "vertical":
            verts[0] = verts[4] = .25, vmin
            verts[1] = .25, vmax
            verts[2] = .75, vmax
            verts[3] = .75, vmin
        else:
            verts[0] = verts[4] = vmin, .25
            verts[1] = vmin, .75
            verts[2] = vmax, .75
            verts[3] = vmax, .25
    def _min_in_bounds(self, min):
        """Ensure the new min value is between valmin and self.val[1]."""
        if min <= self.valmin:
            if not self.closedmin:
                return self.val[0]
            min = self.valmin

        if min > self.val[1]:
            min = self.val[1]
        return self._stepped_value(min)
    def _max_in_bounds(self, max):
        """Ensure the new max value is between valmax and self.val[0]."""
        if max >= self.valmax:
            if not self.closedmax:
                return self.val[1]
            max = self.valmax

        if max <= self.val[0]:
            max = self.val[0]
        return self._stepped_value(max)
    def _value_in_bounds(self, vals):
        """Clip min, max values to the bounds."""
        return (self._min_in_bounds(vals[0]), self._max_in_bounds(vals[1]))
    def _update_val_from_pos(self, pos,handle_index):
        """Update the slider value based on a given position."""
        idx = np.argmin(np.abs(self.val - pos))
        if idx == 0:
            val = self._min_in_bounds(pos)
            self.set_min(val)
        else:
            val = self._max_in_bounds(pos)
            self.set_max(val)
        if self._active_handle:
            if self.orientation == "vertical":
                self._active_handle.set_ydata([val])
            else:
                self._active_handle.set_xdata([val])
    def rectangle_update(self):
        middle=(self._handles[0].get_xdata()[0]+self._handles[1].get_xdata()[0])/200
        self.track = Rectangle(
            (0, .25), middle, .5,
            transform=self.ax.transAxes,
            facecolor=color_left
        )
        self.ax.add_patch(self.track)
        self.track = Rectangle(
            (middle, .25), 1-middle, .5,
            transform=self.ax.transAxes,
            facecolor=color_right
        )
        self.ax.add_patch(self.track)
        self.poly_transform = self.ax.get_xaxis_transform(which="grid")
        self._update_selection_poly(*valinit)
        self.poly.set_transform(self.poly_transform)
        self.poly.get_path()._interpolation_steps = 100
        self.ax.add_patch(self.poly)
    def _update(self, event):
        """Update the slider position."""
        if self.ignore(event) or event.button != 1:
            return
        if event.name == "button_press_event" and event.inaxes == self.ax:
            self.drag_active = True
            event.canvas.grab_mouse(self.ax)
            self.rectangle_update()
        if not self.drag_active:
            return
        elif (event.name == "button_release_event") or (
            event.name == "button_press_event" and event.inaxes != self.ax
        ): 
            self.drag_active = False
            event.canvas.release_mouse(self.ax)
            self._active_handle = None
            return
        # determine which handle was grabbed
        if self.orientation == "vertical":
            handle_index = np.argmin(
                np.abs([h.get_ydata()[0] - event.ydata for h in self._handles])
            )
        else:
            handle_index = np.argmin(
                np.abs([h.get_xdata()[0] - event.xdata for h in self._handles])
            )
        handle = self._handles[handle_index]
        # these checks ensure smooth behavior if the handles swap which one
        # has a higher value. i.e. if one is dragged over and past the other.
        if handle is not self._active_handle:
            self._active_handle = handle

        if self.orientation == "vertical":
            self._update_val_from_pos(event.ydata)
        else:
            self._update_val_from_pos(event.xdata,handle_index)
            #self.rectangle_update()

    def _format(self, val):
        """Pretty-print *val*."""
        if self.valfmt is not None:
            return f"({self.valfmt % val[0]}, {self.valfmt % val[1]})"
        else:
            _, s1, s2, _ = self._fmt.format_ticks(
                [self.valmin, *val, self.valmax]
            )
            # fmt.get_offset is actually the multiplicative factor, if any.
            s1 += self._fmt.get_offset()
            s2 += self._fmt.get_offset()
            # Use f string to avoid issues with backslashes when cast to a str
            return f"({s1}, {s2})"

    def set_min(self, min):
        """
        Set the lower value of the slider to *min*.
        Parameters
        ----------
        min : float
        """
        self.set_val((min, self.val[1]))

    def set_max(self, max):
        """
        Set the lower value of the slider to *max*.
        Parameters
        ----------
        max : float
        """
        self.set_val((self.val[0], max))

    def set_val(self, val):
        """
        Set slider value to *val*.
        Parameters
        ----------
        val : tuple or array-like of float
        """
        val = np.sort(val)
        #_api.check_shape((2,), val=val)
        # Reset value to allow _value_in_bounds() to work.
        self.val = (self.valmin, self.valmax)
        vmin, vmax = self._value_in_bounds(val)
        self._update_selection_poly(vmin, vmax)
        if self.orientation == "vertical":
            self._handles[0].set_ydata([vmin])
            self._handles[1].set_ydata([vmax])
        else:
            self._handles[0].set_xdata([vmin])
            self._handles[1].set_xdata([vmax])

        self.valtext.set_text(self._format((vmin, vmax)))

        if self.drawon:
            self.ax.figure.canvas.draw_idle()
        self.val = (vmin, vmax)
        if self.eventson:
            self._observers.process("changed", (vmin, vmax))

    def on_changed(self, func):
        return self._observers.connect('changed', lambda val: func(val))


a=0.7
color_left='green'
color_middle='red'
color_right='blue'
defaults={'facecolor': 'blue', 'edgecolor': 'red', 'size': 30}
fig_slider = plt.figure(figsize=(10,1))
ax_slider=fig_slider.add_axes([0.1,0.5,0.75,0.3])#, facecolor=axcolor)
defaults={'facecolor': 'blue', 'edgecolor': 'red', 'size': 30}
valinit=[30,75]
sfreq = RangeSlider(ax_slider, 'DoubleSlider', 1, 100,valstep=1,valinit=valinit,handle_style=defaults,color_left=color_left,color_middle=color_middle,color_right=color_right)#([a,a,a],[0.,0.,1.]))plt.show()
plt.show()


