import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/jetson/yahboomcar_ws/src/yahboom_M3Pro_DepthCam/install/yahboom_M3Pro_DepthCam'
