#!/usr/bin/python3
import cv2
import numpy as np
import time, sys, base64

import sudoku

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract'

current_milli_time = lambda: int(round(time.time() * 1000))


def to_base64(img):
    _, buf = cv2.imencode(".jpg", img)
    return "data:image/jpeg;base64," + str(base64.b64encode(buf), 'utf-8')


def from_base64(buf):
    decoded_data = base64.b64decode(buf.split(',')[1])
    np_data = np.frombuffer(decoded_data,np.uint8)
    
    return cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)

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

def check_image_size(original_img):
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

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    biggest = None
    max_area = 0

    for i in contours:
        area = cv2.contourArea(i)
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

def detect_integer(model, images_pytesseract, images_knearest):
    integers_found = []

    for image_pytesseract in images_pytesseract:
        # Use pytesseract
        result = pytesseract.image_to_string(image_pytesseract, config='--psm 7 -c tessedit_char_whitelist=123456789')
        try:
            result = int(result)
            integers_found.append(result)
        except Exception as e:
            pass

    for image_knearest in images_knearest:
        # Try to search number with OPENCV KNEAREST
        small_roi = cv2.resize(image_knearest,(10,10))
        feature = small_roi.reshape((1,100)).astype(np.float32)
        _,results,_,_ = model.findNearest(feature,k=1)
        
        try:
            result = int(results.ravel()[0])
            integers_found.append(result)
        except Exception as e:
            pass

    return integers_found

def retrieve_number_from_square(image):
    samples = np.float32(np.loadtxt('samples.data'))
    responses = np.float32(np.loadtxt('responses.data'))

    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)
    
    warpg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    dict_values_readed = dict()

    for case in range(1,82):
        dict_values_readed[case] = 0

    smooth = cv2.GaussianBlur(warpg ,(3,3), 3)
    thresh = cv2.adaptiveThreshold(smooth, 255, 0, 1, 5, 2)

    kernel_type1 = cv2.getStructuringElement(cv2.MORPH_CROSS, (2,2))
    kernel_type2 = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    
    erode_type1 = cv2.erode(thresh, kernel_type1, iterations = 1)
    erode_type2 = cv2.erode(thresh, kernel_type2, iterations = 1)

    dilate_type1 =cv2.dilate(erode_type1,kernel_type1,iterations =1)
    dilate_type2 =cv2.dilate(erode_type2,kernel_type2,iterations =1)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        (bx,by,bw,bh) = cv2.boundingRect(cnt)

        if (100<bw*bh<1800) and (5<bw<40) and (20<bh<45):

            integers_found = detect_integer(model, [], [erode_type1[by:by+bh,bx:bx+bw], erode_type2[by:by+bh,bx:bx+bw], thresh[by:by+bh,bx:bx+bw], dilate_type1[by:by+bh,bx:bx+bw], dilate_type2[by:by+bh,bx:bx+bw]])
            if len(integers_found) == 0:
                continue

            integer = max(set(integers_found), key = integers_found.count)

            
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

            print("Case: ", case)
            print("Integer: ", integer)
            print("integers: ", integers_found)

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

                posx = (col-1) * 50 + 14
                posy = (line-1) * 50 + 35

                cv2.putText(image, str(dict_values_solved[case]), (posx,posy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,50,50), 3, cv2.LINE_AA, False)
                
    return image


def launch_image_processing_with_base64(data_uri):
    processed_img = process_image(from_base64(data_uri))
    # Re-encode to base64
    return to_base64(processed_img)

def launch_image_processing_with_path(image_path):
    return process_image(cv2.imread(image_path))


def process_image(original_img):
    begin = current_milli_time()
    
    original_img = check_image_size(original_img)
    processed_img = original_img

    image_square_found = search_square_from_image(original_img)

    dict_values_readed = None

    if image_square_found is not None:
        processed_img = image_square_found
        dict_values_readed = retrieve_number_from_square(image_square_found)

    print("Value detected:")
    for index in range(1,82):
        if dict_values_readed[index] != 0:
            print("\tIndex: ", index)
            print("\tValue: ", dict_values_readed[index])
            print("")

    if dict_values_readed is not None:
        processed_img = print_results(processed_img, dict_values_readed, solve_sudoku(dict_values_readed))
    else:
        processed_img = print_results(processed_img, None, None)
    
    print("Duration : ", (current_milli_time() - begin))

    return processed_img