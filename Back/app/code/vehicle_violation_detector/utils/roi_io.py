#保存和加载多个ROI
import yaml

def save_rois(rois, path):
    """保存多个 ROI 到 yaml 文件"""
    # 确保所有的元组被转为列表
    rois_as_list = [[list(roi) for roi in group] for group in rois]
    with open(path, 'w') as f:
        yaml.dump({'rois': rois_as_list}, f, default_flow_style=False)


def load_rois(path):
    """从 yaml 文件中加载多个 ROI"""
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
        return data.get('rois', [])
