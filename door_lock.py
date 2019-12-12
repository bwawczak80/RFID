from keypad import Key
from keypad import Keypad
import RPi.GPIO as GPIO 
import time
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from time import sleep, strftime
from datetime import datetime
import MFRC522
import signal


# I'm not able to get my any of the rfid files to run despite rebooting.  Without a working rfid, I'm lost on the code.  
ROWS = 4
COLS = 4
keys = 	['1','2','3','A',
	  '4','5','6','B',
	  '7','8','9','C',
	  '*','0','#','D'		]

rowsPins = [12,16,18,22]
colsPins = [19,15,13,11]
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    
    
def loop():
    keypad = Keypad(keys,rowsPins,colsPins,ROWS,COLS)
    keypad.setDebounceTime(50)
    mcp.output(3,1) 
    lcd.begin(16,2) 
    while(True):
        lcd.clear()
        lcd.setCursor(0,0)
        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()
        lcd.message('Scan card')  
        
        key = keypad.getKey()
        if(key != keypad.NULL):
            print ("You Pressed Key : %c "%(key) )
        
        sleep(.5)
    
def destroy():
    lcd.clear()
    
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522


PCF8574_address = 0x27
PCF8574A_address = 0x3F #I2C address of the chips

#Create GPIO adapter
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print('  I2C error')
        exit(1)
        
# Create LCD

lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
			
if __name__ == '__main__':     # Program start from here
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		pass
		GPIO.cleanup()		