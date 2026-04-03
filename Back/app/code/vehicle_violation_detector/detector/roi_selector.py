import cv2
import numpy as np

def select_roi(frame):
    all_rois = []  # 存储多个多边形区域
    current_roi = []
    drawing = True  # 控制是否继续绘制新的 ROI

    def mouse_callback(event, x, y, flags, param):
        nonlocal drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            current_roi.append((x, y))
        elif event == cv2.EVENT_RBUTTONDOWN:
            if len(current_roi) >= 3:
                all_rois.append(current_roi.copy())
                current_roi.clear()

    clone = frame.copy()
    cv2.namedWindow("Draw Multiple ROIs")
    cv2.setMouseCallback("Draw Multiple ROIs", mouse_callback)

    while drawing:
        temp = clone.copy()

        # 绘制当前 ROI 点和线
        for pt in current_roi:
            cv2.circle(temp, pt, 5, (0, 0, 255), -1)
        if len(current_roi) > 1:
            cv2.polylines(temp, [np.array(current_roi, np.int32)], False, (0, 255, 255), 2)

        # 绘制所有已完成的 ROI
        for roi in all_rois:
            cv2.polylines(temp, [np.array(roi, np.int32)], True, (0, 255, 0), 2)

        cv2.imshow("Draw Multiple ROIs", temp)
        key = cv2.waitKey(1)
        if key == 27:  # ESC键结束绘制
            drawing = False

    cv2.destroyWindow("Draw Multiple ROIs")
    return all_rois
