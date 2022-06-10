#!/usr/bin/env python3


import rospy
#from geometry_msgs.msg import Twist 
from std_msgs.msg import String
from turtle_bot_15.srv import reproducir_partida, reproducir_partidaResponse

# globals

current_msg = ""
speed = 0
angular = 0
contador = 0
content = 0

def move():
    global current_msg
    global vel_msg
    global content
    global contador
    global speed
    global angular

    k = content[contador]

    if ("W" in k):
        current_msg = "W"
    elif ("S" in k):
        current_msg = "S"
    elif ("A" in k):
        current_msg = "A"
    elif ("D" in k):
        current_msg = "D"
    elif ("N" in k):
        current_msg = "N"

def handle_reproducir_partida(req):
    global current_msg
    global vel_msg
    global content
    global contador
    global speed
    global angular
    pub = rospy.Publisher('Flash_Velocidad', String, queue_size=10) # name of topic: /trutlebot
    nombre_archivo = req.nombre_archivo

    rate = rospy.Rate(10) # publish messages at 10Hz

    file1 = open("/home/ubuntu/catkin_ws/src/turtle_bot_15/results/"+nombre_archivo, 'r')
    content = file1.readlines()

    speed = float(content[-2][0:4])
    angular = float(content[-1][0:4])

    content = content[:-2]
    iteraciones = len(content)
    print(iteraciones)

        # MAIN LOOP
    while not rospy.is_shutdown():
        for i in range(iteraciones):
            move()
            rospy.loginfo(current_msg)
            pub.publish(current_msg)

            contador += 1

            rate.sleep()
        break

    return reproducir_partidaResponse("Secuencia de acciones finalizada")

def reproducir_partida_server():
    rospy.init_node('flashbot_player')
    s = rospy.Service('reproducir_partida', reproducir_partida, handle_reproducir_partida)
    print("Listo para reproducir secuencia de acciones")
    rospy.spin()

if __name__ == "__main__":
    reproducir_partida_server()
