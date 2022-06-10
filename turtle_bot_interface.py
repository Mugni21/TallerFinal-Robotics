#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

#global
plt.style.use('fivethirtyeight')

x_values = []
y_values = []
x_current = 0
y_current = 0
vel_linear = 0
vel_angular = 0
decision = ""

def animate(i):
    global x_values
    global y_values

    x_values.append(x_current)
    y_values.append(y_current)
    plt.cla()
    plt.scatter(x_values, y_values,label= "Turtlebot", color= "red",marker= "o", s=30)
    plt.xlim(-2.5,2.5)
    plt.ylim(-2.5,2.5)
    plt.xlabel("Posicion en x")
    plt.ylabel("Posicion en y")
    plt.title("Trayectoria del Robot")
    plt.legend()
    plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
    plt.grid(True)

    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.rcParams["axes.edgecolor"] = "black"
    plt.rcParams["axes.linewidth"] = 2.50

def callback(vel_msg):
    global x_current
    global y_current

    x_current = vel_msg.linear.x
    y_current = vel_msg.linear.y

def velocidades(current_speed):
    global vel_linear
    global vel_angular
    
    if current_speed.linear.x != 0:
        vel_linear = current_speed.linear.x
    if current_speed.angular.z != 0:
        vel_angular = current_speed.angular.z

    

def callback2(current_msg):
    global decision
    if ((decision == "S")|(decision == "s")): 
        f.write(str(current_msg)+"\r\n")      
            

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    
    rospy.Subscriber("turtlebot_cmdVel", Twist, velocidades)

    rospy.Subscriber("turtlebot_position", Twist, callback)

    rospy.Subscriber("turtlebot_comando", String, callback2)

    

    

    ani = FuncAnimation(plt.gcf(), animate, 1000)

    plt.tight_layout()
    plt.show()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    decision = input("Desea guardar la ruta (S/n):")

    if ((decision == "S")|(decision == "s")):
        name = str(input("Input the name of the file: "))
        f= open("/home/robotica/Robotica_ws/src/turtle_bot_15/results/"+name,"w+")
        
        
    
    listener()

    if ((decision == "S")|(decision == "s")):
        a = open("/home/robotica/Robotica_ws/src/turtle_bot_15/results/"+ name, 'a')
        a.writelines(str(abs(vel_linear))+"\n" + str(abs(vel_angular)) + "\n")  


if ((decision == "S")|(decision == "s")):
    f.close()

