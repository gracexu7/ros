import numpy as np
import cv2 as cv

K = np.array([[832.8384300194141, 0.0, 746.8429494534007], [0.0, 833.2396265836858, 481.4323243408501], [0.0, 0.0, 1.0]])
D = np.array([[-0.09727827932086659], [0.1197741419695968], [-0.20570348346277975], [0.08744077841345506]])
DIM=(1440, 960)

cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    #h, w = frame.shape[:2]
    #newcameramtx = cv.fisheye.estimateNewCameraMatrixForUndistortRectify(K,D,DIM, np.eye(3),balance=1)
    map1, map2 = cv.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv.CV_16SC2)
    dst= cv.remap(frame, map1, map2, interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)

    cv.imshow('UNDISTORTED', dst)

    #End loop when hit d
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()