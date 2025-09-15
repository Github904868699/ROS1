#!/usr/bin/env python3
"""Simple Flask interface with buttons to move in x/y/z.

The previous version used HTML forms and redirected back to the index
page after every click.  Some browsers reported a timeout when waiting
for the redirect, so the interface now uses a small piece of
JavaScript to send POST requests in the background.  Each button press
therefore returns immediately and the page no longer reloads."""

import rospy
from geometry_msgs.msg import PoseStamped
from flask import Flask, request

app = Flask(__name__)

# Publishers for real robot and Gazebo
real_pose_pub = None
sim_pose_pub = None

# Current poses so each button press offsets from the last command
real_pose = PoseStamped()
real_pose.pose.orientation.w = 1.0
real_pose.header.frame_id = "world"
sim_pose = PoseStamped()
sim_pose.pose.orientation.w = 1.0
sim_pose.header.frame_id = "world"


@app.route('/')
def index():
    """Serve a minimal page with buttons that trigger JS fetch calls."""
    return (
        '<h1>Robot Control</h1>'
        '<h2>Real Robot</h2>'
        '<button onclick="step(\'real\',\'x+\')">X+</button>'
        '<button onclick="step(\'real\',\'x-\')">X-</button>'
        '<button onclick="step(\'real\',\'y+\')">Y+</button>'
        '<button onclick="step(\'real\',\'y-\')">Y-</button>'
        '<button onclick="step(\'real\',\'z+\')">Z+</button>'
        '<button onclick="step(\'real\',\'z-\')">Z-</button>'
        '<h2>Gazebo</h2>'
        '<button onclick="step(\'sim\',\'x+\')">X+</button>'
        '<button onclick="step(\'sim\',\'x-\')">X-</button>'
        '<button onclick="step(\'sim\',\'y+\')">Y+</button>'
        '<button onclick="step(\'sim\',\'y-\')">Y-</button>'
        '<button onclick="step(\'sim\',\'z+\')">Z+</button>'
        '<button onclick="step(\'sim\',\'z-\')">Z-</button>'
        '<script>'
        'function step(target, axis){fetch("/step/"+target,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({axis:axis})});}'
        '</script>'
    )


@app.route('/step/<target>', methods=['POST'])
def step(target):
    data = request.get_json(silent=True) or {}
    axis = data.get('axis', '')
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
    return "ok"


def main():
    global real_pose_pub, sim_pose_pub
    rospy.init_node('webui_node')
    real_pose_pub = rospy.Publisher('/target_pose', PoseStamped, queue_size=1)
    sim_pose_pub = rospy.Publisher('/gazebo/target_pose', PoseStamped, queue_size=1)
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)


if __name__ == '__main__':
    main()

