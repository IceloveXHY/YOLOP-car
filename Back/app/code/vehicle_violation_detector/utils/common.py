import cv2
import numpy as np

def get_center(box):
    x1, y1, x2, y2 = box
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

def point_in_roi(point, roi):
    contour = np.array(roi, dtype=np.int32)
    return cv2.pointPolygonTest(contour, point, False) >= 0
