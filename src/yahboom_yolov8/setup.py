from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'yahboom_yolov8'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'),glob(os.path.join('launch','*.py*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jetson',
    maintainer_email='jetson@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'yolov8_detect = yahboom_yolov8.yolov8_detect:main',
        'yolov8_track = yahboom_yolov8.yolov8_track:main'
        ],
    },
)
