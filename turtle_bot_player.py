#!/usr/bin/env python3


import rospy
from geometry_msgs.msg import Twist 
from turtle_bot_15.srv import reproducir_partida, reproducir_partidaResponse

# globals
vel_msg = Twist()
vel_msg.linear.x = 0
vel_msg.linear.y = 0
vel_msg.linear.z = 0
vel_msg.angular.x = 0
vel_msg.angular.y = 0
vel_msg.angular.z = 0

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

    if ("Arriba" in k):
        vel_msg.linear.x = speed
        vel_msg.angular.z = 0
        current_msg = "Arriba"
    elif ("Abajo" in k):
        vel_msg.linear.x = -speed
        vel_msg.angular.z = 0
        current_msg = "Abajo"
    elif ("Izquierda" in k):
        vel_msg.angular.z = angular
        vel_msg.linear.x = 0
        current_msg = "Izquierda"
    elif ("Derecha" in k):
        vel_msg.angular.z = -angular
        vel_msg.linear.x = 0
        current_msg = "Derecha"
    elif ("neutral" in k):
        vel_msg.angular.z = 0
        vel_msg.linear.x = 0
        current_msg = "neutral"

def handle_reproducir_partida(req):
    global current_msg
    global vel_msg
    global content
    global contador
    global speed
    global angular
    pub = rospy.Publisher('turtlebot_cmdVel', Twist, queue_size=10) # name of topic: /trutlebot
    nombre_archivo = req.nombre_archivo

    rate = rospy.Rate(10) # publish messages at 10Hz

    file1 = open("/home/robotica/Robotica_ws/src/turtle_bot_15/results/"+nombre_archivo, 'r')
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
            pub.publish(vel_msg)

            contador += 1

            rate.sleep()
        break

    return reproducir_partidaResponse("Secuencia de acciones finalizada")

def reproducir_partida_server():
    rospy.init_node('turtlebot_player')
    s = rospy.Service('reproducir_partida', reproducir_partida, handle_reproducir_partida)
    print("Listo para reproducir secuencia de acciones")
    rospy.spin()

if __name__ == "__main__":
    reproducir_partida_server()
