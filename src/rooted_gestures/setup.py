from setuptools import setup

package_name = 'plantroid_gestures'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'plantroid_encoder', 'plantroid_neck'],
    zip_safe=True,
    maintainer='Antonio Galiza Cerdeira Gonzalez',
    maintainer_email='antonio@mizuuchi.lab.tuat.ac.jp',
    description='Packahe responsible for implementing the body language commands of the Plantroid robot, such as rotating the boddy  clock and cunter-clockwise when it says no, or shaking its head up and down when saying yes.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ["gesture_server = plantroid_gestures.GestureServer:main"
        ],
    },
)
