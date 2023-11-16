try:
 import usocket as socket        #importing socket
except:
    import socket
import network
import time
from machine import Pin
from time import sleep
import dht
import umail
import Webpage
import Sensors
import utils



ssid = ****                 
password = ****    

def wifi_connect_sap(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password) 
    ap.active(True)
    while ap.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    ip_address = ap.ifconfig()[0]
    print(f'Connected on {ip_address}')
    return ip_address

ssid_s = ****
password_s = ****

#Push Buttons
button_black = Pin(1, Pin.IN, Pin.PULL_UP)
button_green = Pin(11, Pin.IN, Pin.PULL_UP)
button_red = Pin(12, Pin.IN, Pin.PULL_UP)

def wifi_connect_station(ssid, password):
  # Connect to your network using the provided credentials
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    # Wait for the connection to be established
    while station.isconnected() == False:
        print('Awaiting connection...')
        time.sleep(.5)
    print(station.ifconfig())
    return station.ifconfig()[0]
    
def open_socket(ip_address):
    # Open a socket
    address = (ip_address, 80)
    print(address)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection
    

Web = Webpage.Web_Class()
sensors = Sensors.SENSOR()
cond = utils.CONDITIONS()
lcd = utils.LCD_Display()
email = utils.send_email()

def all_reading():
    print('[INFO] Taking reading from sensors')
    body_temp, room_hum = sensors.body_temp()
    room_temp = sensors.room_temperature()
    Sp02 = sensors.spo2()
    pulse_rate = sensors.heart_rate()


    print(room_temp, body_temp, room_hum, pulse_rate, Sp02)

    print('-------------------------\n')
    return room_temp, body_temp, room_hum, pulse_rate, Sp02



def web_response(connection):
    while True:
        print('In the connection loop')
        conn, addr = connection.accept()
        print( conn, addr)
        request = conn.recv(1024)
        print('Trying to get response')
        response = Web.HTML_main(room_temp,room_hum, body_temp, pulse_rate, Sp02,Heading_rtemp, Body_rtemp, Heading_hum, Body_hum, Heading_temp,Body_temp, Heading_Sp02, Body_Sp02, Heading_bpm, Body_bpm )
        print('Response gotten')
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    
def reg_con(connection1):
    #Start a web server
    action = []
    while len(action) <= 0:
        print('In the signup loop')
        client, addr = connection1.accept()
        request = client.recv(1024)
        request = str(request)
        request1 = request.split()
        if request1[1] == '/submit.php':
            items = request1[-1].split('&')
            print(items)
            username = str(items[0]).split("=")[-1]
            password = str(items[1]).split("=")[-1]
            email = str(items[2]).split("=")[-1]
            age = str(items[3]).split("=")[-1]
            #print(items[3], items[4])
            weight = str(items[4]).split("=")[-1]
            height = str(items[5]).split("=")[-1]
            gender = str(items[6]).split("=")[1].split("'")[0]
            print(username,password,age, height, email,gender)
            with open("customers_details.txt", "w") as text_file: #customer_details
                text_file.write(username.rstrip('\n'))
                text_file.write(','+ password.rstrip('\n'))
                text_file.write(','+ email.rstrip('\n'))
                text_file.write(','+ age.rstrip('\n'))
                text_file.write(','+ height.rstrip('\n'))
                text_file.write(','+ weight.rstrip('\n'))
                text_file.write(','+ gender.rstrip('\n'))
                action.append('done')
        resp = Web.HTML_reg()
        client.send('HTTP/1.1 200 OK\n')
        client.send('Content-Type: text/html\n')
        client.send('Connection: close\n\n')
        client.sendall(resp)
        client.close()
        


def log_con(connection1):
    print('In the login loop')
    action = []
    while len(action) <= 0:
        client, addr = connection1.accept()
        request = client.recv(1024)
        request = str(request)
        print(request)
        
        request1 = request.split()
        print('request1[1] is :',request1[1])
        if request1[1] == '/signup.php':
            action.append('signup')
            print(action)
            #break
        elif request1[1] == '/login.php':
            items = request1[-1].split('&')
            #print(items)
            username = str(items[0]).split("=")[-1]
            password = str(items[1]).split("=")[1].split("'")[0]
            print(username, password)
            with open('customers_details.txt', 'r') as file:
                # read all lines in a list
                lines = file.readlines()
                for line in lines:
                    # check if string present on a current line
                    if line.find(username) != -1:
                        print('Line:', line)
                        r = list(line.split(','))
                        r_username = r[0]
                        r_password = r[1]
                        print(r[0], r[1])
                        if r[0] == username and r[1] == password:
                            action.append('proceed')
                            print(action)
                        else:
                            action.append('deny')
                            print(action)
                            
                    else:
                        print('Cannot find request')
            break
        
        html = Web.HTML_log()
        client.send('HTTP/1.1 200 OK\n')
        client.send('Content-Type: text/html\n')
        client.send('Connection: close\n\n')
        client.sendall(html)
        client.close()
        
    return action      



try:
    ip = wifi_connect_station(ssid_s, password_s)
    connection = open_socket(ip)
    lcd.print_screen(' About to take', 'Vital readings')
    time.sleep(10)
    room_temp, body_temp, room_hum, pulse_rate, Sp02 = all_reading()
    lcd.print_screen('  Done taking', 'Vital readings')
    time.sleep(5)
    for i in range(2):
        lcd.print_screen('Room Temp:{}°C'.format(room_temp), 'Humidity:{}%'.format(room_hum))
        time.sleep(5)
        lcd.print_screen('SP02:{}%'.format(Sp02), 'HeartRate:{}BPM'.format(pulse_rate))
        time.sleep(5)
        lcd.print_screen('Body Temp:{}°C'.format(body_temp), '')
        i =+1
        time.sleep(5)
    result = cond.conditions(room_temp, body_temp, room_hum, pulse_rate, Sp02)
    Heading_rtemp = result[0]
    Body_rtemp = result[1]
    Heading_hum=result[2]
    Body_hum = result[3]
    Heading_temp= result[4]
    Body_temp = result[5]
    Heading_Sp02 = result[6]
    Body_Sp02 = result[7]
    Heading_bpm = result[8]
    Body_bpm =  result[9]
    text1 = ('  Vital signs\n', '  are normal,', ' please try to', ' maintain to it')
    text2 = (' Vital signs\n', ' are outside the', 'normal range.\n', '  Contact your', 'GP immediately.', 'Press the black', 'emergency email', 'button to', 'trigger an email', 'or the red cancel', 'button to ignore')
    if result[10] == 1:
        lcd.print_more_lines(text1)
    else:
        while True:
            lcd.print_more_lines(text2)
            if button_black.value() == False: ##To send email
                print('email sent')
                email.to_GP(body_temp, pulse_rate, Sp02)
                lcd.print_screen('Email sent to', '      GP')
                time.sleep(7)
                break  
            if button_red.value() == False: ##To cancel
                break
    text = ('More information', ' are available',' on the Website')
    lcd.print_more_lines(text)
    lcd.print_more_lines(text )
    
    act = log_con(connection)
    print('Action to be taken is ',act[0])
    if act[0] == 'signup':
        reg_con(connection)
    elif act[0] == 'proceed':
        web_response(connection)
    elif act[0] == 'deny':
        log_con(connection)
    web_response(connection)
    
    web_response(connection)
    
except KeyboardInterrupt:
    machine.reset()
