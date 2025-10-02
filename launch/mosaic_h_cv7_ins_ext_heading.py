import os

import ament_index_python

from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch_ros.actions import Node

_PACKAGE_NAME = 'modular_ins'

# Path to the launch files and directories that we will use
_MICROSTRAIN_LAUNCH_FILE = os.path.join(ament_index_python.packages.get_package_share_directory('microstrain_inertial_driver'), 'launch', 'microstrain_launch.py')
_CV7_INS_PARAMS_FILE = os.path.join(ament_index_python.packages.get_package_share_directory('modular_ins'), 'config', 'mosaic_h_cv7_ins_ext_heading.yml')
_RVIZ_DISPLAY_FILE = os.path.join(ament_index_python.packages.get_package_share_directory('modular_ins'), 'config', 'display.rviz')
_CONFIG_DIRECTORY = os.path.join(ament_index_python.packages.get_package_share_directory('modular_ins'), 'config')
_SEPT_CONFIG_FILE = os.path.join(_CONFIG_DIRECTORY, 'mosaic_h_cv7_ins_ext_heading.yml') 
_RTK_PARAMS_FILE = os.path.join(_CONFIG_DIRECTORY, 'rtk_params.yml')

def generate_launch_description():
  print(f"sept params: {_SEPT_CONFIG_FILE}")
  return LaunchDescription([
    # Microstrain node
    IncludeLaunchDescription(
      PythonLaunchDescriptionSource(_MICROSTRAIN_LAUNCH_FILE),
      launch_arguments={
        'configure': 'true',
        'activate': 'true',
        'params_file': _CV7_INS_PARAMS_FILE,
        'namespace': 'modular_ins', #need to verify
	        'debug': 'false',
      }.items()
    ),
    
    # Septentrio Mosaic H node
    Node(
      package='septentrio_gnss_driver',
      executable='septentrio_gnss_driver_node',
      output='screen',
      # parameters=[_SEPT_CONFIG_FILE],
      parameters=[_SEPT_CONFIG_FILE, _RTK_PARAMS_FILE],
      namespace='modular_ins',
      remappings=[
        ('navsatfix','/modular_ins/ext/llh_position'),
        ('twist_gnss','/modular_ins/ext/velocity_enu'),
        ('pose','/modular_ins/ext/heading_enu')
        # ('navsatfix','/modular_ins/ext/llh_position'),
        # ('twist_gnss','/modular_ins/ext/velocity_ned'),
        # ('pose','/modular_ins/ext/heading_ned')
      ]
    ),

    # Publish a static transform for where the GNSS antenna is mounted on base_link.
    # You should replace this with actual transforms for where your aiding sensors are
    # Node(
    #   package='tf2_ros',
    #   executable='static_transform_publisher',
    #   output='screen',
    #   arguments=[
    #       "--x", "0.00",
    #       "--y", "0.00",
    #       "--z", "0.00",
    #       "--roll", "0",
    #       "--pitch", "0",
    #       "--yaw", "0",
    #       "--frame-id", "base_link",
    #       "--child-frame-id", "gnss"
    #     ]
    # ),

    # # Publish a static transform for where the CV7-INS is mounted on base_link.
    # # Unless the CV7-INS is mounted exactly at base_link, you should change this to be accurate to your setup
    # Node(
    #   package='tf2_ros',
    #   executable='static_transform_publisher',
    #   output='screen',
    #   arguments=[
    #       "--x", "0.00",
    #       "--y", "0.00",
    #       "--z", "0.00",
    #       "--roll", "0",
    #       "--pitch", "0",
    #       "--yaw", "0",
    #       "--frame-id", "base_link",
    #       "--child-frame-id", "cv7_ins_link"
    #     ]
    # ),

    # Publish mock information from a fake sensor to the CV7-INS
    # ExecuteProcess(
    #   cmd=[
    #     "ros2", "topic", "pub", "/modular_ins/ext/llh_position", "sensor_msgs/msg/NavSatFix",
    #       f'''
    #       header:
    #         stamp: 'now'
    #         frame_id: 'gnss'
    #       status:
    #         status: 0
    #         service: 0
    #       latitude: 44.4373567456773
    #       longitude: -73.10625770609381
    #       altitude: 126.0
    #       position_covariance:
    #       - 0.78
    #       - 0.0
    #       - 0.0
    #       - 0.0
    #       - 0.78
    #       - 0.0
    #       - 0.0
    #       - 0.0
    #       - 0.78
    #       position_covariance_type: 1
    #       '''
    #   ],
    # ),
    # ExecuteProcess(
    #   cmd=[
    #     "ros2", "topic", "pub", "/modular_ins/ext/velocity_enu", "geometry_msgs/msg/TwistWithCovarianceStamped",
    #       f'''
    #         header:
    #           stamp: 'now'
    #           frame_id: 'gnss'
    #         twist:
    #           twist:
    #             linear:
    #               x: 0.0
    #               y: 0.0
    #               z: 0.0
    #             angular:
    #               x: 0.0
    #               y: 0.0
    #               z: 0.0
    #           covariance:
    #           - 0.01
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.01
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.01
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #           - 0.0
    #       '''
    #   ],
    # ),


# # from radar node 

    # Publish a static transform for where the our gps is mounted on base_link.
    Node(
      package='tf2_ros',
      executable='static_transform_publisher',
      output='screen',
      arguments=[
          "--x", "0.15",
          "--y", "-0.45",
          "--z", "1.58",
          "--roll", "0",
          "--pitch", "0",
          "--yaw", "0",
          "--frame-id", "base_link",
          "--child-frame-id", "gnss"
        ]
    ),

    # Publish a static transform for where the CV7-INS is mounted on base_link.
    # Unless the CV7-INS is mounted exactly at base_link, you should change this to be accurate to your setup
    Node(
      package='tf2_ros',
      executable='static_transform_publisher',
      output='screen',
      arguments=[
          "--x", "-0.37",
          "--y", "-0.55",
          "--z", "0.63",
          "--roll", "0",
          "--pitch", "0",
          "--yaw", "0",
          "--frame-id", "base_link",
          "--child-frame-id", "cv7_ins_link"
        ]
    ),

    # Run rviz to view the state of the application
    Node(
      package='rviz2',
      executable='rviz2',
      output='screen',
      arguments=[
        '-d', _RVIZ_DISPLAY_FILE
      ]
    ),
  ])