from setuptools import setup

package_name = 'plantroid_sensors'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Antonio Galiza Cerdeira Gonzalez',
    maintainer_email='antonio@mizuuchi.lab.tuat.ac.jp',
    description='Package related to Plantroid sensors that are not vision related. It interfaces with the Arduino Nano inside the smart PlantPot and the NPK+EC+pH integrated soil sensor.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ["sensor_server = plantroid_sensors.SensorServer:main",
                            "fake_sensor_server = plantroid_sensors.FakeSensorServer:main"
        ],
    },
)
