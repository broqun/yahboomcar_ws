from setuptools import find_packages, setup

package_name = 'learning_time'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'rate_demo=learning_time.rate_demo:main',
            'timer_demo=learning_time.timer_demo:main',
            'get_clock_demo=learning_time.get_clock_demo:main',
            'time_duration_demo=learning_time.time_duration_demo:main'
        ],
    },
)
