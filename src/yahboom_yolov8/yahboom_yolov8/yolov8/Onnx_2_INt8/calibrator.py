import os
import cv2
import numpy as np
import glob
from cuda import cudart  # pip3 install cuda-python
import tensorrt as trt


class MyEntropyCalibrator(trt.IInt8EntropyCalibrator2):

    def __init__(self, imgs_dir, tensor_shape, cache_file):
        trt.IInt8EntropyCalibrator2.__init__(self)

        self.cache_file = cache_file
        self.batch_size, self.Channel, self.Height, self.Width = tensor_shape
        self.imgs = [os.path.join(imgs_dir,
                                  file_name) for file_name in os.listdir(imgs_dir) if file_name.lower().endswith((".jpg", ".bmp", ".png", ".jpeg"))]
        np.random.shuffle(self.imgs)
        self.batch_idx = 0
        self.max_batch_idx = len(self.imgs) // self.batch_size
        self.data_size = trt.volume([self.batch_size, self.Channel, self.Height, self.Width]) * trt.float32.itemsize
        # self.device_input = cuda.mem_alloc(self.data_size)
        _, self.dIn = cudart.cudaMalloc(self.data_size)
        # print(int(self.dIn))

    def next_batch(self):
        if self.batch_idx < self.max_batch_idx:
            batch_files = self.imgs[self.batch_idx * self.batch_size: (self.batch_idx + 1) * self.batch_size]
            batch_imgs = np.zeros((self.batch_size, self.Channel, self.Height, self.Width),
                                  dtype=np.float32)
            for i, f in enumerate(batch_files):
                img = cv2.imread(f)
                img = self.transform(img, (self.Height, self.Width))
                assert (img.nbytes == self.data_size / self.batch_size), 'not valid img!' + f
                batch_imgs[i] = img
            self.batch_idx += 1
            print("\rbatch:[{}/{}]".format(self.batch_idx, self.max_batch_idx), end='')
            return np.ascontiguousarray(batch_imgs)
        else:
            return np.array([])

    def transform(self, image, img_size):
        img_square = self.letterbox(image, img_size, auto=False, stride=32)[0]  # 将其变成640x640形式,上下填充灰边
        img = cv2.cvtColor(img_square, cv2.COLOR_BGR2RGB)
        img = img / 255.
        img = np.asarray(img, dtype=np.float32)
        img = img.transpose((2, 0, 1))
        return img

    @staticmethod
    def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better val mAP)
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
        elif scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return im, ratio, (dw, dh)

    def get_batch_size(self):
        return self.batch_size

    def get_batch(self, names, p_str=None):
        batch_imgs = self.next_batch()
        print(batch_imgs.shape)
        # print("okk")
        if batch_imgs.size == 0 or batch_imgs.size != self.batch_size * self.Channel * self.Height * self.Width:
            return None
        # cuda.memcpy_htod(self.device_input, batch_imgs.astype(np.float32))
        cudart.cudaMemcpy(self.dIn, batch_imgs.ctypes.data,
                          self.data_size, cudart.cudaMemcpyKind.cudaMemcpyHostToDevice)
        # return [int(self.device_input)]
        return [int(self.dIn)]

    def read_calibration_cache(self):
        # If there is a cache, use it instead of calibrating again. Otherwise, implicitly return None.
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "rb") as f:
                return f.read()

    def write_calibration_cache(self, cache):
        with open(self.cache_file, "wb") as f:
            f.write(cache)


if __name__ == "__main__":
    cudart.cudaDeviceSynchronize()

    m = MyEntropyCalibrator("../0000/", (1, 1, 270, 540), "int8.cache")
    result = m.get_batch("FakeNameList")
    print(result)
