import pyrealsense2 as rs
import numpy as np
import cv2

# 初始化管道和配置
pipeline = rs.pipeline()
config = rs.config()

# 安全配置（兼容性优先）
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 15)  # 左红外
config.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 15)  # 右红外

try:
    # 启动管道
    pipeline.start(config)
    print("摄像头已成功启动！")

    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        # 获取各帧数据
        # ir1_frame = frames.get_infrared_frame(1)
        # ir2_frame = frames.get_infrared_frame(2)
        # #转换为可显示格式
        # ir1_image = cv2.convertScaleAbs(np.asanyarray(ir1_frame.get_data()), alpha=1.0)
        # ir2_image = cv2.convertScaleAbs(np.asanyarray(ir2_frame.get_data()), alpha=1.0)    

        if not color_frame or not depth_frame:
            continue
                         
        # 转换为 numpy 数组
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # 显示图像
        cv2.imshow('RGB', color_image)
        cv2.imshow('Depth', cv2.convertScaleAbs(depth_image, alpha=0.03))
        # cv2.imshow('IR Left', ir1_image)
        # cv2.imshow('IR Right', ir2_image)

        if cv2.waitKey(1) == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()