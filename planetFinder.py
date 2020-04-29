from RPLCD.gpio import CharLCD
import time
import RPi.GPIO as GPIO
from astroquery.jplhorizons import Horizons

count = 0
stepperPinsAZ = [7,11,13,15]
stepperPinsEL = [40, 38, 36, 32]
selectBtnPin = 33
incBtnPin = 37
decBtnPin = 35
mars = 499
planets = [199, 299, 301, 499, 599, 699, 799, 899, 999]
planetNames = ["Mercury", "Venus", "Moon", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

def button_callback(channel):
        print("button pressed")

def incSelect(channel):
	global count
	global planetNames
	count = count + 1
	print(count)
	lcd.clear()
	lcd.write_string(planetNames[count])
	time.sleep(1)


def decSelect(channel):
	global count
	global planetNames
	if count>0:
		count=count-1
	print(count)
	lcd.clear()
	lcd.write_string(planetNames[count])
	time.sleep(1)


def getPlanetInfo(planet):
	obj = Horizons(id=planet, location='000', epochs=None, id_type='majorbody')
	eph = obj.ephemerides()
	return eph


def findAZ(planet):
	obj = Horizons(id=planet, location='000', epochs=None, id_type='majorbody')
	eph = obj.ephemerides()
	percentageArc = (eph['AZ'][0])/360 #find Azimuth
	stepsNeeded = int(percentageArc*512) #512 steps is 360degrees
	print(eph['AZ'][0])
	return stepsNeeded

def findEL(planet):
        obj = Horizons(id=planet, location='000', epochs=None, id_type='majorbody')
        eph = obj.ephemerides()
        percentageArc = (eph['EL'][0])/360 #find Elevation
        stepsNeeded = int(percentageArc*512) #512 steps is 360degrees
        print(eph['EL'][0])
        return stepsNeeded

def moveStepper(axis, stepsNeeded):
	halfstep_seq = [
		[1,0,0,0],
		[1,1,0,0],
		[0,1,0,0],
		[0,1,1,0],
		[0,0,1,0],
		[0,0,1,1],
		[0,0,0,1],
		[1,0,0,1]
	]
	for i in range(stepsNeeded):
		for halfstep in range(8):
			for pin in range(4):
				GPIO.output(axis[pin], halfstep_seq[halfstep][pin])
			time.sleep(0.001)

GPIO.setmode(GPIO.BOARD)

for pin in stepperPinsAZ + stepperPinsEL:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,0)

GPIO.setup(selectBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(incBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(decBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(selectBtnPin, GPIO.FALLING, callback=button_callback, bouncetime=200)#Setup event on falling edge
GPIO.add_event_detect(incBtnPin, GPIO.FALLING, callback=incSelect, bouncetime=200)
GPIO.add_event_detect(decBtnPin, GPIO.FALLING, callback=decSelect, bouncetime=200)

lcd = CharLCD(cols=16, rows=2, dotsize=8, pin_rs=26,  pin_e=24, pins_data=[22, 18, 16, 12], numbering_mode=GPIO.BOARD)

lcd.clear()
lcd.write_string("Hello world!")
time.sleep(1)

AZSteps = findAZ(mars)
print(AZSteps)
ELSteps = findEL(mars)
print(ELSteps)

lcd.clear()
lcd.write_string("AZ " + str(AZSteps) + " EL " + str(ELSteps))
time.sleep(1)

#moveStepper(stepperPinsAZ, AZSteps)
#time.sleep(1)
#moveStepper(stepperPinsEL, ELSteps)
#time.sleep(1)

message = input("press enter to quit\n\n")

GPIO.cleanup()


