def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rooted_speech_synthesizer',
            executable='speech_synthesizer_service',
            name='speech_synthesizer_service_node',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'mode': 'local',
                 'model': 'espeak_ng',
                 'IP': '127.0.0.1',
                 'PORT': '5049',}
            ]
        )
    ])