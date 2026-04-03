import cv2
from ultralytics import YOLO

def throws_solve(input_video_path, output_video_path):
    # 初始化结果数组
    detection_results = []

    # 定义模型路径和类别名称
    model_path = 'app01/code/throws/best.pt'
    class_names = {
        0: 'Bottle',
        1: 'Scattered debris',
        2: 'Soft_plastics',
        3: 'cardboard_boxes',
        4: 'rock',
        5: 'small items'
    }

    # 加载YOLO模型
    model = YOLO(model_path)

    # 打开视频文件
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise IOError("无法打开视频文件")

    # 获取视频参数
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 设置跳帧参数（每2帧处理1帧）
    frame_skip = 2
    out_fps = fps // frame_skip

    # 创建视频写入对象
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_video_path, fourcc, out_fps, (width, height))

    frame_num = 0
    processed_frames = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 跳帧处理
            if frame_num % frame_skip != 0:
                frame_num += 1
                continue

            # 执行目标检测
            results = model(frame)

            # 处理检测结果并绘制框
            for result in results:
                for box in result.boxes:
                    if box.conf < 0.5:  # 置信度阈值
                        continue

                    # 获取检测框坐标和类别
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls = int(box.cls)
                    conf = float(box.conf)

                    # 在帧上绘制检测框和标签
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f'{class_names[cls]} {conf:.2f}'
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    timestamp = frame_num / fps  # 计算准确时间戳
                    # 将结果添加到数组
                    detection_results.append({
                        'time_sec': round(timestamp, 1),  # 当前帧号
                        'class': class_names[cls],
                        'confidence': conf,
                        "bbox": (x1, y1, x2 - x1, y2 - y1)  # (x,y,w,h)
                    })

            # 写入处理后的帧
            out.write(frame)
            processed_frames += 1
            frame_num += 1

            # 打印处理进度
            print(f"已处理 {processed_frames}/{total_frames//frame_skip} 帧...")

    finally:
        # 释放资源
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    # 返回检测结果数组
    return detection_results