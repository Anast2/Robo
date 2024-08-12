from setuptools import setup

package_name = 'facial_expression'

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
    description="Facial Expression Control Module",
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ["face_expression_server = facial_expression.face_expression_server:main"
        ],
    },
)
