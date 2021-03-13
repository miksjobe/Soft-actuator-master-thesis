import cv2
import numpy as np

Ts = 20 #milliseconds

cap=cv2.VideoCapture(0)

#----------------------------------------------------------------------------#
# Grabs dimensions of the camera to rescale while keeping aspect-ratio
ret, frame = cap.read()
width = frame.shape[1]
height = frame.shape[0]
scale = 0.5

cv2.namedWindow('Masks_R_G_B', cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow('Masks_R_G_B', int(width*scale*3),int(height*scale))

#---------------------------------------------------------------------------#
# Starting posistion of the Trackbars, paste here after the calbiration to remember the latest values.
lower_red = np.array([ 0 , 157 , 116 ])
upper_red = np.array([ 19 , 255 , 255 ])
lower_green = np.array([ 43 , 127 , 119 ])
upper_green = np.array([ 95 , 255 , 255 ])
lower_black = np.array([ 0 , 16 , 0 ])
upper_black = np.array([ 179 , 255 , 38 ])

# Needed for the trackbars
def empty(a):
    pass

# Trackbar Red: H,S,V lower and upper
cv2.namedWindow('R_Trackbar')
cv2.resizeWindow('R_Trackbar',300,250)
cv2.createTrackbar('RH_min', 'R_Trackbar', lower_red[0], 179, empty)
cv2.createTrackbar('RH_max', 'R_Trackbar', upper_red[0], 179, empty)
cv2.createTrackbar('RS_min', 'R_Trackbar', lower_red[1], 255, empty)
cv2.createTrackbar('RS_max', 'R_Trackbar', upper_red[1], 255, empty)
cv2.createTrackbar('RV_min', 'R_Trackbar', lower_red[2], 255, empty)
cv2.createTrackbar('RV_max', 'R_Trackbar', upper_red[2], 255, empty)

# Trackbar Green: H,S,V lower and upper
cv2.namedWindow('G_Trackbar')
cv2.resizeWindow('G_Trackbar',300,250)
cv2.createTrackbar('GH_min', 'G_Trackbar', lower_green[0], 179, empty)
cv2.createTrackbar('GH_max', 'G_Trackbar', upper_green[0], 179, empty)
cv2.createTrackbar('GS_min', 'G_Trackbar', lower_green[1], 255, empty)
cv2.createTrackbar('GS_max', 'G_Trackbar', upper_green[1], 255, empty)
cv2.createTrackbar('GV_min', 'G_Trackbar', lower_green[2], 255, empty)
cv2.createTrackbar('GV_max', 'G_Trackbar', upper_green[2], 255, empty)

# Trackbar Black: H,S,V lower and upper
cv2.namedWindow('B_Trackbar')
cv2.resizeWindow('B_Trackbar',300,250)
cv2.createTrackbar('BH_min', 'B_Trackbar', lower_black[0], 179, empty)
cv2.createTrackbar('BH_max', 'B_Trackbar', upper_black[0], 179, empty)
cv2.createTrackbar('BS_min', 'B_Trackbar', lower_black[1], 255, empty)
cv2.createTrackbar('BS_max', 'B_Trackbar', upper_black[1], 255, empty)
cv2.createTrackbar('BV_min', 'B_Trackbar', lower_black[2], 255, empty)
cv2.createTrackbar('BV_max', 'B_Trackbar', upper_black[2], 255, empty)


while True:
    ret, frame = cap.read()
    #frame = cv2.imread('Image1.jpg',1)
    frame = cv2.rectangle(frame, (0,round(0.75*height)), (round(0.35*width),height), (255,255,255), -1)
    frame = cv2.resize(frame, (int(width*scale),int(height*scale)), interpolation = cv2.INTER_AREA)

    #-----------------------------------------------------------------------#
    # Tries on filtering the original capture for easier tracking. Slows down the process, though.
    #frame = cv2.medianBlur(frame,5)
    #img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #frame = cv2.bilateralFilter(frame,15,50,50)
    #img = np.histogram(frame.flatten(),256,[0,256])
    #img_hsv = cv2.equalizeHist(img_hsv)

    img_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # Get values from trackbars
    c_lower_red = np.array([cv2.getTrackbarPos('RH_min','R_Trackbar'),cv2.getTrackbarPos('RS_min','R_Trackbar'),cv2.getTrackbarPos('RV_min','R_Trackbar')])
    c_upper_red = np.array([cv2.getTrackbarPos('RH_max','R_Trackbar'),cv2.getTrackbarPos('RS_max','R_Trackbar'),cv2.getTrackbarPos('RV_max','R_Trackbar')])

    c_lower_green = np.array([cv2.getTrackbarPos('GH_min','G_Trackbar'),cv2.getTrackbarPos('GS_min','G_Trackbar'),cv2.getTrackbarPos('GV_min','G_Trackbar')])
    c_upper_green = np.array([cv2.getTrackbarPos('GH_max','G_Trackbar'),cv2.getTrackbarPos('GS_max','G_Trackbar'),cv2.getTrackbarPos('GV_max','G_Trackbar')])

    c_lower_black = np.array([cv2.getTrackbarPos('BH_min','B_Trackbar'),cv2.getTrackbarPos('BS_min','B_Trackbar'),cv2.getTrackbarPos('BV_min','B_Trackbar')])
    c_upper_black = np.array([cv2.getTrackbarPos('BH_max','B_Trackbar'),cv2.getTrackbarPos('BS_max','B_Trackbar'),cv2.getTrackbarPos('BV_max','B_Trackbar')])

    # find the matching pixels in the image and arrange the windows.
    mask_red = cv2.inRange(img_hsv, c_lower_red, c_upper_red)
    mask_green = cv2.inRange(img_hsv, c_lower_green, c_upper_green)
    mask_black = cv2.inRange(img_hsv, c_lower_black, c_upper_black)
    masks = cv2.hconcat([mask_red,mask_green,mask_black])
    capture = cv2.hconcat([frame, img_hsv])

    cv2.imshow('Capture',capture)
    cv2.imshow('Masks_R_G_B',masks)

    if cv2.waitKey(Ts) & 0xFF==ord('q'):
        break

# Prints the values in code-form so they can be copied and pasted easily.
print('lower_red = np.array([',c_lower_red[0],',',c_lower_red[1],',',c_lower_red[2],'])')
print('upper_red = np.array([',c_upper_red[0],',',c_upper_red[1],',',c_upper_red[2],'])')
print('lower_green = np.array([',c_lower_green[0],',',c_lower_green[1],',',c_lower_green[2],'])')
print('upper_green = np.array([',c_upper_green[0],',',c_upper_green[1],',',c_upper_green[2],'])')
print('lower_black = np.array([',c_lower_black[0],',',c_lower_black[1],',',c_lower_black[2],'])')
print('upper_black = np.array([',c_upper_black[0],',',c_upper_black[1],',',c_upper_black[2],'])')

cv2.destroyAllWindows()
#cv2.VideoCapture(0).release()
