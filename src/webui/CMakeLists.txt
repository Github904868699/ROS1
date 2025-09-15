cmake_minimum_required(VERSION 3.0.2)
project(webui)

find_package(catkin REQUIRED COMPONENTS rospy geometry_msgs)

catkin_package()

catkin_install_python(PROGRAMS scripts/webui_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
