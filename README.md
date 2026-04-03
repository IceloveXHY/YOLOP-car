YOLOP-car
面向车载场景的轻量化多任务感知模型
项目简介
YOLOP-car 是基于 YOLOP 改进的自动驾驶多任务视觉感知模型，专为车载实时场景设计。模型可在一次前向推理中同时完成：
- 车辆、行人等交通目标检测
- 可行驶区域分割
- 车道线检测
实现精度与速度的均衡，适用于智能驾驶、辅助驾驶系统等实际部署场景。
主要特性
- 端到端多任务学习，共享主干网络，推理高效
- 轻量化结构，适合嵌入式端与车载平台实时运行
- 在 BDD100K 等自动驾驶数据集上表现优异
- 训练、测试、部署流程简洁，易于二次开发
环境配置
- Python 3.8+
- PyTorch 1.8+
- torchvision
- opencv-python
- numpy、tqdm、Pillow 等
运行命令
git clone https://github.com/yourname/YOLOP-car.git
cd YOLOP-car
pip install -r requirements.txt
数据集准备
本项目默认支持 BDD100K 自动驾驶数据集。
1. 下载数据集并解压
2. 按 data/ 目录结构组织图片与标签
3. 修改配置文件中的数据集路径
模型训练
单卡训练示例：
python train.py --config configs/yolop_car.yaml
多卡分布式训练：
python -m torch.distributed.launch train.py --dist
模型测试与推理
