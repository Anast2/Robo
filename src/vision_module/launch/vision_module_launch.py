def generate_launch_description():
    return LaunchDescription([
        Node(
            package='vision_module',
            executable='vision_server',
            name='vision_module_node',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'identity_db': '/home/plantroid/plantroid_ws/src/robot_memory/db/people.db'}
            ]
        )
    ])