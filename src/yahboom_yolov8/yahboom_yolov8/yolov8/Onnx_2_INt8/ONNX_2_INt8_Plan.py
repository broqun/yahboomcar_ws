import os
import sys
import numpy as np
from cuda import cudart
import tensorrt as trt
import calibrator

print(trt.__version__)

onnxFile = "../weights/yolov8s.onnx"
trtFile = "../weights/yolov8s.trt"
calibrationDataPath = "../coco128-images"  # 校准数据集路径
cacheFile = "int8.cache"
imageHeight = 640
imageWidth = 640

# os.system("rm -rf ./*.pt ./*.onnx ./*.plan ./*.cache")
np.set_printoptions(precision=4, linewidth=200, suppress=True)
cudart.cudaDeviceSynchronize()

# TensorRT 中加载 .onnx 创建 engine ----------------------------------------------
logger = trt.Logger(trt.Logger.INFO)
if os.path.isfile(trtFile):
    with open(trtFile, 'rb') as f:
        engine = trt.Runtime(logger).deserialize_cuda_engine(f.read())
    if engine == None:
        print("Failed loading engine!")
        exit()
    print("Succeeded loading engine!")
else:
    builder = trt.Builder(logger)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    profile = builder.create_optimization_profile()
    config = builder.create_builder_config()
    config.flags = 1 << int(trt.BuilderFlag.INT8)
    config.int8_calibrator = calibrator.MyEntropyCalibrator(calibrationDataPath,
                                                            (4, 3, imageHeight, imageWidth),
                                                            cacheFile)  # 调用定义的校准器，并设置输入Tensor维度
    #config.max_workspace_size_bytes = 3 << 30
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 3 << 30)
    parser = trt.OnnxParser(network, logger)
    if not os.path.exists(onnxFile):
        print("Failed finding onnx file!")
        exit()
    print("Succeeded finding onnx file!")
    with open(onnxFile, 'rb') as model:
        if not parser.parse(model.read()):
            print("Failed parsing .onnx file!")
            for error in range(parser.num_errors):
                print(parser.get_error(error))
            exit()
        print("Succeeded parsing .onnx file!")

    inputTensor = network.get_input(0)
    profile.set_shape(inputTensor.name, (4, 3, 640, 640), (4, 3, 640, 640), (4, 3, 640, 640))
    config.add_optimization_profile(profile)

    engineString = builder.build_serialized_network(network, config)
    if engineString == None:
        print("Failed building engine!")
        exit()
    print("Succeeded building engine!")
    with open(trtFile, 'wb') as f:
        f.write(engineString)
