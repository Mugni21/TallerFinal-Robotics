#!/usr/bin/env python3

import rospy
from pynput.keyboard import Key, Listener
from std_msgs.msg import String

# globals
current_msg = "N"

estado_msg = "neutral"

#speed = 0
#angular = 0

# define key press event callback
def on_press(key):
    global estado_msg
    global current_msg
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if (k == "w"):
        current_msg = "W"
        estado_msg = "Arriba"
    elif (k == "s"):
        current_msg = "S"
        estado_msg = "Abajo"
    elif (k == "a"):
        current_msg = "A"
        estado_msg = "Izquierda"
    elif (k == "d"):
        current_msg = "D"
        estado_msg = "Derecha"

# define key release event callback
def on_release(key):
    global estado_msg
    global current_msg

    current_msg = "N"

    estado_msg = "neutral"


# main section
if __name__ == "__main__":
    # setup ros publisher
    pub = rospy.Publisher('Flash_Velocidad', String, queue_size=10) # name of topic: /trutlebot
    rospy.init_node('Flash_cmdVel', anonymous=True) # name of node: /keyboard_input

    #pub2 = rospy.Publisher('turtlebot_comando', String, queue_size=10)

    rate = rospy.Rate(10) # publish messages at 10Hz

    #print("Let's move your robot")
    #speed = float(input("Input your linear speed:"))
    #angular = float(input("Input your angular speed:"))

    # setup keyboard listener
    listener = Listener(on_press=on_press, on_release=on_release, suppress=False)
    listener.start()

    # MAIN LOOP
    # endlessly react on keyboard events and send appropriate messages
    while listener.running and not rospy.is_shutdown():
        rospy.loginfo(estado_msg)
        pub.publish(current_msg)
        #pub2.publish(current_msg)
        rate.sleep()
