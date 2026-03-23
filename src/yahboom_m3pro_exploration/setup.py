from glob import glob
import os

from setuptools import find_packages, setup


package_name = 'yahboom_m3pro_exploration'


setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.py'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='broqun',
    maintainer_email='broqun@yahoo.com',
    description='Autonomous exploration scaffolding for Yahboom M3Pro SLAM demos.',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'frontier_explorer = yahboom_m3pro_exploration.frontier_explorer:main',
        ],
    },
)
