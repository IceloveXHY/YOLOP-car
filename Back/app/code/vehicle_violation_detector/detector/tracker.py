
import numpy as np
from app01.code.vehicle_violation_detector.utils.common import get_center

class VehicleTracker:
    def __init__(self, max_distance):
        self.max_distance = max_distance
        self.next_id = 0
        self.vehicles = {}

    def update(self, detections):
        updated = []
        for box, cls in detections:
            center = get_center(box)
            matched_id = None
            for vid, info in self.vehicles.items():
                if np.linalg.norm(np.array(center) - np.array(info['center'])) < self.max_distance:
                    matched_id = vid
                    break
            if matched_id is None:
                matched_id = self.next_id
                self.next_id += 1
            self.vehicles[matched_id] = {'center': center}
            updated.append((matched_id, box))
        return updated
