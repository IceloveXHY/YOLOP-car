import uuid
from django.conf import settings
from django.db.models.expressions import result
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import torch
import os
from app01.code.drowsy_driving.drowsy_driving import drowsy_driving_solve
from app01.code.lane_markings.tools.demo import lane_detection
from app01.code.throws.testbest import throws_solve


def index(request):
    return HttpResponse("这是首页内容")


# 疲劳驾驶处理
@csrf_exempt
def drowsy_driving(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        if video_file:
            # 确保 input_video 目录存在
            input_video_path = os.path.join(settings.MEDIA_ROOT, 'input_video', 'drowsy_driving')
            if not os.path.exists(input_video_path):
                os.makedirs(input_video_path)
            # 生成新的文件路径
            input_video_path = os.path.join(input_video_path, video_file.name)
            # 保存文件到输入文件夹
            with open(input_video_path, 'wb') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            # 输出处理之后的目录
            output_video_path = os.path.join(settings.MEDIA_ROOT, 'output_video', 'drowsy_driving')
            if not os.path.exists(output_video_path):
                os.makedirs(output_video_path)
            # 生成新的文件路径
            output_video_path = os.path.join(output_video_path, video_file.name)
            # 处理调用函数
            result_data=drowsy_driving_solve(input_video_path, output_video_path)
            # 构建前端可访问的文件路径
            relative_path = os.path.relpath(output_video_path, settings.MEDIA_ROOT)
            accessible_path = settings.MEDIA_URL + relative_path
            print(input_video_path)
            print(accessible_path)
            # 安全统计计算（关键修改点3）
            dangerous_actions = sum(
                1 for item in result_data
                if item.get('class') in {'close_eyes','open_mouth', 'looking_away'}  # 使用正确的键名
            )
            return JsonResponse({
                'status': 'success',
                'output_url': accessible_path,
                'analysis': {
                    'total_events': len(result_data),
                    'dangerous_actions': dangerous_actions,
                    'details': result_data[:20]  # 返回前20条记录防止数据过大
                }
            })
        return JsonResponse({'error': 'No video file provided'}, status=400)
    elif request.method == 'GET':
        # 添加对 GET 请求的处理逻辑
        return JsonResponse({'error': 'GET method is not allowed for this endpoint. Please use POST method.'},
                            status=405)
    elif request.method == 'OPTIONS':
        # 处理 OPTIONS 预检请求
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'  # 注意：生产环境中不要使用 '*'，应指定具体的源
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response


# 车道线生成
@csrf_exempt
def lane_markings(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        if video_file:
            # 确保 input_video 目录存在
            input_video_path = os.path.join(settings.MEDIA_ROOT, 'input_video', 'lane_markings')
            if not os.path.exists(input_video_path):
                os.makedirs(input_video_path)
            # 生成新的文件路径
            input_video_path = os.path.join(input_video_path, video_file.name)
            # 保存文件到输入文件夹
            with open(input_video_path, 'wb') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            # 输出处理之后的目录
            output_video_path = os.path.join(settings.MEDIA_ROOT, 'output_video', 'lane_markings')
            if not os.path.exists(output_video_path):
                os.makedirs(output_video_path)
            # 生成新的文件路径
            output_video_path = os.path.join(output_video_path, video_file.name)
            # 处理调用函数
            lane_detection(
                source=input_video_path,
                save_dir=os.path.dirname(output_video_path),
                device='cpu'
            )
            # 构建前端可访问的文件路径
            relative_path = os.path.relpath(output_video_path, settings.MEDIA_ROOT)
            accessible_path = settings.MEDIA_URL + relative_path
            print(input_video_path)
            print(accessible_path)
            return JsonResponse({
                'message': 'Video saved successfully',
                'output_video_path': accessible_path
            })
        return JsonResponse({'error': 'No video file provided'}, status=400)
    elif request.method == 'GET':
        # 添加对 GET 请求的处理逻辑
        return JsonResponse({'error': 'GET method is not allowed for this endpoint. Please use POST method.'},
                            status=405)
    elif request.method == 'OPTIONS':
        # 处理 OPTIONS 预检请求
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'  # 注意：生产环境中不要使用 '*'，应指定具体的源
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response


#车辆违停
@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        # 生成唯一任务ID（UUID4格式字符串）
        task_id = str(uuid.uuid4())
        # 定义上传目录（项目根目录下的uploads文件夹）
        upload_dir = 'uploads'
        # 自动创建目录（如果不存在）
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        # 获取上传的视频文件（前端表单字段名需为'video'）
        file = request.FILES.get('video')
        if not file:
            # （可选：添加文件不存在的错误处理）
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        # 拼接文件保存路径（任务ID作为文件名，确保唯一性）
        file_path = os.path.join(upload_dir, f'{task_id}.mp4')
        # 分块写入文件（支持大文件上传）
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():  # 按块读取文件内容（默认块大小为2.5MB）
                f.write(chunk)
        # 返回任务ID给前端，用于后续WebSocket连接标识当前任务
        return JsonResponse({'task_id': task_id})
        # 处理非POST请求（如GET、PUT等）
    return JsonResponse({'error': 'Invalid method'}, status=405)
# 抛洒物
@csrf_exempt
def throws(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        if video_file:
            # 确保 input_video 目录存在
            input_video_path = os.path.join(settings.MEDIA_ROOT, 'input_video', 'throws')
            if not os.path.exists(input_video_path):
                os.makedirs(input_video_path)
            # 生成新的文件路径
            input_video_path = os.path.join(input_video_path, video_file.name)
            # 保存文件到输入文件夹
            with open(input_video_path, 'wb') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            # 输出处理之后的目录
            output_video_path = os.path.join(settings.MEDIA_ROOT, 'output_video', 'throws')
            if not os.path.exists(output_video_path):
                os.makedirs(output_video_path)
            # 生成新的文件路径
            output_video_path = os.path.join(output_video_path, video_file.name)
            # 处理调用函数
            result_data=throws_solve(input_video_path, output_video_path)
            # 构建前端可访问的文件路径
            relative_path = os.path.relpath(output_video_path, settings.MEDIA_ROOT)
            accessible_path = settings.MEDIA_URL + relative_path
            # 安全统计计算（关键修改点3）
            dangerous_actions = sum(
                1 for item in result_data
                if item.get('class') in {
                    0: 'Bottle',
                    1: 'Scattered debris',
                    2: 'Soft_plastics',
                    3: 'cardboard_boxes',
                    4: 'rock',
                    5: 'small items'
                 }  # 使用正确的键名
            )
            print(input_video_path)
            print(accessible_path)
            return JsonResponse({
                    'status': 'success',
                    'output_url': accessible_path,
                    'analysis': {
                        'total_events': len(result_data),
                        'dangerous_actions': dangerous_actions,
                        'details': result_data
                    }
                }
            )
        return JsonResponse({'error': 'No video file provided'}, status=400)
    elif request.method == 'GET':
        # 添加对 GET 请求的处理逻辑
        return JsonResponse({'error': 'GET method is not allowed for this endpoint. Please use POST method.'},
                            status=405)
    elif request.method == 'OPTIONS':
        # 处理 OPTIONS 预检请求
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'  # 注意：生产环境中不要使用 '*'，应指定具体的源
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
