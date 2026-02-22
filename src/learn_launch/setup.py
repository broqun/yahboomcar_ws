from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'learn_launch'

# 以 setup.py 所在目录为基准找到 launch 文件，再转为相对路径（colcon 要求 data_files 必须为相对路径）
# setup_dir = os.path.dirname(os.path.abspath(__file__))
# launch_files = [os.path.relpath(p, setup_dir) for p in glob(os.path.join(setup_dir, 'launch', '*launch.py'))]

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'),glob(os.path.join('launch','*launch.py')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='spen',
    maintainer_email='broqun@yahoo.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
