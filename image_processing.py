#!/usr/bin/python3
# python -m pip install pytesseract

import cv2
import numpy as np
import time,sys

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract'
# pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract"
# Example tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract'

# Simple image to string
# print(pytesseract.image_to_string(Image.open('C:/Users/Wallouf/Desktop/python/test.png')))
# print(pytesseract.image_to_string(Image.open('C:/Users/Wallouf/Desktop/python/test.png'), config='-c tessedit_char_whitelist=123456789'))

# frame = cv2.imread("C:/Users/Wallouf/Desktop/python/test.png")

##############  Load OCR data for training #######################################
samples = np.float32(np.loadtxt('feature_vector_pixels.data'))
responses = np.float32(np.loadtxt('samples_pixels.data'))

model = cv2.ml.KNearest_create()
model.train(samples, cv2.ml.ROW_SAMPLE, responses)



def rectify(h):
        h = h.reshape((4,2))
        hnew = np.zeros((4,2),dtype = np.float32)
 
        add = h.sum(1)
        hnew[0] = h[np.argmin(add)]
        hnew[2] = h[np.argmax(add)]
         
        diff = np.diff(h,axis = 1)
        hnew[1] = h[np.argmin(diff)]
        hnew[3] = h[np.argmax(diff)]
  
        return hnew

img =  cv2.imread('C:/Users/Wallouf/Desktop/python/test.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)

image_area = gray.size

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

biggest = None
max_area = 0

for i in contours:
    area = cv2.contourArea(i)
    if area > (image_area/2):
        peri = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i,0.02*peri, True)
        if area > max_area and len(approx)==4:
            biggest = approx
            max_area = area

h = np.array([ [0,0],[449,0],[449,449],[0,449] ], np.float32)    # this is corners of new square image taken in CW order

biggest = rectify(biggest)
retval = cv2.getPerspectiveTransform(biggest, h)  # apply perspective transformation

warp = cv2.warpPerspective(img, retval, (450,450))  # Now we get perfect square with size 450x450
warp_thresh = cv2.warpPerspective(thresh, retval, (450,450))  # Now we get perfect square with size 450x450

warpg = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)


############ now take each element for inspection ##############

dict_values_readed = dict()

for case in range(0,81):
    dict_values_readed[case] = 0

smooth = cv2.GaussianBlur(warpg ,(3,3), 3)
thresh = cv2.adaptiveThreshold(smooth, 255, 0, 1, 5, 2)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
erode = cv2.erode(thresh, kernel, iterations = 1)
dilate = cv2.dilate(erode, kernel, iterations = 1)


contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


for cnt in contours:
    area = cv2.contourArea(cnt)
    
    (bx,by,bw,bh) = cv2.boundingRect(cnt)
    
    # if 1 == 1:
    if (100<bw*bh<1200) and (10<bw<40) and (25<bh<45):
        roi = dilate[by:by+bh,bx:bx+bw]
        
        small_roi = cv2.resize(roi,(10,10))
        feature = small_roi.reshape((1,100)).astype(np.float32)

        ret,results,neigh,dist = model.findNearest(feature,k=1)
        integer = int(results.ravel()[0])
        
        gridx = int((bx+bw/2) / 50)
        gridy = int((by+bh/2) / 50)

        # calcul square
        posx = gridx + 1
        posy = gridy + 1

        square=1

        offsetx = 0
        offsety = 0

        if posx > 6:
            square += 2
            offsetx = 6
        elif posx > 3:
            square += 1
            offsetx = 3

        if posy > 6:
            square += 6
            offsety = 6
        elif posy > 3:
            square += 3
            offsety = 3

        # Calculate position
        square_offset = ((square - 1) * 9)
        
        case = square_offset + ((posy - offsety - 1) * 3) + (posx - offsetx)

        dict_values_readed[case] = integer

dict_values_solved = dict_values_readed

#################### Uncomment below two lines if you want to print solved 9x9 matrix sudoku on terminal, optional ####################

#l = [int(i) for i in ans]      # we make string ans to a list 
#ansarray = np.array(l,np.uint8).reshape((9,9))  # Now we make it into an array of sudoku

############### Below print sudoku answer on our image.  #########################################
for case in range(1,82):
    if dict_values_readed[case] == 0:

        square = int((case - 1) / 9)
        line = int(((case-(square*9))-1)/3) + 1 + (int(square/3) * 3)
        col = (((case - 1) - (square * 9)) % 3) + 1 + ((square % 3) * 3)



        print("")
        print("Case: ", case)
        print("Square: ", square)
        print("Line: ", line)
        print("Col: ", col)
        print("Value: ", dict_values_solved[case])

        posx = (col-1) * 50 + 13
        posy = (line-1) * 50 + 13

        # raw_y, raw_x = i/9, i%9
        

        # posx,posy = int(raw_x * 50 + 15), int(raw_y * 50) + int(20 - (raw_y * 3))

        cv2.putText(warp, str(dict_values_solved[case]), (posx,posy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3, cv2.LINE_AA, True)
        
cv2.imshow('img',warp)


cv2.waitKey(0)
cv2.destroyAllWindows()