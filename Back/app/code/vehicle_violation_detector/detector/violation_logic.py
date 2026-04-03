import cv2
import numpy as np
from app01.code.vehicle_violation_detector.utils.common import point_in_roi

class ViolationDetector:
    def __init__(self, fps, threshold, rois):
        """
        fps: 视频帧率
        threshold: 超过该秒数视为违规
        rois: 多个 ROI 区域，每个区域是点列表 [(x1,y1), (x2,y2), ...]
        """
        self.fps = fps
        self.threshold = threshold
        self.rois = rois  # 注意现在是多个多边形区域
        self.states = {}  # 每个车辆ID对应的状态
        self.violated = set()

    def process(self, frame, vehicles, frame_idx, logger):
        for vid, box in vehicles:
            center = ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2)

            if vid not in self.states:
                self.states[vid] = {'frames': 0, 'last_seen': frame_idx}

            # 判断是否在任意 ROI 内
            in_any_roi = any(point_in_roi(center, roi) for roi in self.rois)

            if in_any_roi:
                self.states[vid]['frames'] += 1
            else:
                self.states[vid]['frames'] = 0

            time_in_roi = self.states[vid]['frames'] / self.fps
            if time_in_roi > self.threshold:
                color = (0, 0, 255)
                label = f"ID:{vid} - {time_in_roi:.1f}s 🚨"
                if vid not in self.violated:
                    self.violated.add(vid)
                    logger.log_violation(frame, vid, frame_idx, box, time_in_roi)
            else:
                color = (0, 255, 0)
                label = f"ID:{vid} - {time_in_roi:.1f}s"

            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
            cv2.putText(frame, label, (box[0], box[1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # 画出所有 ROI 区域
        for roi in self.rois:
            cv2.polylines(frame, [np.array(roi, np.int32)], True, (255, 0, 0), 2)

        return frame
