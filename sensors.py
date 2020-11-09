import sys
import time
import math
import threading

sys.path.append('./Software/Python/')
sys.path.append('./Software/Python/grove_rgb_lcd')

import grovepi
import grove_rgb_lcd as lcd

if __name__ == '__main__':
    UR = 4      # Ultrasonic ranger, D4
    DHT = 3     # humidity and temp sensor, D3
    LIGHT = 0   # light sensor, A0
    lcd.setRGB(153,255,51)
    lcd.clear()

    grovepi.pinMode(LIGHT,"INPUT")
    lock = threading.Lock()

    while True:
        time.sleep(5)   #polls every 5 seconds

        try:
            with lock:  #read ultrasonic ranger
                dist = grovepi.ultrasonicRead(UR)
                time.sleep(0.2)
            print("Distance:" + str(dist))

            with lock:  #read humidity&temp sensor
                [temp,humidity] = grovepi.dht(DHT,0)
                time.sleep(0.2)
  
            if math.isnan(temp) == False and math.isnan(humidity) == False:
                print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
         
            with lock:  #read light sensor
                light_value = grovepi.analogRead(LIGHT)
                time.sleep(0.2)
            print("Light:" + str(light_value))

        except IOError:
            print ("Error")

        #lcd display
        lcd.setText_norefresh("dist=%3dcm \nT=%.01f H=%.01f" % (dist,temp,humidity))
