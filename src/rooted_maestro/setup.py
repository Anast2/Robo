from setuptools import setup

package_name = 'plantroid_social'

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
    description='Package responsible for managing the social interfaces of plantroid, reciving data from the listen server, using the chatbot and GPTJ interfaces and prosody generation packages to genrate responses.',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ["social_manager = plantroid_social.SocialManager:main"
        ],
    },
)
