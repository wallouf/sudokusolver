#!/usr/bin/python3
# python -m pip install pytesseract

import cv2
import numpy as np
import time,sys

import sudoku

samples = np.float32(np.loadtxt('samples.data'))
responses = np.float32(np.loadtxt('responses.data'))

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

def open_original_image(image_path):
    original_img =  cv2.imread(image_path)

    img = original_img

    # Check size
    if original_img.shape[1] > 500:
        scale_percent = original_img.shape[1] / 500
        
        width = int(original_img.shape[1] / scale_percent)
        height = int(original_img.shape[0] / scale_percent)

        # dsize
        dsize = (width, height)
        img = cv2.resize(original_img, dsize)

    return img

def search_square_from_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)

    image_area = gray.size

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    biggest = None
    max_area = 0

    for i in contours:
        area = cv2.contourArea(i)
        
        # if area > (image_area/2):
        if 1 == 1:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i,0.02*peri, True)
            if area > max_area and len(approx)==4:
                biggest = approx
                max_area = area

    h = np.array([ [0,0],[449,0],[449,449],[0,449] ], np.float32)

    if biggest is None:
        print("Cannot find square ! Cancel processing...")
        return None

    biggest = rectify(biggest)
    retval = cv2.getPerspectiveTransform(biggest, h)

    return cv2.warpPerspective(img, retval, (450,450))


def retrieve_number_from_square(image):
    global model
    
    warpg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    dict_values_readed = dict()

    for case in range(1,82):
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

    return dict_values_readed

def solve_sudoku(dict_values_readed):
    dict_values_solved = dict(dict_values_readed)

    return sudoku.solve_sudoku(dict_values_solved)


def print_results(image, dict_values_readed, dict_values_solved):
    if dict_values_readed is None:
        cv2.putText(image, "Can't read sudoku values!", (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA, False)
    elif dict_values_solved is None:
        cv2.putText(image, "Can't solve sudoku!", (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA, False)
    else:
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

                posx = (col-1) * 50 + 14
                posy = (line-1) * 50 + 35

                cv2.putText(image, str(dict_values_solved[case]), (posx,posy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3, cv2.LINE_AA, False)
                
    return image


original_img = open_original_image('C:/Users/Wallouf/Desktop/python/test3.jpg')
processed_img = original_img

image_square_found = search_square_from_image(original_img)

dict_values_readed = None

if image_square_found is not None:
    processed_img = image_square_found
    dict_values_readed = retrieve_number_from_square(image_square_found)

if dict_values_readed is not None:
    processed_img = print_results(processed_img, dict_values_readed, solve_sudoku(dict_values_readed))
else:
    processed_img = print_results(processed_img, None, None)


cv2.imshow('img', processed_img)

cv2.waitKey(0)
cv2.destroyAllWindows()