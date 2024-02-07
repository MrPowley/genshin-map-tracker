import numpy as np
import cv2
from os.path import exists
import pickle
import time

import pyautogui

# Number of "good" points" calculated
MIN_MATCH_COUNT = 7

# Locate function
def locate(minimap):    
    # Initiate SIFT detector
    sift = cv2.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(minimap,None)

    # Cheking if map's keypoints and descriptors are present in the assets folder
    # Would definilty not recommand somebody lauching the program without the map data
    # Check readme.md for more info
    if not exists("assets/map_kp_des.pkl"):
        map = cv2.imread('assets/map.png', cv2.IMREAD_GRAYSCALE) # trainImage
        map = cv2.resize(map, None, fx=0.3, fy=0.3)
        kp2, des2 = sift.detectAndCompute(map,None)
        kp2_serializable = [(kp.pt, kp.size, kp.angle, kp.response, kp.octave, kp.class_id) for kp in kp2]
        with open("assets/map_kp_des.pkl", "wb") as f:
            pickle.dump((kp2_serializable, des2), f)
    else:
        # Opens and load map data
        with open("assets/map_kp_des.pkl", "rb") as f:
            kp2_serializable, des2 = pickle.load(f)
            kp2 = [cv2.KeyPoint(x, y, _size, _angle, _response, _octave, _class_id) for (x, y), _size, _angle, _response, _octave, _class_id in kp2_serializable]

    # Detection algorithm
    FLANN_INDEX_KDTREE = 1
    # Juste to check compute time
    t1 = time.monotonic()
    # Settings knn parameters, More trees == better precision + more compute time
    # the less tree the fastest, with 1 tree, speed is around 0.6s comute time average
    # With 10 trees, computetime is 8s average
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 1)
    # The less trees, the more checks needed to keep the map from going insane
    # for 1 tree, i recommand betwin 500 and 100 checks, i didn't realy deeply tested this tho
    # For 10 trees, i recommand around 50 checks
    search_params = dict(checks = 1000)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    # Start computing and getting the good matches
    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.8 * n.distance:
            good.append(m)

    # Make shure the is more good points than the minimum set
    if len(good)>=MIN_MATCH_COUNT:
        # No idea what's appening, i'm a total noob with numpy
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        # getting minimap size
        h,w = minimap.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        
        # Getting cordinates from the center of the minimap
        center_of_minimap = np.float32([[minimap.shape[1] / 2, minimap.shape[0] / 2]]).reshape(-1, 1, 2)
        
        # I dind't realy check why but the perspective transform function sometimes give an error when compute points are not good enough
        try:
            center_of_map = cv2.perspectiveTransform(center_of_minimap, M)
            player_coordinates = center_of_map[0][0].tolist()
            # Print compute time
            print("Compute time", time.monotonic() - t1,"s")
            return player_coordinates
        except Exception:
            # If any error happens, returning these off the map coordinates
            return -9999, -9999
    else:
        return -9999, -9999

# Function to check if main gui is visible: check if minimap is visible
def check_for_game_gui():
    # Taking a screeshot of the little message icon in the bottom left corner
    gui = pyautogui.screenshot(region=(52, 1364, 52, 42))
    # Converting image to array
    gui = cv2.cvtColor(np.array(gui), cv2.COLOR_RGB2GRAY)
    # Converting image to binary
    _, binary_image = cv2.threshold(gui, 127, 255, cv2.THRESH_BINARY)
    # Gettings contours of image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        # Making sure there's at least 4 sides (rectangle)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)
            # Cheking if they're at least a minimum lenght(a little less than the true size)
            if w > 45 and h > 35:
                return True
    return False
