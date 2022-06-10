#!/usr/bin/env python3

import rospy
import numpy as np

from std_msgs.msg import String

current_msg = ""
position_msg = ""
x = 0
y = 0
theta =0

rw=3.0
l=22.5

phi_r = 2.75*np.pi
phi_l = 2.75*np.pi

V_r=0
V_l=0

dt = 0.1 #10Hz


#Datos brazo
x1=0
y1=25
long=25
theta1=0
current_msg2=''
position_msg2=''
phi_bra=0.55*np.pi
r_bra=1.2
V_bra=0


# setup ros publisher
pub = rospy.Publisher('Flash_bot_position', String, queue_size=10) # name of topic: /trutlebot
pub2 =rospy.Publisher('Manipulator_position',String,queue_size=10)


def callback(data):
    global current_msg
    global position_msg
    global x
    global y
    global theta
    global V_r
    global V_l
    #print("entro 1")
    current_msg = data.data
    #print("el mensaje es"+current_msg)
    
    if current_msg == "W":
        V_r = rw*phi_r
        V_l = rw*phi_l
    elif current_msg == "A":
        V_r = rw*phi_r
        V_l = 0
    elif current_msg == "S":
        V_r = -rw*phi_r
        V_l = -rw*phi_l
    elif current_msg == "D":
        V_r = 0
        V_l = rw*phi_l
    elif current_msg == "N":
        V_r = 0
        V_l = 0
    
    x = ( x + 0.5*(V_r+V_l)*np.cos(theta)*dt)
    y = ( y + 0.5*(V_r+V_l)*np.sin(theta)*dt)
    theta = (theta + (1/l)*(V_r-V_l)*dt)
    
    position_msg = str(x)+":"+str(y)+":"+ str(theta)
    pub.publish(position_msg)
    
def callback2(data2):
    global current_msg2
    global position_msg2
    
    global x1
    global y1
    global theta1
    global phi_bra
    global r_bra
    global long
    current_msg2=data2.data
    
    global x
    global y
    global theta
    
    
    if current_msg2 == "R":
        theta1=theta1+(np.pi/180)
        x1=abs(long)*np.cos(theta1)
        y1=abs(long)*np.sin(theta1)
   
    elif current_msg2 == "F":
        theta1=theta1-(np.pi/180)
        x1=abs(long)*np.cos(theta1)
        y1=abs(long)*np.sin(theta1)
        
    elif current_msg2 == "T":
        long=long+phi_bra*r_bra*dt
        x1=abs(long)*np.cos(theta1)
        y1=abs(long)*np.sin(theta1)
      
    elif current_msg2 == "G":
        long=long-phi_bra*r_bra*dt
        x1=abs(long)*np.cos(theta1)
        y1=abs(long)*np.sin(theta1)
        
    
    elif current_msg2 == "N":
        V_bra=0
    
    M=np.matrix([[np.cos(theta),-np.sin(theta),x],[np.sin(theta),np.cos(theta),y],[0,0,1]])	
    
    
    Posloc=np.matrix([ [x1], [y1], [1]])
    
    Global=M*Posloc
    
    x1_global = Global[0,0]
    y1_global = Global[1,0]
    theta1_current= theta1
  
    position_msg2=str(x1_global)+":"+str(y1_global)+":"+ str(theta1)
    pub2.publish(position_msg2)
  
def listener():
    
    
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('Lectura_pos', anonymous=True)

    rospy.Subscriber("Flash_Velocidad", String, callback)
    
    rospy.Subscriber('Manipulator_Velocidad',String, callback2)
    
    # setup ros publisher
    #pub = rospy.Publisher('Flash_bot_position', String, queue_size=10) # name of topic: /trutlebot
    
    #rate = rospy.Rate(10) # publish messages at 10Hz
    
    # spin() simply keeps python from exiting until this node is stopped
    
    
    #rospy.loginfo(str(x)+", "+str(y))
    
    
    rospy.spin()
        

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
