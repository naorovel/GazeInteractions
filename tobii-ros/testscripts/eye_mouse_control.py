import time
import pyautogui
from itertools import combinations
import math

MOUSE_NEIGHBOURHOOD_SQUARED:int = 100 # default neighbourhood in px
curr_mouse_neighbourhood = 1
prev_points = [[], []]
MIN_POINTS:int = 10
last_clicked = False
last_timestamp = 0
refresh_rate = 100000

def move_mouse(timestamp: int, x: int, y: int): 
    global last_timestamp
    global prev_points
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0
     
    # Check if point is near previous point: 
    if prev_points[0] == []: # No previous point in buffer
        prev_points[0] = [x]
        prev_points[1] = [y]
        last_timestamp = timestamp
    else: # There is a previous point in the buffer
        if dist((prev_points[0][-1], prev_points[1][-1]), (x, y)) <= 50: 
            # Point is in the radius, will be checked for timestamp
            pyautogui.moveTo(x, y, 0)
            if timestamp - last_timestamp >= 2000000: 
                print("should have clicked")
                pyautogui.click(x,y)
                # Clear the buffer
                prev_points = [[], []]
            else: 
                # Add point to buffer
                prev_points[0].append(x)
                prev_points[1].append(y)
        else: # Clear the buffer if points are not close enough to each other
            prev_points = [[], []]

    return

def dist(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
