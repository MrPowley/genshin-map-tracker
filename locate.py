import numpy as np
import cv2
from os.path import exists
import pickle
import time

MIN_MATCH_COUNT = 7

def locate():
    minimap = cv2.imread('assets/minimap.png', cv2.IMREAD_GRAYSCALE) # queryImage
    # minimap = cv2.resize(minimap, (int(minimap.shape[1]/2.5), int(minimap.shape[1]/2.5)))
    
    # Initiate SIFT detector
    sift = cv2.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(minimap,None)
    if not exists("assets/map_kp_des.pkl"):
        map = cv2.imread('assets/map.png', cv2.IMREAD_GRAYSCALE) # trainImage
        map = cv2.resize(map, None, fx=0.3, fy=0.3)
        kp2, des2 = sift.detectAndCompute(map,None)
        kp2_serializable = [(kp.pt, kp.size, kp.angle, kp.response, kp.octave, kp.class_id) for kp in kp2]
        with open("assets/map_kp_des.pkl", "wb") as f:
            pickle.dump((kp2_serializable, des2), f)
    else:
        with open("assets/map_kp_des.pkl", "rb") as f:
            kp2_serializable, des2 = pickle.load(f)
            kp2 = [cv2.KeyPoint(x, y, _size, _angle, _response, _octave, _class_id) for (x, y), _size, _angle, _response, _octave, _class_id in kp2_serializable]

    FLANN_INDEX_KDTREE = 1
    
    t1 = time.monotonic()
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 1)
    search_params = dict(checks = 1000)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.8 * n.distance:
            good.append(m)

    print("good kp nb", len(good))
    if len(good)>=MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        # matchesMask = mask.ravel().tolist()
        h,w = minimap.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        # dst = cv2.perspectiveTransform(pts,M)
        #map = cv2.polylines(map,[np.int32(dst)],True,255,3, cv2.LINE_AA)
        
        # Obtenir les coordonnées du centre de l'image minimap dans l'image map
        center_of_minimap = np.float32([[minimap.shape[1] / 2, minimap.shape[0] / 2]]).reshape(-1, 1, 2)
        
        try:
            center_of_map = cv2.perspectiveTransform(center_of_minimap, M)
            player_coordinates = center_of_map[0][0].tolist()
            print("Compute time", time.monotonic() - t1,"s")
            return player_coordinates
        except Exception:
            return -9999, -9999
    else:
        return -9999, -9999
