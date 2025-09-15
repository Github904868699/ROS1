#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist, PoseStamped
from flask import Flask, request, redirect
from tf.transformations import quaternion_from_euler

app = Flask(__name__)

real_pub = None
sim_pub = None
real_pose_pub = None
sim_pose_pub = None

@app.route('/')
def index():
    return (
        '<h1>Robot Control</h1>'
        '<h2>Real Robot</h2>'
        '<form action="/move/real" method="post">'
        '<button name="action" value="forward">Forward</button>'
        '<button name="action" value="back">Back</button>'
        '<button name="action" value="left">Left</button>'
        '<button name="action" value="right">Right</button>'
        '<button name="action" value="stop">Stop</button>'
        '</form>'
        '<form action="/pose/real" method="post">'
        'X:<input name="x" type="number" step="0.01">'
        'Y:<input name="y" type="number" step="0.01">'
        'Z:<input name="z" type="number" step="0.01">'
        'Roll:<input name="roll" type="number" step="0.01">'
        'Pitch:<input name="pitch" type="number" step="0.01">'
        'Yaw:<input name="yaw" type="number" step="0.01">'
        '<button type="submit">Send Pose</button>'
        '</form>'
        '<h2>Gazebo</h2>'
        '<form action="/move/sim" method="post">'
        '<button name="action" value="forward">Forward</button>'
        '<button name="action" value="back">Back</button>'
        '<button name="action" value="left">Left</button>'
        '<button name="action" value="right">Right</button>'
        '<button name="action" value="stop">Stop</button>'
        '</form>'
        '<form action="/pose/sim" method="post">'
        'X:<input name="x" type="number" step="0.01">'
        'Y:<input name="y" type="number" step="0.01">'
        'Z:<input name="z" type="number" step="0.01">'
        'Roll:<input name="roll" type="number" step="0.01">'
        'Pitch:<input name="pitch" type="number" step="0.01">'
        'Yaw:<input name="yaw" type="number" step="0.01">'
        '<button type="submit">Send Pose</button>'
        '</form>'
    )

@app.route('/move/<target>', methods=['POST'])
def move(target):
    action = request.form.get('action', 'stop')
    twist = Twist()
    speed = 0.5
    turn = 1.0
    if action == 'forward':
        twist.linear.x = speed
    elif action == 'back':
        twist.linear.x = -speed
    elif action == 'left':
        twist.angular.z = turn
    elif action == 'right':
        twist.angular.z = -turn
    # else stop
    if target == 'real':
        real_pub.publish(twist)
    else:
        sim_pub.publish(twist)
    return redirect('/')


@app.route('/pose/<target>', methods=['POST'])
def pose(target):
    x = float(request.form.get('x', 0))
    y = float(request.form.get('y', 0))
    z = float(request.form.get('z', 0))
    roll = float(request.form.get('roll', 0))
    pitch = float(request.form.get('pitch', 0))
    yaw = float(request.form.get('yaw', 0))
    qx, qy, qz, qw = quaternion_from_euler(roll, pitch, yaw)
    msg = PoseStamped()
    msg.header.stamp = rospy.Time.now()
    msg.pose.position.x = x
    msg.pose.position.y = y
    msg.pose.position.z = z
    msg.pose.orientation.x = qx
    msg.pose.orientation.y = qy
    msg.pose.orientation.z = qz
    msg.pose.orientation.w = qw
    if target == 'real':
        real_pose_pub.publish(msg)
    else:
        sim_pose_pub.publish(msg)
    return redirect('/')

def main():
    global real_pub, sim_pub, real_pose_pub, sim_pose_pub
    rospy.init_node('webui_node')
    real_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    sim_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    real_pose_pub = rospy.Publisher('/target_pose', PoseStamped, queue_size=1)
    sim_pose_pub = rospy.Publisher('/gazebo/target_pose', PoseStamped, queue_size=1)
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()
