from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import xbox
import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x6f)

FrontLeft = mh.getMotor(1)
FrontRight = mh.getMotor(2)
RearLeft = mh.getMotor(3)
RearRight = mh.getMotor(4)

joy = xbox.Joystick()
Wheels = [FrontLeft,FrontRight,RearLeft,RearRight]

turnThreshold = 100 #Turn Sensitivity
GasThreshold = 50 #Gas Sensitivity

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)


def stick2speed(y):
    return int(255*y)

def moveMotor(speeds,turn):
    i = 0
    for w in Wheels:
        spd = speeds[i]
        # print spd
        if  spd < 0:
            direction = Adafruit_MotorHAT.BACKWARD
        else:
            direction = Adafruit_MotorHAT.FORWARD
        if turn == True:
            direction = Adafruit_MotorHAT.FORWARD
        w.run(direction)
        w.setSpeed(abs(spd))
        i=i+1


atexit.register(turnOffMotors)

# # set the speed to start, from 0 (off) to 255 (max speed)
# myMotor.setSpeed(150)
# myMotor.run(Adafruit_MotorHAT.FORWARD);
# # turn on motor
# myMotor.run(Adafruit_MotorHAT.RELEASE);

while not joy.Back():
    lx, ly = joy.leftStick()
    rx, ry = joy.rightStick()
    speed = stick2speed(ly)
    turn = stick2speed(rx)
    # print "Left ", speed, "|  Right ", turn, "\r"
    if speed < GasThreshold and turn < turnThreshold:  #if sticks are not moving , shut off motors
        turnOffMotors()
    if (abs(speed) > GasThreshold) and (turn < turnThreshold):
       # print "Left ", speed, "|  Right ", turn ,"\r"
        moveMotor([speed,speed,speed,speed], False)
    if abs(turn) > turnThreshold:
       # print "Left ", speed, "|  Right ", turn, "\r"
        if turn > 0:
            moveMotor([turn,0,turn,0],True)
        else:
            moveMotor([0,turn,0,turn],True)
    time.sleep(0.1)

joy.close()
