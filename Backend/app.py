import time
from RPi import GPIO
import threading 
import datetime

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository

import json
from json import JSONEncoder
from subprocess import check_output

import board
import adafruit_ws2801
#from hx711 import HX711
from hx711Klasse import HX711

leds = adafruit_ws2801.WS2801(board.SCLK, board.MOSI, 32)

#LED = 27
LDR = 21
PIR = 19

MotorPin1 = 22
MotorPin2 = 23
MotorPin3 = 24
MotorPin4 = 25

StepCount = 4086

step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
direction = False

hxx = HX711(18, 12, 128)

RS = 20
E = 26

LCDpin4 = 16
LCDpin5 = 17
LCDpin6 = 27
LCDpin7 = 13

LCD_CHR = True
LCD_CMD = False 
LCD_CHARS = 16 
LCD_LINE1 = 0x80 
LCD_LINE2 = 0xC0 

HoursMinutesNow = str(datetime.datetime.now().strftime("%H:%M"))

timeofday = ''

everyday = 0

ips = check_output(['hostname', '--all-ip-address'])
# LOCALHOST
adres1 = str(ips[0:15])
ip1 = adres1[2:]
# WIFI
adres2 = str(ips[16:30])
ip2 = adres2[2:]

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

def init_LCD():
    sendLCD(0x33,LCD_CMD) # Initialize
    sendLCD(0x32,LCD_CMD) # Set to 4-bit mode
    sendLCD(0x06,LCD_CMD) # Cursor move direction
    sendLCD(0x0C,LCD_CMD) # Turn cursor off
    sendLCD(0x28,LCD_CMD) # 2 line display
    sendLCD(0x01,LCD_CMD) # Clear display
    time.sleep(0.002)

def sendLCD(bits, mode):
    GPIO.output(RS, mode)

    GPIO.output(LCDpin4, False)
    GPIO.output(LCDpin5, False)
    GPIO.output(LCDpin6, False)
    GPIO.output(LCDpin7, False)

    if bits&0x10==0x10:
        GPIO.output(LCDpin4, True)

    if bits&0x20==0x20:
        GPIO.output(LCDpin5, True)

    if bits&0x40==0x40:
        GPIO.output(LCDpin6, True)

    if bits&0x80==0x80:
        GPIO.output(LCDpin7, True)

    lcd_toggle_enable()

    GPIO.output(LCDpin4, False)
    GPIO.output(LCDpin5, False)
    GPIO.output(LCDpin6, False)
    GPIO.output(LCDpin7, False)

    if bits&0x01==0x01:
        GPIO.output(LCDpin4, True)

    if bits&0x02==0x02:
        GPIO.output(LCDpin5, True)

    if bits&0x04==0x04:
        GPIO.output(LCDpin6, True)

    if bits&0x08==0x08:
        GPIO.output(LCDpin7, True)

    lcd_toggle_enable()

def lcd_toggle_enable():
    time.sleep(0.0005)
    GPIO.output(E, True)
    time.sleep(0.0005)
    GPIO.output(E, False)
    time.sleep(0.0005)

def send_message(message, line):
    # Send text to display
    message = message.ljust(LCD_CHARS," ")

    sendLCD(line, LCD_CMD)

    for i in range(LCD_CHARS):
        sendLCD(ord(message[i]), LCD_CHR)

    sendLCD(line, LCD_CMD)

    for i in range(LCD_CHARS):
        sendLCD(ord(message[i]), LCD_CHR)

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    #GPIO.setup(LED, GPIO.OUT)
    GPIO.setup(LDR, GPIO.OUT)

    GPIO.setup(MotorPin1, GPIO.OUT)
    GPIO.setup(MotorPin2, GPIO.OUT)
    GPIO.setup(MotorPin3, GPIO.OUT)
    GPIO.setup(MotorPin4, GPIO.OUT)

    GPIO.output(MotorPin1, GPIO.LOW)
    GPIO.output(MotorPin2, GPIO.LOW)
    GPIO.output(MotorPin3, GPIO.LOW)
    GPIO.output(MotorPin4, GPIO.LOW)

    GPIO.setup(PIR, GPIO.IN)

    GPIO.setup(E, GPIO.OUT)
    GPIO.setup(RS, GPIO.OUT)
    GPIO.setup(LCDpin4, GPIO.OUT)
    GPIO.setup(LCDpin5, GPIO.OUT)
    GPIO.setup(LCDpin6, GPIO.OUT)
    GPIO.setup(LCDpin7, GPIO.OUT)

    init_LCD()

    hxx.reset()

def read_LDR(pin):
    count = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(pin, GPIO.IN)

    while (GPIO.input(pin) == GPIO.LOW):
         count += 1
    return count

def LDR_value():
    value = read_LDR(LDR) / 1000
    return value

def cleanup_MotorPins():
    GPIO.output(MotorPin1, GPIO.LOW)
    GPIO.output(MotorPin2, GPIO.LOW)
    GPIO.output(MotorPin3, GPIO.LOW)
    GPIO.output(MotorPin4, GPIO.LOW)

