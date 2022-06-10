/* 
 * rosserial Subscriber Example
 * Blinks an LED on callback
 */

#include <ros.h>
#include <std_msgs/String.h>
#include <Servo.h>A

Servo servoAngulo;
Servo servoDistancia;
Servo servoPinza;

int incomingByte = 0;
int angulo1 = 90;
int angulo2 = 0;
int angulo3 = 0;
int vel = 3;

String current_msg = "N";

ros::NodeHandle  nh;                   

void messageCb( const std_msgs::String& toggle_msg){
  current_msg = toggle_msg.data;
  if (current_msg == "R"){                                                                                                                                
    //R: Sumar angulo
    angulo1 -=vel;
    servoAngulo.write(angulo1);
  }else if(current_msg == "F"){
    //F:Restar angulo
    angulo1 +=vel;
    servoAngulo.write(angulo1);
  }else if(current_msg == "T"){
    //T:Sumar distancia
    angulo2 +=vel;
    servoDistancia.write(angulo2);
  }else if(current_msg == "G"){
    //G:Restar distancia
    angulo2 -=vel;
    servoDistancia.write(angulo2);
  }else if(current_msg == "Y"){
    //Y:Sumar pinza
    angulo3 +=vel;
    servoPinza.write(angulo3);
  }else if(current_msg == "H"){
    //H:Restar pinza
    angulo3 -=vel;
    servoPinza.write(angulo3);
  }
}

ros::Subscriber<std_msgs::String> sub("Manipulator_Velocidad", &messageCb );

void setup()
{ 
  servoAngulo.attach(9);
  servoDistancia.attach(10);
  servoPinza.attach(11);
  
  servoAngulo.write(angulo1);
  servoDistancia.write(angulo2);
  servoPinza.write(angulo3);
  nh.initNode();
  nh.subscribe(sub);
}

void loop()
{  
  nh.spinOnce();
  delay(1);
}

