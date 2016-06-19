import RPi.GPIO as GPIO
import sys, tty, termios, os
import time

#Raspberry GPIO PIN for car control
LEFT_FORWARD = 2
LEFT_BACKWARD= 3
LEFT_PWM = 4
RIGHT_FORWARD = 27
RIGHT_BACKWARD= 17
RIGHT_PWM = 18

#global variables 
speedleft = 0 
speedright = 0 
PWM_MAX = 100
STEP = 0.2

# setMotorMode()
# Sets the mode for the L298 H-Bridge which motor is in which mode.
# This is a short explanation for a better understanding:
# motor         -> which motor is selected left motor or right motor
# mode          -> mode explains what action should be performed by the H-Bridge
# setMotorMode(leftmotor, reverse)      -> The left motor is called by a function and set into reverse mode
# setMotorMode(rightmotor, stopp)       -> The right motor is called by a function and set into stopp mode

def setMotorMode(motor, mode):
        if motor == "leftmotor":
                if mode == "reverse":
                        GPIO.output(LEFT_BACKWARD, GPIO.HIGH)
                        GPIO.output(LEFT_FORWARD,  GPIO.LOW)
                elif  mode == "forward":
                        GPIO.output(LEFT_BACKWARD, GPIO.LOW)
                        GPIO.output(LEFT_FORWARD,  GPIO.HIGH)
                else:
                        GPIO.output(LEFT_BACKWARD, GPIO.LOW)
                        GPIO.output(LEFT_FORWARD,  GPIO.LOW)

        elif motor == "rightmotor":
                if mode == "reverse":
                        GPIO.output(RIGHT_BACKWARD, GPIO.HIGH)
                        GPIO.output(RIGHT_FORWARD,  GPIO.LOW)
                elif  mode == "forward":
                        GPIO.output(RIGHT_BACKWARD, GPIO.LOW)
                        GPIO.output(RIGHT_FORWARD,  GPIO.HIGH)
                else:
                        GPIO.output(RIGHT_BACKWARD, GPIO.LOW)
                        GPIO.output(RIGHT_FORWARD,  GPIO.LOW)
        else:
        	GPIO.output(LEFT_FORWARD, GPIO.LOW)
        	GPIO.output(RIGHT_FORWARD, GPIO.LOW)
        	GPIO.output(LEFT_BACKWARD, GPIO.LOW)
        	GPIO.output(RIGHT_BACKWARD, GPIO.LOW)

# Sets the drive level for the left motor, from +1 (max) to -1 (min).
# This is a short explanation for a better understanding:
# SetMotorLeft(0)     -> left motor is stopped
# SetMotorLeft(0.75)  -> left motor moving forward at 75% power
# SetMotorLeft(-0.5)  -> left motor moving reverse at 50% power
# SetMotorLeft(1)     -> left motor moving forward at 100% power
def setMotorLeft(power):
        print "LEFT POWER=" + str(power)
        if power < 0:
                # Reverse mode for the left motor
                setMotorMode("leftmotor", "reverse")
                pwm = -int(PWM_MAX * power)
                if pwm > PWM_MAX:
                        pwm = PWM_MAX
        elif power > 0:
                # Forward mode for the left motor
                setMotorMode("leftmotor", "forward")
                pwm = int(PWM_MAX * power)
                if pwm > PWM_MAX:
                        pwm = PWM_MAX
        else:
                # Stopp mode for the left motor
                setMotorMode("leftmotor", "stopp")
                pwm = 0
        print "SetMotorLeft", pwm
        leftmotorpwm.ChangeDutyCycle(pwm)

# Sets the drive level for the right motor, from +1 (max) to -1 (min).
# This is a short explanation for a better understanding:
# SetMotorRight(0)     -> right motor is stopped
# SetMotorRight(0.75)  -> right motor moving forward at 75% power
# SetMotorRight(-0.5)  -> right motor moving reverse at 50% power
# SetMotorRight(1)     -> right motor moving forward at 100% power
def setMotorRight(power):
        print "RIGHT POWER=" + str(power)
        if power < 0:
                # Reverse mode for the right motor
                setMotorMode("rightmotor", "reverse")
                pwm = -int(PWM_MAX * power)
                if pwm > PWM_MAX:
                        pwm = PWM_MAX
        elif power > 0:
                # Forward mode for the right motor
                setMotorMode("rightmotor", "forward")
                pwm = int(PWM_MAX * power)
                if pwm > PWM_MAX:
                        pwm = PWM_MAX
        else:
                # Stopp mode for the right motor
                setMotorMode("rightmotor", "stopp")
                pwm = 0
        print "SetMotorRight", pwm
        rightmotorpwm.ChangeDutyCycle(pwm)

def close():
	setMotorLeft(0)
	setMotorRight(0)
        print "clean up"
        GPIO.cleanup()

def forward():
        global speedleft, speedright 
	# synchronize after a turning the motor speed
	# if speedleft > speedright:
		# speedleft = speedright
	
	# if speedright > speedleft:
		# speedright = speedleft
			
	# accelerate the RaPi car
	speedleft = speedleft + STEP
	speedright = speedright + STEP

	if speedleft > 1:
		speedleft = 1
	if speedright > 1:
		speedright = 1
	
	setMotorLeft(speedleft)
	setMotorRight(speedright)

def backward():
        global speedleft, speedright 
	# synchronize after a turning the motor speed
		
	# if speedleft > speedright:
		# speedleft = speedright
		
	# if speedright > speedleft:
		# speedright = speedleft
		
	# slow down the RaPi car
	speedleft = speedleft - STEP
	speedright = speedright - STEP

	if speedleft < -1:
		speedleft = -1
	if speedright < -1:
		speedright = -1
	
	setMotorLeft(speedleft)
	setMotorRight(speedright)

def stop():
	speedleft = 0
	speedright = 0
	setMotorLeft(speedleft)
	setMotorRight(speedright)

def right():
        global speedleft, speedright 
	#if speedright > speedleft:
	speedright = speedright - STEP
	speedleft = speedleft + STEP
	
	if speedright < -1:
		speedright = -1
	
	if speedleft > 1:
		speedleft = 1
	
	setMotorLeft(speedleft)
	setMotorRight(speedright)

def left():
        global speedleft, speedright 
	#if speedleft > speedright:
	speedleft = speedleft - STEP
	speedright = speedright + STEP
		
	if speedleft < -1:
		speedleft = -1
	
	if speedright > 1:
		speedright = 1
	
	setMotorLeft(speedleft)
	setMotorRight(speedright)

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

def printscreen():
        # Print the motor speed just for interest
        os.system('clear')
        print("w/s: direction")
        print("a/d: steering")
        print("q: stops the motors")
        print("x: exit")
        print("========== Speed Control ==========")
        print "left motor:  ", speedleft
        print "right motor: ", speedright

    # Infinite loop
    # The loop will not end until the user presses the
    # exit key 'X' or the program crashes...

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
		
	# The "x" key will break the loop and exit the program
	if(char == "x"):
		close()
		break
	
        # The keyboard character variable char has to be set blank. We need
	# to set it blank to save the next key pressed by the user
	char = ""


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
test()
# End
