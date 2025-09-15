#!/usr/bin/env python3
"""Simple Flask interface with buttons to move in x/y/z."""

import rospy
from geometry_msgs.msg import PoseStamped
from flask import Flask, request, redirect

app = Flask(__name__)

# Publishers for real robot and Gazebo
real_pose_pub = None
sim_pose_pub = None

# Current poses so each button press offsets from the last command
real_pose = PoseStamped()
real_pose.pose.orientation.w = 1.0
sim_pose = PoseStamped()
sim_pose.pose.orientation.w = 1.0


@app.route('/')
def index():
    return (
        '<h1>Robot Control</h1>'
        '<h2>Real Robot</h2>'
        '<form action="/step/real" method="post">'
        '<button name="axis" value="x+">X+</button>'
        '<button name="axis" value="x-">X-</button>'
        '<button name="axis" value="y+">Y+</button>'
        '<button name="axis" value="y-">Y-</button>'
        '<button name="axis" value="z+">Z+</button>'
        '<button name="axis" value="z-">Z-</button>'
        '</form>'
        '<h2>Gazebo</h2>'
        '<form action="/step/sim" method="post">'
        '<button name="axis" value="x+">X+</button>'
        '<button name="axis" value="x-">X-</button>'
        '<button name="axis" value="y+">Y+</button>'
        '<button name="axis" value="y-">Y-</button>'
        '<button name="axis" value="z+">Z+</button>'
        '<button name="axis" value="z-">Z-</button>'
        '</form>'
    )


@app.route('/step/<target>', methods=['POST'])
def step(target):
    axis = request.form.get('axis', '')
    step = 0.1
    pose = real_pose if target == 'real' else sim_pose
    if axis == 'x+':
        pose.pose.position.x += step
    elif axis == 'x-':
        pose.pose.position.x -= step
    elif axis == 'y+':
        pose.pose.position.y += step
    elif axis == 'y-':
        pose.pose.position.y -= step
    elif axis == 'z+':
        pose.pose.position.z += step
    elif axis == 'z-':
        pose.pose.position.z -= step
    pose.header.stamp = rospy.Time.now()
    pub = real_pose_pub if target == 'real' else sim_pose_pub
    pub.publish(pose)
    return redirect('/')


def main():
    global real_pose_pub, sim_pose_pub
    rospy.init_node('webui_node')
    real_pose_pub = rospy.Publisher('/target_pose', PoseStamped, queue_size=1)
    sim_pose_pub = rospy.Publisher('/gazebo/target_pose', PoseStamped, queue_size=1)
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    main()

