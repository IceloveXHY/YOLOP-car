import os
import cv2
import base64
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
# 按照项目结构调整导入路径
from app01.code.vehicle_violation_detector.main import load_config, init_detection_components, process_single_frame

class VideoProcessingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        await self.accept()

        # 加载配置与初始化组件
        config_path = "app01/code/vehicle_violation_detector/config/config.yaml"
        self.config = load_config(config_path)
        roi_path = self.config['roi_path']
        self.model, self.tracker, self.violator, self.logger = init_detection_components(
            self.config, roi_path
        )

        # 初始化视频捕获
        self.video_path = os.path.join('uploads', f'{self.task_id}.mp4')
        self.cap = cv2.VideoCapture(self.video_path)
        self.frame_idx = 0

        # 启动处理任务
        self.processing_task = asyncio.create_task(self.process_video())

    async def process_video(self):
        """视频处理主循环"""
        while self.cap.isOpened():
            # 异步读取视频帧
            ret, frame = await asyncio.to_thread(self.cap.read)
            if not ret:
                break

            # 调用检测逻辑处理单帧
            processed_frame = process_single_frame(
                frame, self.frame_idx, self.model, self.tracker, self.violator, self.logger
            )
            if processed_frame is None:
                continue

            # 编码并发送帧
            _, buffer = cv2.imencode('.jpg', processed_frame)
            base64_frame = base64.b64encode(buffer).decode('utf-8')
            # 添加图片格式前缀
            base64_frame_with_prefix = f"data:image/jpg;base64,{base64_frame}"
            await self.send(text_data=base64_frame_with_prefix)

            self.frame_idx += 1
            await asyncio.sleep(0.03)  # 控制帧率

        # 释放资源
        self.cap.release()
        self.logger.close()

    async def disconnect(self, close_code):
        """连接断开时取消任务"""
        if hasattr(self, 'processing_task') and not self.processing_task.done():
            self.processing_task.cancel()