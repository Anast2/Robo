from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'maestro_langgraph'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=[
        'setuptools',
        'langchain>=0.1',
        'langgraph>=0.0.30',
        'langchain-community>=0.0.20',
        'langchain-ollama>=0.0.1',
    ],
    zip_safe=True,
    maintainer='Tomasz Koczar',
    maintainer_email='tomasz@example.com',
    description='LangGraph-based dialogue system for ROOTED robot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'maestro_langgraph_node = maestro_langgraph.maestro_node:main',
        ],
    },
)
