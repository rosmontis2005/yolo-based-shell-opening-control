from ultralytics import YOLO
from pathlib import Path

# ... 下面是你原本的 model = YOLO(...) 代码 ...
# 1. 加载模型
# yolov8n.pt 是纳米级模型，速度最快，精度一般，适合笔记本电脑或初学跑通流程
# 如果显卡好，可以换成 yolov8s.pt (小), yolov8m.pt (中)
model = YOLO('yolo26n.pt')

# 2. 开始训练
if __name__ == '__main__':
    project_root = Path(__file__).resolve().parent
    data_yaml = project_root / "data.yaml"

    # data: 指向你的配置文件
    # epochs: 训练轮数，初学可以设 50-100
    # imgsz: 图片大小，通常是 640
    # batch: 显存不够就调小，比如 8 或 4，显存大就 16 或 32
    # device: '0' 表示使用第一块 GPU，如果没有 GPU 则填 'cpu'
    model.train(data=str(data_yaml),
                epochs=500,
                imgsz=640,
                batch=8,
                workers=0,
                device=0) # Windows下workers设大容易报错，建议设0或2
