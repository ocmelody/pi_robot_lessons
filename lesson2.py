import RPi.GPIO as GPIO
import sys, tty, termios, os
import time

#Raspberry GPIO PIN for car control
#use GPIO 2, 3 for left motors direction control , 4 for power control
LEFT_FORWARD = 2
LEFT_BACKWARD= 3
LEFT_PWM = 4

#use GPIO 27, 17 for right motors direction control , 18 for power control
RIGHT_FORWARD = 27
RIGHT_BACKWARD= 17
RIGHT_PWM = 18

#left motor speed initial value
speedleft = 0 

#right  motor speed initial value
speedright = 0 

#power for motor ranges from 0 to 100, 0 is stop, 100 is maximum
PWM_MAX = 100


def forward():
        GPIO.output(LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(LEFT_FORWARD,  GPIO.HIGH)
        leftmotorpwm.ChangeDutyCycle(100)

        GPIO.output(RIGHT_BACKWARD, GPIO.LOW)
        GPIO.output(RIGHT_FORWARD,  GPIO.HIGH)
        rightmotorpwm.ChangeDutyCycle(100)

def backward():
        GPIO.output(LEFT_BACKWARD, GPIO.HIGH)
        GPIO.output(LEFT_FORWARD,  GPIO.LOW)
        leftmotorpwm.ChangeDutyCycle(100)

        GPIO.output(RIGHT_BACKWARD, GPIO.HIGH)
        GPIO.output(RIGHT_FORWARD,  GPIO.LOW)
        rightmotorpwm.ChangeDutyCycle(100)

def stop():
        GPIO.output(LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(LEFT_FORWARD,  GPIO.LOW)
        GPIO.output(RIGHT_BACKWARD, GPIO.LOW)
        GPIO.output(RIGHT_FORWARD,  GPIO.LOW)
        leftmotorpwm.ChangeDutyCycle(0)
        rightmotorpwm.ChangeDutyCycle(0)

#initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_FORWARD, GPIO.OUT)
GPIO.setup(LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(LEFT_PWM, GPIO.OUT)
GPIO.setup(RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(RIGHT_BACKWARD, GPIO.OUT)
GPIO.setup(RIGHT_PWM, GPIO.OUT)
leftmotorpwm = GPIO.PWM(LEFT_PWM,100)
rightmotorpwm = GPIO.PWM(RIGHT_PWM,100)
leftmotorpwm.start(0)
leftmotorpwm.ChangeDutyCycle(0)
rightmotorpwm.start(0)
rightmotorpwm.ChangeDutyCycle(0)


#my test starts here
backward()
time.sleep(1)
stop()
# End
