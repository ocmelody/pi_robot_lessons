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

def left():
        GPIO.output(LEFT_BACKWARD, GPIO.HIGH)
        GPIO.output(LEFT_FORWARD,  GPIO.LOW)
        leftmotorpwm.ChangeDutyCycle(100)

        GPIO.output(RIGHT_BACKWARD, GPIO.LOW)
        GPIO.output(RIGHT_FORWARD,  GPIO.HIGH)
        rightmotorpwm.ChangeDutyCycle(100)

def right():
        GPIO.output(LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(LEFT_FORWARD,  GPIO.HIGH)
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
def printscreen():
        # Print the motor speed just for interest
        os.system('clear')
        print("w/s: forward/backward")
        print("a/d: left/right")
        print("q: stops the motors")
        print("x: exit")

    # Infinite loop
    # The loop will not end until the user presses the
    # exit key 'X' or the program crashes...

    #class method can determine which key has been pressed
    # by the user on the keyboard.
def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
        finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def test():
      printscreen()
      while True:
    # Keyboard character retrieval method. This method will save
    # the pressed key into the variable char
	char = getch()
	
	# The car will drive forward when the "w" key is pressed
	if(char == "w"):
		forward()
		printscreen()
	
    	# The car will reverse when the "s" key is pressed
	if(char == "s"):
		backward()
		printscreen()

	# Stop the motors
	if(char == "q"):
		stop()
		printscreen()

        # The "d" key will toggle the steering right
	if(char == "d"):		
		right()
		printscreen()

        # The "a" key will toggle the steering left
	if(char == "a"):
		left()
		printscreen()

	if(char == "q"):
		stop()
		printscreen()
		
	# The "x" key will break the loop and exit the program
	if(char == "x"):
		break
	
        # The keyboard character variable char has to be set blank. We need
	# to set it blank to save the next key pressed by the user
	char = ""

printscreen()
test()
stop()
# End
