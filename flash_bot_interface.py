#!/usr/bin/env python3
import rospy
#from geometry_msgs.msg import Twist
from std_msgs.msg import String
import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import numpy as np

#global
plt.style.use('fivethirtyeight')

x_values = []
y_values = []
theta_values=[]
x_current = 0
y_current = 0
theta_current=0
#vel_linear = 0
#vel_angular = 0
decision = ""

x1_values = []
y1_values = []
theta1_values=[]
x1_current = 0
y1_current = 25
theta1_current=0



def animate(i):
    global x_values
    global y_values
    
    global x1_values
    global y1_values

    x_values.append(x_current)
    y_values.append(y_current)
    x1_values.append(x1_current)
    y1_values.append(y1_current)
    
    plt.cla()
    plt.scatter(x_values, y_values,label= "Flash bot", color= "red",marker= "o", s=30)
    plt.scatter(x1_values, y1_values,label= "Brazo", color= "black",marker= "+", s=15)
    plt.xlim(-100,100)
    plt.ylim(-100,100)
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
    global theta_current
    
    #print(str(vel_msg.data))
    x_current = float(str(vel_msg.data).split(":")[0])
    y_current = float(str(vel_msg.data).split(":")[1])
    theta_current = float(str(vel_msg.data).split(":")[2])

    #def velocidades(current_speed):
    #global vel_linear
    #global vel_angular
    
    #if current_speed.linear.x != 0:
        #vel_linear = current_speed.linear.x
    #if current_speed.angular.z != 0:
        #vel_angular = current_speed.angular.z

    

def callback2(current_msg):
    global decision
    if ((decision == "S")|(decision == "s")): 
        f.write(str(current_msg)+"\r\n")    
        
def callback3(arm_vel_msg):
    global x1_current
    global y1_current
    global theta1_current
    
    #print(str(vel_msg.data))
    x1_current = float(str(arm_vel_msg.data).split(":")[0])
    y1_current = float(str(arm_vel_msg.data).split(":")[1])
    theta1_current=float(str(arm_vel_msg.data).split(":")[2])
    
   
    #rospy.loginfo(arm_vel_msg)        

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    
    #rospy.Subscriber("turtlebot_cmdVel", Twist, velocidades)

    rospy.Subscriber('Flash_bot_position', String, callback)

    rospy.Subscriber("Flash_Velocidad", String, callback2)
    
    rospy.Subscriber('Manipulator_position',String,callback3)

    ani = FuncAnimation(plt.gcf(), animate, 1000)

    plt.tight_layout()
    plt.show()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    decision = input("Desea guardar la ruta (S/n):")

    if ((decision == "S")|(decision == "s")):
        name = str(input("Input the name of the file: "))
        f= open("/home/ubuntu/catkin_ws/src/turtle_bot_15/results/"+name,"w+")

    listener()

    if ((decision == "S")|(decision == "s")):
        a = open("/home/ubuntu/catkin_ws/src/turtle_bot_15/results/"+ name, 'a')
        a.writelines(str(10)+"\n" + str(10) + "\n")  


if ((decision == "S")|(decision == "s")):
    f.close()

