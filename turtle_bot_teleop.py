#!/usr/bin/env python3

import rospy
from pynput.keyboard import Key, Listener
from geometry_msgs.msg import Twist
from std_msgs.msg import String

# globals
vel_msg = Twist()
vel_msg.linear.x = 0
vel_msg.linear.y = 0
vel_msg.linear.z = 0
vel_msg.angular.x = 0
vel_msg.angular.y = 0
vel_msg.angular.z = 0

current_msg = "neutral"
speed = 0
angular = 0

# define key press event callback
def on_press(key):
    global vel_msg
    global current_msg
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if (k == "w"):
        vel_msg.linear.x = speed
        vel_msg.angular.z = 0
        current_msg = "Arriba"
    elif (k == "s"):
        vel_msg.linear.x = -speed
        vel_msg.angular.z = 0
        current_msg = "Abajo"
    elif (k == "a"):
        vel_msg.angular.z = angular
        vel_msg.linear.x = 0
        current_msg = "Izquierda"
    elif (k == "d"):
        vel_msg.angular.z = -angular
        vel_msg.linear.x = 0
        current_msg = "Derecha"

# define key release event callback
def on_release(key):
    global vel_msg
    global current_msg

    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    current_msg = "neutral"


# main section
if __name__ == "__main__":
    # setup ros publisher
    pub = rospy.Publisher('turtlebot_cmdVel', Twist, queue_size=10) # name of topic: /trutlebot
    rospy.init_node('teleop_cmd', anonymous=True) # name of node: /keyboard_input

    pub2 = rospy.Publisher('turtlebot_comando', String, queue_size=10)

    rate = rospy.Rate(10) # publish messages at 10Hz

    print("Let's move your robot")
    speed = float(input("Input your linear speed:"))
    angular = float(input("Input your angular speed:"))

    # setup keyboard listener
    listener = Listener(on_press=on_press, on_release=on_release, suppress=False)
    listener.start()

    # MAIN LOOP
    # endlessly react on keyboard events and send appropriate messages
    while listener.running and not rospy.is_shutdown():
        rospy.loginfo(current_msg)
        pub.publish(vel_msg)
        pub2.publish(current_msg)
        rate.sleep()
