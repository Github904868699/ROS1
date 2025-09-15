#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from flask import Flask, request, redirect

app = Flask(__name__)

real_pub = None
sim_pub = None

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
        '<h2>Gazebo</h2>'
        '<form action="/move/sim" method="post">'
        '<button name="action" value="forward">Forward</button>'
        '<button name="action" value="back">Back</button>'
        '<button name="action" value="left">Left</button>'
        '<button name="action" value="right">Right</button>'
        '<button name="action" value="stop">Stop</button>'
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

def main():
    global real_pub, sim_pub
    rospy.init_node('webui_node')
    real_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    sim_pub = rospy.Publisher('/gazebo/cmd_vel', Twist, queue_size=1)
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()
