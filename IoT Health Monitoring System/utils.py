import machine, time
from machine import Pin, PWM
from machine import Pin
from gpio_lcd import GpioLcd

import umail

sender_email = ****
sender_name = ****
sender_app_password = ****
recipient_email =****
email_subject_gp = ****

red=PWM(Pin(13,machine.Pin.OUT))
green=PWM(Pin(14,machine.Pin.OUT))
blue=PWM(Pin(15,machine.Pin.OUT))

red.freq(1000)
green.freq(1000)
blue.freq(1000)


class CONDITIONS():
    def __init__(self):
        pass

    def conditions(self, rtemp, btemp, rHum, pr, o2):
        result = []
        if 23 <= rtemp <= 26:
            Heading_rtemp = 'Room Temperature is normal'
            Body_rtemp = 'Temperature with normal range 23C to 26C'
            print(Heading_rtemp)
            result.append(Heading_rtemp)
            result.append(Body_rtemp)

        else:
            Heading_rtemp = 'Room Temperature is abnormal'
            Body_rtemp = 'Room Temperature outside the normal range 23C to 26C. Kindly ventilate the room'
            print(Heading_rtemp)
            result.append(Heading_rtemp)
            result.append(Body_rtemp)
            
        if 40 <= rHum <= 70:
            Heading_hum = 'Room Humidity is normal'
            Body_hum = 'Room Humidity with normal range 40% to 70%'
            print(Heading_hum)
            result.append(Heading_hum)
            result.append(Body_hum)
            #Action_rtemp = None
        else:
            Heading_hum = 'Room Humidity is abnormal'
            Body_hum = 'Room Humidity outside the normal range 23C to 26C. Kindly ventilate the room'
            print(Heading_hum)
            result.append(Heading_hum)
            result.append(Body_hum)
            #Action_rtemp = None
            
        if 36.1 <= btemp <= 37.9:
            Heading_temp = 'Body Temperature is normal'
            Body_temp = 'Body Temperature with normal range 40% to 70%'
            #Action_rtemp = Turn on red alert, send email to GP
            print(Heading_temp)
            result.append(Heading_temp)
            result.append(Body_temp)
        else:
            Heading_temp = 'Body Temperature is abnormal'
            Body_temp = 'Body Temperature outside the normal range 36.1C to 37.9C. Kindly ventilate the room'
            #Action_rtemp = if red alert is on ==> pass #else turn on red alert)
            print(Heading_temp)
            result.append(Heading_temp)
            result.append(Body_temp)

        if 93 <= o2 <= 100:
            Heading_Sp02 = 'Sp02 is normal'
            Body_Sp02 = 'Sp02 is within the normal range 93% -100%'
            print(Heading_Sp02)
            result.append(Heading_Sp02)
            result.append(Body_Sp02)
            #Action_Sp02 = no action
        else:
            Heading_Sp02 = 'Sp02 is abnormal'# (Red colour)'
            Body_Sp02 =  'Sp02 is outside the normal range 93% -100%, Kindly contact a GP'
            print(Heading_Sp02)
            result.append(Heading_Sp02)
            result.append(Body_Sp02)
            #Action_Sp02= ( if red alert is on ==> pass #else turn on red alert)
            
        if pr is None:
            Heading_bpm = 'Please take the heart rate reading again'
            Body_bpm = 'Unable to take Heart Rate per minutes'
        elif 60 <= pr <= 100:
            Heading_bpm = 'Heart Rate per minutes is normal'
            Body_bpm = 'Heart Rate per minutes is within the normal range 60 BPM -100 BPM'
            print(Heading_bpm)
            result.append(Heading_bpm)
            result.append(Body_bpm)
            #Action_Sp02 = no action
        else:
            Heading_bpm = 'Heart Rate is abnormal'# (Red colour)'
            Body_bpm =  'Heart Rate per minutes is outside the normal range 60 BPM -100 BPM, Kindly contact a GP'
            print(Heading_bpm)
            result.append(Heading_bpm)
            result.append(Body_bpm)
            
        if  (30 <= btemp <= 37.9) and (93 <= o2 <= 100) and (60 <= pr <= 100):
            red.duty_u16(0)
            green.duty_u16(65025)  ##Red light
            blue.duty_u16(0)
            print('Good Health Condition')
            HealthStatus = 1
            result.append(HealthStatus)
        elif (btemp <= 30 or btemp >= 37.9) or (o2 <= 93 or 02 >= 100) or (pr <= 60 or pr >= 150):
            red.duty_u16(65025)
            green.duty_u16() ##Green light
            blue.duty_u16(0)
            print('Bad Health Condition')
            HealthStatus = 0
            result.append(HealthStatus)
        elif (rtemp <= 23 or rtemp >= 26) or (rHum <= 40 or rHum >= 70):
            red.duty_u16(65550)
            green.duty_u16(50550)  ##Yellow Light
            blue.duty_u16(0)
            print('Bad Room Condition')
                                                           
        return result


 
class LCD_Display():
    def __init__(self, lcd= GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=16)):
        self.lcd = lcd
        
    def print_more_lines(self, a):
        a = list(a)
        self.lcd.clear()
        for item in a:
            print(a.index(item))
            if a.index(item) % 2 == 0:
                self.lcd.clear()
            self.lcd.putstr(item+'\n')
            time.sleep(3)
            
    def print_screen(self, text1, text2):
        self.lcd.clear()
        self.lcd.putstr(text1+'\n')
        self.lcd.move_to(0,1)
        self.lcd.putstr(text2+'\n')
        


##Send emails
class send_email:
    def __init__(self, smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)):
        self.smtp = smtp
        
    def to_GP(self, body_temp, pulse_rate, Sp02):
        self.smtp.login(sender_email, sender_app_password)
        self.smtp.to(recipient_email)
        self.smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
        self.smtp.write("Subject:" + email_subject_gp + "\n")
        self.smtp.write("Please below Amanda's Health Status\n")
        self.smtp.write("For your immediate attention!\n\n")
        self.smtp.write("Body Temperature:{}°C\n".format(body_temp))
        self.smtp.write("Heart Rate:{}BPM\n".format(pulse_rate))
        self.smtp.write("Oxygen Saturation Level (Sp02):{}°C\n".format(Sp02))
        self.smtp.send()
        self.smtp.quit()
        print('Email sent')
                 
                

