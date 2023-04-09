# You should replace these 3 lines with the output in calibration step
import cv2
import numpy as np
import sys

DIM=(1440, 960)
K=np.array([[832.8384300194141, 0.0, 746.8429494534007], [0.0, 833.2396265836858, 481.4323243408501], [0.0, 0.0, 1.0]])
D=np.array([[-0.09727827932086659], [0.1197741419695968], [-0.20570348346277975], [0.08744077841345506]])
def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)