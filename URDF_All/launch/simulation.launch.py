from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import FindExecutable, PathJoinSubstitution, Command
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_name = FindPackageShare("pkg_name")

    # Path to the robot.xacro file
    xacro_file = PathJoinSubstitution([pkg_name, "urdf", "robot.xacro"])

    # Generate robot_description from xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            xacro_file,
        ]
    )

    robot_description = {"robot_description": robot_description_content}

    return LaunchDescription(
        [
            # Control node (placeholder - you can replace with actual control node later)
            # Node(
            #     package="your_control_pkg",
            #     executable="your_control_node",
            #     name="control_node",
            #     output="screen",
            # ),

            # Load Gazebo world
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [
                            FindPackageShare("gazebo_ros"),
                            "launch",
                            "gazebo.launch.py",
                        ]
                    )
                ),
                launch_arguments={
                    "world": PathJoinSubstitution(
                        [pkg_name, "worlds", "four_walls.world"]
                    ),
                    "paused": "false",
                    "use_sim_time": "true",
                    "gui": "true",
                    "headless": "false",
                    "debug": "false",
                }.items(),
            ),

            # Robot State Publisher node
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[robot_description],
            ),

            # Spawn robot in Gazebo
            Node(
                package="gazebo_ros",
                executable="spawn_entity.py",
                arguments=[
                    "-topic", "robot_description",
                    "-entity", "my_robot"
                ],
                output="screen",
            ),
        ]
    )
