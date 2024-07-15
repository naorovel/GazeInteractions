# import cv2
import matplotlib
import numpy as np
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from tobii_stream_engine import Api, Device, GazePoint, EyePosition, Stream, GazeOrigin, GazePoint, Stream, UserPresence, get_api_version
class HeatmapVisualizer():

    def __init__(self, blit=False): 
        self.blit = blit
        plt.ion()
        self.fig, self.ax = plt.subplots()
        # self.im = plt.imread("desktop.png")
        # self.implot = plt.imshow(self.im, origin='lower')
        self.x, self.y = [], []
        self.scat = self.ax.scatter(self.x, self.y)
        plt.ylim(1920, 0)
        plt.xlim(0, 2880)
        self.fig.canvas.draw()

        if blit:
            # cache the background
            self.ax2background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

        plt.show(block=False)

    def redraw_heatmap(self, pt: GazePoint):
        # plt.scatter([pt.x], [pt.y], c='blue')
        # self.x.append(pt.x)
        old_off = self.scat.get_offsets()
        new_off = np.concatenate([old_off,np.array([pt.x, pt.y], ndmin=2)])
        self.scat.set_offsets(new_off)

        if self.blit: 
            self.fig.canvas.restore_region(self.ax2background)

            self.ax.draw_artist(self.scat)
            self.fig.canvas.blit(self.ax.bbox)
        else: 
            self.fig.canvas.draw()

        self.fig.canvas.flush_events()

        # plt.scatter(self.x, self.y, c='blue')
        # # self.addPoint([pt.x, pt.y])
        # self.x.append(pt.x)
        # self.y.append(pt.y)
        # # self.scat.set_data(self.x, self.y)
        # self.ax.draw_artist(self.scat)
        # # # print(self.x, self.y)
        # # # plt.scatter([pt.x], [pt.y], c='blue')
        # # self.ax.canvas.draw_idle()
        # # plt.pause(1e-10)
        # # plt.show()
        return
    
    def addPoint(self, new_point, c='k'):
        old_off = self.scat.get_offsets()
        new_off = np.concatenate([old_off,np.array(new_point, ndmin=2)])
        old_c = self.scat.get_facecolors()
        new_c = np.concatenate([old_c, np.array(matplotlib.colors.to_rgba(c), ndmin=2)])

        self.scat.set_offsets(new_off)
        self.scat.set_facecolors(new_c)

        self.scat.axes.figure.canvas.draw_idle()
        return