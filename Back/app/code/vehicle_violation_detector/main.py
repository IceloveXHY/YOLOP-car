import sys
import os

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将父目录（包含 detector 和 utils 目录的路径）加入系统路径
sys.path.append(os.path.join(current_dir, ".."))  # 假设 detector 与 main.py 同级或上级
import cv2
import yaml
from app01.code.vehicle_violation_detector.detector.yolo_detector import YOLODetector
from app01.code.vehicle_violation_detector.detector.roi_selector import select_roi
from app01.code.vehicle_violation_detector.detector.tracker import VehicleTracker
from app01.code.vehicle_violation_detector.detector.violation_logic import ViolationDetector
from app01.code.vehicle_violation_detector.utils.logger import ViolationLogger
from app01.code.vehicle_violation_detector.utils.video_writer import VideoWriter
from app01.code.vehicle_violation_detector.utils.roi_io import save_rois, load_rois
def load_config(path: str) -> dict:
    """加载配置文件"""
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def init_detection_components(config: dict, roi_path: str):
    """初始化检测组件"""
    rois = load_rois(roi_path)
    model = YOLODetector(
        config['model']['path'],
        config['model']['target_classes']
    )
    tracker = VehicleTracker(max_distance=config['max_tracking_distance'])
    violator = ViolationDetector(
        fps=config['fps'],
        threshold=config['violation_threshold_sec'],
        rois=rois
    )
    logger = ViolationLogger(
        config['log_path'],
        config['output_dir']
    )
    return model, tracker, violator, logger

def process_single_frame(frame: cv2.Mat, frame_idx: int, model, tracker, violator, logger):
    """处理单帧：检测→跟踪→违规判断"""
    detections = model.detect(frame)
    tracked = tracker.update(detections)
    return violator.process(frame, tracked, frame_idx, logger)