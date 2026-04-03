import cv2
from ultralytics import YOLO

def drowsy_driving_solve(input_video_path, output_video_path):
    # 模型配置
    model_path = 'app01/code/drowsy_driving/best.pt'
    class_names = {
        0: 'open_eyes',
        1: 'close_eyes',
        2: 'open_mouth',
        3: 'close_mouth',
        4: 'looking_away',
    }
    target_classes = {'close_eyes', 'open_mouth', 'looking_away'}

    # 初始化模型
    model = YOLO(model_path)

    # 打开视频文件
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise ValueError("无法打开视频文件")

    # 获取视频参数
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # 修正帧率获取方式
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 视频写入配置
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # 初始化结果存储
    result_data = []

    try:
        frame_num = 0       # 原始视频帧号
        processed_count = 0 # 已处理帧计数器

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 每5帧处理一次
            if frame_num % 5 == 0:
                # 执行目标检测
                results = model(frame)

                # 处理检测结果
                frame_results = []
                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cls = int(box.cls)
                        conf = float(box.conf)
                        class_name = class_names.get(cls, 'Unknown')

                        if class_name in target_classes and conf >= 0.5:
                            # 绘制检测结果
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            label = f'{class_name} {conf:.2f}'
                            cv2.putText(frame, label, (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                            # 记录检测结果
                            timestamp = frame_num / fps  # 计算准确时间戳
                            frame_results.append({
                                "time_sec": round(timestamp, 1),
                                "class": class_name,
                                "confidence": round(conf, 3),
                                "bbox": (x1, y1, x2 - x1, y2 - y1)  # (x,y,w,h)
                            })

                # 保存本帧结果
                if frame_results:
                    result_data.append({
                        "frame_number": frame_num,
                        "detections": frame_results
                    })

                # 写入处理后的帧
                out.write(frame)
                processed_count += 1
                print(f"已处理 {processed_count}/{(total_frames+4)//5} 帧...", end='\r')

            frame_num += 1  # 始终递增原始帧号

    finally:
        # 释放资源
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    return result_data