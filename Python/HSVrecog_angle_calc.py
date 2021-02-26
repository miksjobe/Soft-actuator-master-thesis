import cv2                                                      # OpenCV
import serial                                                   # Serial communication
#import scipy.io                                                # Not used?
import numpy as np                                              # Arrays and linear algebra
#import matplotlib.pyplot as plt                                # Not used?
from apscheduler.schedulers.blocking import BlockingScheduler   # Scheduler so every operations takes equal time
#import math                                                    # Not used?
import time                                                     # Sleep

#----------------------------------------------------------------------------#
# Grabs frame, resize and split ino different channels.
def grab_frame(cap):
    global width, height, scale
    #frame = cv2.imread('test.png',1)
    ret,frame = cap.read()
    frame = cv2.rectangle(frame, (0,370), (220,500),(255,255,255),-1)
    #frame = cv2.medianBlur(frame,5)
    #frame = cv2.bilateralFilter(frame,15,50,50)
    img_bgr = cv2.resize(frame, (int(width*scale),int(height*scale)), interpolation = cv2.INTER_AREA)
    img_hsv = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
    return img_bgr, img_hsv

#----------------------------------------------------------------------------#
# Finds center of mass for the color dots, specified in Main()
def find_center_with_color(img_hsv,lower_color, upper_color):
    mask = cv2.inRange(img_hsv, lower_color, upper_color)
    # get all non zero values
    points = cv2.findNonZero(mask)

    if points is None:
        return False
    else:
        x = [p[0][0] for p in points]
        y = [p[0][1] for p in points]
        cen = (sum(x) / len(x), sum(y) / len(x))

    return(cen)

#----------------------------------------------------------------------------#
# Finds radius and origio of an circle with 3 points (2D)
def circleRadius(b, c, d):
    temp = c[0]**2 + c[1]**2
    bc = (b[0]**2 + b[1]**2 - temp) / 2
    cd = (temp - d[0]**2 - d[1]**2) / 2
    det = (b[0] - c[0]) * (c[1] - d[1]) - (c[0] - d[0]) * (b[1] - c[1])

    if abs(det) < 1.0e-10:
        return False

    # Center of circle
    cx = (bc*(c[1] - d[1]) - cd*(b[1] - c[1])) / det
    cy = ((b[0] - c[0]) * cd - (c[0] - d[0]) * bc) / det
    origo = (cx,cy)

    radius = ((cx - b[0])**2 + (cy - b[1])**2)**.5

    return radius,origo

#----------------------------------------------------------------------------#
# Finds relative angle between 2 vectors, retuns Degrees
def relative_angle(a, b, c):
    ab = (b[0]-a[0], b[1]-a[1])
    bc = (c[0]-b[0], c[1]-b[1])

    unit_ab = ab / np.linalg.norm(ab)
    unit_bc = bc / np.linalg.norm(bc)
    dot = np.dot(unit_ab,unit_bc)
    angle = np.arccos(dot)*180/np.pi

    if angle <0: return 0
    elif angle >180: return 180
    return angle

#----------------------------------------------------------------------------#
# Finds the current angle, with help from Relative_angle(), Saves old values to smooth out noise
def find_angle():
    img_bgr, img_hsv = grab_frame(cap)
    global cen1_old
    global cen2_old
    global cen3_old
    global radius_old
    global origo_old
    # find the cen of the color marks
    if (find_center_with_color(img_hsv,lower_red, upper_red) != False):
        cen1 = find_center_with_color(img_hsv,lower_red, upper_red)
        cen1_old = cen1
    else:
        cen1 = cen1_old

    if (find_center_with_color(img_hsv,lower_green, upper_green) != False):
        cen2 = find_center_with_color(img_hsv,lower_green, upper_green)
        cen2_old = cen2
    else:
        cen2 = cen2_old

    if (find_center_with_color(img_hsv,lower_black, upper_black) != False):
        cen3 = find_center_with_color(img_hsv,lower_black, upper_black)
        cen3_old = cen3
    else:
        cen3 = cen3_old

    if (circleRadius(cen1,cen2,cen3) !=False):
        radius,origo = circleRadius(cen1,cen2,cen3)
        radius_old = radius
        origo_old = origo
    else:
        radius = radius_old
        origo = origo_old

    angle = relative_angle(cen1,cen2,cen3)

    #------------------------------------------------------------------------#
    #Displays the points and lines between them on a graphisc window
    #------------------------------------------------------------------------#
    if show=='all':
        cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
        img_bgr = cv2.circle(img_bgr, (int(origo[0]),int(origo[1])), int(radius),(100,50,50),1)
        img_bgr = cv2.line(img_bgr, (int(cen1[0]),int(cen1[1])), (int(cen2[0]),int(cen2[1])), (0, 0, 255) , 1)
        img_bgr = cv2.line(img_bgr, (int(cen2[0]),int(cen2[1])), (int(cen3[0]),int(cen3[1])), (0, 255, 0) , 1)
        img_bgr = cv2.line(img_bgr, (int(cen3[0]),int(cen3[1])), (int(cen1[0]),int(cen1[1])), (0, 0, 0) , 1)
        cv2.imshow('image', img_bgr)
        cv2.waitKey(1)
    elif show=='lines':
        global width, height, scale
        cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
        img_bgr = np.zeros((int(height*scale),int(width*scale),3),np.uint8)
        img_bgr[:] = 255,255,255
        img_bgr = cv2.circle(img_bgr, (int(origo[0]),int(origo[1])), int(radius),(100,50,50),1)
        img_bgr = cv2.line(img_bgr, (int(cen1[0]),int(cen1[1])), (int(cen2[0]),int(cen2[1])), (0, 0, 255) , 1)
        img_bgr = cv2.line(img_bgr, (int(cen2[0]),int(cen2[1])), (int(cen3[0]),int(cen3[1])), (0, 255, 0) , 1)
        img_bgr = cv2.line(img_bgr, (int(cen3[0]),int(cen3[1])), (int(cen1[0]),int(cen1[1])), (0, 0, 0) , 1)
        cv2.imshow('image', img_bgr)
        cv2.waitKey(1)
    else:
        pass
    return angle

