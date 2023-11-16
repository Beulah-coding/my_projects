import machine
import dht
import math
import utime
import time
import max30100
import utils

from machine import Pin, PWM


#i2c = machine.I2C(0, scl=Pin(17), sda=Pin(16))
def normalise(buffer_list):
    sample_size = 4
    count = 0
    #print('[normalise function]: Entring while loop')
    while count < len(buffer_list) - sample_size +1:
        samples = buffer_list[count : count + sample_size]
        average = sum(samples) / sample_size
        count += 1
    try:
        return int(average)
    except:
        pass

#oximeter = max30100.MAX30100(i2c=(machine.I2C(0, scl=Pin(17), sda=Pin(16)
class SENSOR():
    
    def __init__(self,
                 in_temp = machine.ADC(4),
                 conversion_factor = 3.3 / (65535),
                 dhtSensor = dht.DHT11(Pin(2)),
                 oximeter = max30100.MAX30100(i2c=(machine.I2C(0, scl=Pin(9), sda=Pin(8)))),
                 lcd = utils.LCD_Display()
                 ):
        
        self.in_temp = in_temp
        self.conversion_factor = conversion_factor
        self.dhtSensor = dhtSensor
        self.oximeter = oximeter
        self.lcd = lcd
        
        
    def room_temperature(self):
        #print("[INFO]---Please place your finger on the temperature sensor")
        #print("[INFO]---Taking the Room Temperature Reading")
        temp_reading = self.in_temp.read_u16() * self.conversion_factor 
        room_temp = 27 - (temp_reading - 0.706)/0.001721
        time.sleep(2)
        return int(room_temp)
        time.sleep(1)
    
    def body_temp(self):
        self.lcd.print_screen('Put temp sensor', 'btw your elbow')
        time.sleep(7)
        self.lcd.print_screen('Taking the Temp', '    reading')
        time.sleep(7)
        #print("[INFO]---Taking the Room Humidity Reading")
        #print("[INFO]---Taking the Body Temperature Reading")
        self.dhtSensor.measure()
        body_temp = self.dhtSensor.temperature()
        room_hum = self.dhtSensor.humidity()
        return int(body_temp), int(room_hum)
    
    
    def spo2(self):
        self.oximeter.enable_spo2()
        
        wait_time = time.time() + int(60*.1)
        #print("[INFO]---Please place your finger on the pulse sensor")
        self.lcd.print_screen('place finger on', 'the pulse sensor')
        while time.time() < wait_time:
            self.oximeter.read_sensor()
        #print("[INFO] Taking spo2 reading")
        self.lcd.print_screen('Taking the Sp02', '     value')
        end_time = time.time() + int(60*.25)
        while time.time() < end_time:
            self.oximeter.read_sensor()
            if self.oximeter.ir != self.oximeter.buffer_ir :
                normalise_ir = (normalise(self.oximeter.buffer_ir))
            else:
                normalise_ir = int(self.oximeter.ir )
                
            if self.oximeter.red != self.oximeter.buffer_red:
                normalise_red = (normalise(self.oximeter.buffer_red))
            else:
                normalise_red = int(self.oximeter.red)
                
            Sp02 = math.log(normalise_red) / math.log(normalise_ir)
        return int(round(Sp02*100))

    def heart_rate(self):
        try:
            MAX_HISTORY = 250
            Total_Beats =30
            history = []
            beat = False
            beats = []
            
            self.oximeter.enable_spo2()
            
            wait_time = time.time() + int(60*.1)
            #print("[INFO]---Please place your finger on the pulse sensor")
            while time.time() < wait_time:
                self.oximeter.read_sensor()
            self.lcd.print_screen('Taking the Heart', '   Rate value')
            
            end_time = time.time() + int(60*.1)
            while time.time() < end_time:
                self.oximeter.read_sensor()
                history.append(self.oximeter.ir)
                history = history[-MAX_HISTORY:]
                minima, maxima = min(history), max(history)
                threshold_on = (minima + maxima * 3) // 4   # 3/4
                threshold_off = (minima + maxima) // 2      # 1/2
                if beat is False and self.oximeter.ir > threshold_on:
                    beat = True
                    beats.append(time.time())
                    beats = beats[-Total_Beats:]
                    beat_time = beats[-1] - beats[0]
                    if beat_time:
                        bpm = (len(beats)/(beat_time)) *60
                #elif beat is True and self.oximeter.ir > threshold_on:
                    #beats += 1
                time.sleep(.1)
                #print(self.oximeter.ir, threshold_on, threshold_off, beat, beats)
                    
                if beat is True and self.oximeter.ir < threshold_off:
                    beat = False
            return (int(bpm))
        except:
            pass
    