def rotate():
    motor_pins = [MotorPin1, MotorPin2, MotorPin3, MotorPin4]
    motor_step_counter = 0
    i = 0
    for i in range(StepCount):
        for pin in range(0, len(motor_pins)):
            GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])

        if direction ==True:
            motor_step_counter = (motor_step_counter - 1) % 8

        elif direction == False:
            motor_step_counter = (motor_step_counter + 1) % 8

        else:
            cleanup_MotorPins()

        time.sleep(0.002)

# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False, ping_timeout=1)
CORS(app)

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

def status():
    # Ophalen van de data

    global old_status_LDR

    while True:

        global HoursMinutesNow
        HoursMinutesNow = str(datetime.datetime.now().strftime("%H:%M"))

        dag = datetime.datetime.today().weekday()

        if (dag == 0) and HoursMinutesNow =='12:00':
            print("reset historiek")
            DataRepository.reset_History()

        send_message(str(ip1), LCD_LINE1)
        send_message("", LCD_LINE2)
        #send_message(str(ip2), LCD_LINE2)

        global everyday
        global timeofday
        #print(f"het uur nu: {HoursMinutesNow}")
        #print(f"gekozen uur: {timeofday}")
        #print(f"elke dag: {everyday}")

        #if everyday == 0:
        #    if timeofday == HoursMinutesNow:
        #        print("eten wordt gegeven!")
        #        Change_motor_Value()
        #        everyday == 99

        if timeofday == HoursMinutesNow:
            print("eten wordt gegeven!")
            Change_motor_Value()
            timeofday = 'gedaan'

        new_status = LDR_value()
        #print(f"new status: {new_status}")
        if new_status > 400:
            #GPIO.output(LED, GPIO.HIGH)
            leds.fill((0x40, 0x40, 0x40))
        if new_status <= 400:
            #GPIO.output(LED, GPIO.LOW)
            leds.fill((0, 0, 0))

        #print(f"LDR wordt veranderd naar {new_status}")
        
        date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        try:
            if old_status_LDR != new_status:
                if (new_status >= (old_status_LDR + 400)) or (new_status <= (old_status_LDR - 400)):
                    # Stel de status in op de DB
                    DataRepository.add_LDR(date, new_status)
                    old_status_LDR = new_status
                    #print(f"old status: {old_status_LDR}")
        except:
            old_status_LDR = new_status

        socketio.emit('B2F_verandering_LDR', {'LDR': new_status}, broadcast=True)
        time.sleep(0.01)
        Change_PIR_Value()
        time.sleep(0.01)
        Change_HX711_Value()

        time.sleep(2)

print("**** Program started ****")

setup()

thread = threading.Timer(2, status)
thread.start()

@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    statusLDR = DataRepository.read_LDR()
    emit('B2F_status', {'LDR': statusLDR}, broadcast=True)
    
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    emit('B2F_date', {'date': date}, broadcast=True)

@socketio.on('F2B_change_LDR_Value')
def Change_LDR_Value():
    # Ophalen van de data
    new_status = LDR_value()
    if new_status > 400:
        #GPIO.output(LED, GPIO.HIGH)
        leds.fill((0x40, 0x40, 0x40))

    if new_status <= 400:
        #GPIO.output(LED, GPIO.LOW)
        leds.fill((0, 0, 0))
    
    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    #print(f"LDR wordt veranderd naar {new_status}")

    # Stel de status in op de DB
    #res = DataRepository.add_LDR(date, new_status)

    socketio.emit('B2F_verandering_LDR', {'LDR': new_status}, broadcast=True)

@socketio.on('F2B_change_Motor_Value')
def Change_motor_Value():
    # Ophalen van de data
    rotate()

    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #print(date)

    # Stel de status in op de DB
    DataRepository.add_Motor(date)
    socketio.emit('B2F_verandering_Motor', {'Motor': date}, broadcast=True)

@socketio.on('F2B_change_PIR_Value')
def Change_PIR_Value():
    # Ophalen van de data
    new_status = GPIO.input(PIR)
    #print(f"status PIR: {new_status}")

    if new_status == 1:

        date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        #print(date)

        # Stel de status in op de DB
        DataRepository.add_PIR(date, new_status)

        socketio.emit('B2F_verandering_PIR', {'PIR': new_status}, broadcast=True)

@socketio.on('F2B_change_HX711_Value')
def Change_HX711_Value():
    # Ophalen van de data
    d = hxx.get_weight()
    new_status = d
    #print(f"status HX711: {new_status[0]}")

    date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Stel de status in op de DB
    # DataRepository.add_HX711(date, new_status[0])

    socketio.emit('B2F_verandering_HX711', {'HX711': new_status[0]}, broadcast=True)

@socketio.on('F2B_history')
def History():
    # Ophalen van de data
    his = DataRepository.read_History()
    #print(DateTimeEncoder().encode(his))
    x = json.dumps(his, indent=4, cls=DateTimeEncoder)
    socketio.emit('B2F_history', x, broadcast=True)

@socketio.on('F2B_autofeed')
def Autofeed(jsonObject):
    # Ophalen van de data
    global timeofday
    global everyday
    timeofday = jsonObject['timeofday']
    everyday = jsonObject['everyday']
    #print(jsonObject)

if __name__ == '__main__':
    try:
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt:
        GPIO.cleanup()
