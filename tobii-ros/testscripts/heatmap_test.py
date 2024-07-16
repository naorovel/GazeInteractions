# import cv2
import matplotlib
import numpy as np
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from tobii_stream_engine import Api, Device, GazePoint, EyePosition, Stream, GazeOrigin, GazePoint, Stream, UserPresence, get_api_version
from gaze_demo import normalize_alpha, upsample_alpha, heatmap_overlay, gaussian
import cv2
import math

def init_heatmap(blit=False): 
    plt.ion()
    img = cv2.imread("desktop.png")
    fig, ax = plt.subplots()
    heatmap = ax.imshow(img)
    prev_M = np.zeros((2880, 1920), dtype=np.uint8)
    plt.show()

def draw_heatmap(x, y, prev_vis, heatmap):
    img = prev_vis
    h, w = img.shape[:2]

    # Give normalized coordinates
    x /= w
    y /= h

    # Can give a lower resolution gaze map and upsample it later
    resolution = (120, 120)
    M = gaussian(x, y, resolution=resolution, sigma=8)
    vis = heatmap_overlay(img, M)
    vis = cv2.addWeighted(prev_vis, 0.5, vis, 0.5, 0)
    prev_vis = vis

    vis = cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)

    heatmap.set_array(vis)
    return prev_vis


if __name__ == "__main__":
    #### INIT FUNCTION
    plt.ion()
    img = cv2.imread("/home/user/tobii-ros/testscripts/desktop.png")
    fig, ax = plt.subplots()
    heatmap = plt.imshow(img)
    prev_vis = np.ones((1920, 2880, 3), dtype=np.uint8)
    prev_exists = False
    # prev_vis = cv2.imread("/home/user/tobii-ros/testscripts/desktop.png")


    ### END OF INIT FUNCTION

    r = 1000
    pi = math.pi
    n = 100

    circle_points = [(math.cos(2*math.pi/100*x)*1000,math.sin(2*math.pi/100*x)*1000) for x in range(0,n+1)]

    for p in range(100):
        # img = cv2.imread("/home/user/tobii-ros/testscripts/desktop.png")
        x, y = (circle_points[p][0] + 1000, circle_points[p][1]+ 1000) # x, y
        h, w = img.shape[:2]

        prev_vis = draw_heatmap(x, y, prev_vis, heatmap)

        plt.pause(0.0001)
        plt.draw()
        fig.canvas.flush_events()