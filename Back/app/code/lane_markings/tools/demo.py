import argparse
import os, sys
import shutil
import time
from pathlib import Path
import imageio
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import scipy.special
import numpy as np
import torchvision.transforms as transforms
import PIL.Image as image

from app01.code.lane_markings.lib.config import cfg
from app01.code.lane_markings.lib.config import update_config
from app01.code.lane_markings.lib.utils.utils import create_logger, select_device, time_synchronized
from app01.code.lane_markings.lib.models import get_net
from app01.code.lane_markings.lib.dataset import LoadImages, LoadStreams
from app01.code.lane_markings.lib.core.general import non_max_suppression, scale_coords
from app01.code.lane_markings.lib.utils import plot_one_box,show_seg_result
from app01.code.lane_markings.lib.core.function import AverageMeter
from app01.code.lane_markings.lib.core.postprocess import morphological_process, connect_lane
from tqdm import tqdm

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到系统路径中
sys.path.append(BASE_DIR)

print(sys.path)


# 图像归一化处理
normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
)

# 图像预处理步骤
transform = transforms.Compose([
    transforms.ToTensor(),
    normalize,
])


def detect(cfg, opt):
    # 创建日志记录器
    logger, _, _ = create_logger(
        cfg, cfg.LOG_DIR, 'demo')

    # 选择设备（cpu或GPU）
    device = select_device(logger, opt.device)
    # 如果保存结果的目录存在，则删除它
    if os.path.exists(opt.save_dir):
        shutil.rmtree(opt.save_dir)
    # 创建新的保存结果的目录
    os.makedirs(opt.save_dir)

    # 是否使用半精度（仅在cpu设备上支持）
    half = device.type!= 'cpu'

    # 加载模型
    model = get_net(cfg)
    # 加载模型权重
    checkpoint = torch.load(opt.weights, map_location=device)
    model.load_state_dict(checkpoint['state_dict'])
    model = model.to(device)
    if half:
        model.half()  # 转换为半精度

    # 设置数据加载器
    if opt.source.isnumeric():
        cudnn.benchmark = True
        dataset = LoadStreams(opt.source, img_size=opt.img_size)
        bs = len(dataset)
    else:
        dataset = LoadImages(opt.source, img_size=opt.img_size)
        bs = 1

    # 获取类别名称和颜色
    names = model.module.names if hasattr(model,'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

    # 记录开始时间
    t0 = time.time()

    vid_path, vid_writer = None, None
    # 创建一个全零的图像张量，用于初始化模型
    img = torch.zeros((1, 3, opt.img_size, opt.img_size), device=device)
    _ = model(img.half() if half else img) if device.type!= 'cpu' else None
    model.eval()

    # 初始化推理时间和NMS时间的平均记录器
    inf_time = AverageMeter()
    nms_time = AverageMeter()

    # 遍历数据集中的每一个样本
    for i, (path, img, img_det, vid_cap, shapes) in tqdm(enumerate(dataset), total=len(dataset)):
        img = transform(img).to(device)
        img = img.half() if half else img.float()
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        # 前向推理
        t1 = time_synchronized()
        det_out, da_seg_out, ll_seg_out = model(img)
        t2 = time_synchronized()
        inf_out, _ = det_out
        # 更新推理时间
        inf_time.update(t2 - t1, img.size(0))

        # 应用非极大值抑制
        t3 = time_synchronized()
        det_pred = non_max_suppression(inf_out, conf_thres=opt.conf_thres, iou_thres=opt.iou_thres, classes=None,
                                       agnostic=False)
        t4 = time_synchronized()

        # 更新NMS时间
        nms_time.update(t4 - t3, img.size(0))
        det = det_pred[0]

        # 构建保存路径
        save_path = str(opt.save_dir + '/' + Path(path).name) if dataset.mode!= 'stream' else str(
            opt.save_dir + '/' + "web.mp4")

        _, _, height, width = img.shape
        h, w, _ = img_det.shape
        pad_w, pad_h = shapes[1][1]
        pad_w = int(pad_w)
        pad_h = int(pad_h)
        ratio = shapes[1][0][1]

        # 对分割结果进行处理
        da_predict = da_seg_out[:, :, pad_h:(height - pad_h), pad_w:(width - pad_w)]
        da_seg_mask = torch.nn.functional.interpolate(da_predict, scale_factor=int(1 / ratio), mode='bilinear')
        _, da_seg_mask = torch.max(da_seg_mask, 1)
        da_seg_mask = da_seg_mask.int().squeeze().cpu().numpy()
        # da_seg_mask = morphological_process(da_seg_mask, kernel_size=7)

        ll_predict = ll_seg_out[:, :, pad_h:(height - pad_h), pad_w:(width - pad_w)]
        ll_seg_mask = torch.nn.functional.interpolate(ll_predict, scale_factor=int(1 / ratio), mode='bilinear')
        _, ll_seg_mask = torch.max(ll_seg_mask, 1)
        ll_seg_mask = ll_seg_mask.int().squeeze().cpu().numpy()
        # Lane line post-processing
        # ll_seg_mask = morphological_process(ll_seg_mask, kernel_size=7, func_type=cv2.MORPH_OPEN)
        # ll_seg_mask = connect_lane(ll_seg_mask)

        img_det = show_seg_result(img_det, (da_seg_mask, ll_seg_mask), _, _, is_demo=True)

        if len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img_det.shape).round()
            for *xyxy, conf, cls in reversed(det):
                label_det_pred = f'{names[int(cls)]} {conf:.2f}'
                plot_one_box(xyxy, img_det, label=label_det_pred, color=colors[int(cls)], line_thickness=2)

        if dataset.mode == 'images':
            cv2.imwrite(save_path, img_det)

        elif dataset.mode == 'video':
            if vid_path!= save_path:
                vid_path = save_path
                if isinstance(vid_writer, cv2.VideoWriter):
                    vid_writer.release()

                fourcc = 'avc1'
                fps = vid_cap.get(cv2.CAP_PROP_FPS)
                h, w, _ = img_det.shape
                vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
            vid_writer.write(img_det)

        else:
            cv2.imshow('image', img_det)
            cv2.waitKey(1)

    print('Results saved to %s' % Path(opt.save_dir))
    print('Done. (%.3fs)' % (time.time() - t0))
    print('inf : (%.4fs/frame)   nms : (%.4fs/frame)' % (inf_time.avg, nms_time.avg))

def lane_detection(
    weights = r"E:\Code\YOLOP-car\Back\app01\code\lane_markings\weights\End-to-end.pth",
    source = r"E:\Code\YOLOP-car\Back\app01\media\input_video\lane_markings",
    save_dir = r"E:\Code\YOLOP-car\Back\app01\media\output_video\lane_markings",
    device='cpu',
    img_size=640
):
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=weights, help='model.pth path(s)')
    parser.add_argument('--source', type=str, default=source, help='source')
    parser.add_argument('--img-size', type=int, default=img_size, help='inference size (pixels)')  # 修正此处
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default=device, help='cpu device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--save-dir', type=str, default=save_dir, help='directory to save results')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    opt = parser.parse_args(args=[])

    with torch.no_grad():
        detect(cfg, opt)


if __name__ == '__main__':
    lane_detection()