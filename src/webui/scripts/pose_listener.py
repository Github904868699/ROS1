#!/usr/bin/env python3
"""Subscribe to target_pose topics and execute motions with MoveIt."""

import rospy
from geometry_msgs.msg import PoseStamped
import moveit_commander


class PoseListener:
    def __init__(self):
        moveit_commander.roscpp_initialize([])
        group_name = rospy.get_param('~move_group', 'arm')
        try:
            self.group = moveit_commander.MoveGroupCommander(group_name)
        except RuntimeError as exc:
            rospy.logfatal("Planning group '%s' not found: %s", group_name, exc)
            raise
        rospy.Subscriber('/target_pose', PoseStamped, self._cb)
        rospy.Subscriber('/gazebo/target_pose', PoseStamped, self._cb)

    def _cb(self, msg: PoseStamped):
        self.group.set_pose_target(msg.pose)
        self.group.go(wait=True)
        self.group.stop()
        self.group.clear_pose_targets()


def main():
    rospy.init_node('pose_listener')
    listener = PoseListener()
    rospy.spin()
    moveit_commander.roscpp_shutdown()


if __name__ == '__main__':
    main()
