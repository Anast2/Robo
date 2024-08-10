from setuptools import setup

package_name = 'plantroid_gui'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'kivy', 'beepy'],
    zip_safe=True,
    maintainer='Antonio Galiza Cerdeira Gonzalez',
    maintainer_email='antonio@mizuuchi.lab.tuat.ac.jp',
    description="Plantroid's emotion engine and face display package",
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ["gui = plantroid_gui.GUI_MEGA:main"
        ],
    },
)