#----------------------------------------------------------------------------#
# Sends multiple Bytes to the Serial Communication
def send_data(data1, data2):#, data3):
    data_bytes = bytes([])
    data1 = abs(data1 - 135)
    for data in [data1, data2]:#, data3]:
        data_times_100 = int(round(data,2)*100)
        data_bytes +=  bytes([int(data_times_100/256)]) + bytes([int(data_times_100%256)])
    # send the data
    ser.write(data_bytes)
    #print(data_bytes)
    print(list(data_bytes),data1,data2)

#----------------------------------------------------------------------------#
# Sends 2 Bytes for 1 inserted data, this to increase resoultion of the sent value.
def send_single_data(data):
    #data = 12.34
    #data_bytes = bytes([])
    data_times_100 = int(round(data,2)*100)
    data_bytes = bytes([int(data_times_100/256)]) + bytes([int(data_times_100%256)])
    # send the data
    ser.write(data_bytes)
    #print(list(data_bytes),data)

#----------------------------------------------------------------------------#
# Specifies what whall be run during schedueled tasks.
def job_list():
    global Ts
    angle=find_angle()
    print(angle)
    send_single_data(angle)
    #print(ser.in_waiting)
    #if ser.in_waiting>0:

    #ser.write(bytes([255]))
    #if ser.isOpen():
    #    send_single_data(angle) #mult by 3.6 to get the most accuracy
    #    if (ser.readline().decode('utf-8')=="0\r\n"):# and (ser.in_waiting>0):
    #        ser.write(bytes([100]))
    #else:
    #    scheduler.shutdown(wait=False)
        #pass
    #time.sleep(round(Ts*0.01,3))

#----------------------------------------------------------------------------#
# Main function starting from HERE:
#----------------------------------------------------------------------------#
# HSV codes range of used colors. Use Calibrate_color_HSV_codes.py
lower_red = np.array([ 0 , 157 , 116 ])
upper_red = np.array([ 19 , 255 , 255 ])
lower_green = np.array([ 43 , 95 , 78 ])
upper_green = np.array([ 95 , 255 , 255 ])
lower_black = np.array([ 0 , 16 , 0 ])
upper_black = np.array([ 179 , 144 , 42 ])


# Failsafe values for Null cases
cen1_old=(0,0)
cen2_old=(0,0)
cen3_old=(0,0)
radius_old=1
origo_old=(1,1)

#----------------------------------------------------------------------------#
# initiate the camera and the serial communication
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ser = serial.Serial("COM12", 115200)
#ser = serial.Serial('COM3', 9600)
ser.reset_input_buffer()

ret, frame = cap.read()
width = frame.shape[1]
height = frame.shape[0]
scale = 0.5
Ts = 0.05

#Show:      all=show capture and lines.  lines=only lines on white background       none = no visuals
show = 'all'
#show = 'lines'
#show = 'none'

#---------------------------------------------------------------------------#
# scheduled task at Ts intervals
scheduler = BlockingScheduler()
scheduler.add_job(job_list,'interval',seconds=Ts,id='job_list',misfire_grace_time=10,coalesce=True)
scheduler.start()

#----------------------------------------------------------------------------#
cv2.destroyAllWindows()
