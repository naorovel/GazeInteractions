import pyautogui
import math

prev_points = [[], []]
last_timestamp = 0
dwell_time = 1000000 # 1000ms
prev_avg = []
distance = 50

def move_mouse(timestamp: int, x: int, y: int): 
    global last_timestamp
    global prev_points
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0
    global prev_avg
     
    # Check if point is near previous point: 
    if prev_points[0] == []: # No previous point in buffer
        prev_points[0] = [x]
        prev_points[1] = [y]
        last_timestamp = timestamp
        prev_avg = [x, y]
    else: # There is a previous point in the buffer
        global distance

        if dist((prev_avg[0], prev_avg[1]), (x, y)) <= distance: 
            # Point is in the radius, will be checked for timestamp
            if timestamp - last_timestamp >= dwell_time: 
                avg_x = sum(prev_points[0])/len(prev_points[0])
                avg_y = sum(prev_points[1])/len(prev_points[1])

                prev_avg = [avg_x, avg_y]

                pyautogui.click(avg_x, avg_y) # Click at the average of all the points in the buffer

                # Clear the buffer
                prev_points = [[], []]
                prev_avg = []
            else: 
                # Add point to buffer
                prev_points[0].append(x)
                prev_points[1].append(y)

                avg_x = sum(prev_points[0])/len(prev_points[0])
                avg_y = sum(prev_points[1])/len(prev_points[1])
                prev_avg = [avg_x, avg_y]
        else: # Clear the buffer if points are not close enough to each other
            prev_points = [[], []]
            prev_avg = []

    return


def dist(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
