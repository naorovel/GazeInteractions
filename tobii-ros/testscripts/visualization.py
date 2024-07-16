# import cv2
import matplotlib
import numpy as np
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from tobii_stream_engine import Api, Device, GazePoint, EyePosition, Stream, GazeOrigin, GazePoint, Stream, UserPresence, get_api_version
from gaze_demo import normalize_alpha, upsample_alpha, heatmap_overlay, gaussian
import cv2

class HeatmapVisualizer():

    def __init__(self, blit=False): 
        self.blit = blit
        plt.ion()
        self.fig, self.ax = plt.subplots()
        # img = plt.imread("desktop.png")
        # self.ax.imshow(img)
        self.x = []
        self.y = []
        self.scat = self.ax.scatter(self.x, self.y)
        self.line, = self.ax.plot(self.x, self.y, color="crimson", zorder=4)
        plt.ylim(1920, 0)
        plt.xlim(0, 2880)
        self.fig.canvas.draw()

        if blit:
            # cache the background for faster drawing
            self.ax2background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

        plt.show(block=False)
        return

    def redraw_scatterplot(self, pt: GazePoint):
        self.x.append(pt.x)
        self.y.append(pt.y)
        old_off = self.scat.get_offsets()
        new_off = np.concatenate([old_off,np.array([pt.x, pt.y], ndmin=2)])
        self.scat.set_offsets(new_off)
        self.line.set_data(self.x, self.y)

        if self.blit: 
            self.fig.canvas.restore_region(self.ax2background)

            self.ax.draw_artist(self.scat)
            self.fig.canvas.blit(self.ax.bbox)
        else: 
            self.fig.canvas.draw()

        self.fig.canvas.flush_events()
        return

    def init_heatmap(self, blit=False): 
        # self.blit = blit
        # plt.ion()
        # self.fig, self.ax = plt.subplots()
        # # img = plt.imread("desktop.png")
        # # self.ax.imshow(img)
        # self.x = []
        # self.y = []
        # self.scat = self.ax.scatter(self.x, self.y)
        # self.line, = self.ax.plot(self.x, self.y, color="crimson", zorder=4)
        # plt.ylim(1920, 0)
        # plt.xlim(0, 2880)
        # self.fig.canvas.draw()

        # if blit:
        #     # cache the background for faster drawing
        #     self.ax2background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

        # plt.show(block=False)
        plt.ion()
        img = cv2.imread("desktop.png")
        fig, self.ax = plt.subplots()
        self.heatmap = self.ax.imshow(img)
        self.prev_M = np.zeros((2880, 1920), dtype=float)
        plt.show()
    
    def draw_heatmap(self, pt: GazePoint):
        img = cv2.imread("desktop.png")
        x, y = pt.x, pt.y
        h, w = img.shape[:2]

        # Give normalized coordinates
        x /= w
        y /= h

        # Can give a lower resolution gaze map and upsample it later
        resolution = (120, 120)
        M = gaussian(x, y, resolution=resolution, sigma=8)
        M_display = np.add(M, self.prev_M)
        self.prev_M = M
        vis = heatmap_overlay(img, M_display)
        vis = cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)
        self.ax.imshow(vis)

        self.prev_vis = vis
        # self.heatmap.set_data(vis)
        # plt.imshow(vis)
        plt.pause(0.0001)
        plt.draw()
        # plt.imshow(vis)
        # plt.show()

        return
    


