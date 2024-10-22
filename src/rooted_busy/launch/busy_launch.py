def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rooted_busy',
            executable='busy_server',
            name='busy_server_node',
            output='screen',
            emulate_tty=True,
            parameters=[
                {}
            ]
        )
    ])
