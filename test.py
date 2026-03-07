from ultralytics import YOLO

# 1. 加载你训练好的模型 (注意路径，runs文件夹是自动生成的)
# 这里的路径可能需要根据实际生成的文件夹修改，比如 runs/detect/train2/...
model = YOLO(r'C:\Users\rosmo\Desktop\Project\CONTEST\model_02.2\runs\detect\train2\weights\best.pt')

# 2. 进行预测
# source 可以是图片路径、视频路径，甚至填 '0' 调用摄像头
results = model.predict(source=r'C:\Users\rosmo\Desktop\Project\CONTEST\model_02.2\runs\test_image\1.jpg', show=True, save=True, conf=0.3)

print("预测完成！结果保存在 runs/detect/predict 文件夹中")