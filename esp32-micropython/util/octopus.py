# this module is for Basic simple examples & tests
# it's loaded in boot.py and provides function octopus()
# user is questioned in interactive mode

# esp8266 / wemos / esp32 doit...

# ampy -p /COM4 put util/octopus-8266.py util/octopus.py
ver = "18.12.2018-v:0.25"

from micropython import const
import time, os
import machine, ubinascii
from machine import Pin, PWM, SPI, Timer

from util.buzzer import beep, play_melody
from util.led import blink
from util.pinout import set_pinout
pinout = set_pinout()

from util.display_segment import *

# spi
try:
    #spi.deinit()
    #print("spi > close")
    spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(pinout.SPI_CLK_PIN), mosi=Pin(pinout.SPI_MOSI_PIN))
    ss = Pin(pinout.SPI_CS0_PIN, Pin.OUT)
except:
    print()
rtc = machine.RTC() # real time

pwm0 = PWM(Pin(pinout.PIEZZO_PIN)) # create PWM object from a pin
pwm0.duty(0)

"""
timNote = Timer(8, freq=3000)
ch = timNote.channel(2, Timer.PWM, pin=Pin(pinout.PIEZZO_PIN))

tim = Timer(-1)
"""
led = Pin(pinout.BUILT_IN_LED, Pin.OUT) # BUILT_IN_LED

def add0(sn):
    ret_str=str(sn)
    if int(sn)<10:
       ret_str = "0"+str(sn)
    return ret_str

def get_hhmm():
    #print(str(rtc.datetime()[4])+":"+str(rtc.datetime()[5]))
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+":"+mm

octopuASCII = [
"      ,'''`.",
"     /      \ ",
"     |(@)(@)|",
"     )      (",
"    /,'))((`.\ ",
"   (( ((  )) ))",
"   )  \ `)(' / ( ",
]

def mainOctopus():
    for ol in octopuASCII:
        print(str(ol))
    print()

def mainMenu():
    print()
    print(get_hhmm())
    print('=' * 35)
    print("     O C T O P U S    M E N U")
    print('=' * 35)
    print("SYSTEM & SETTINGS")
    print("[i] - device & system info")
    print("[s] - setup machine and wifi")
    print("[w] - wifi test")
    print("[f] - file info/dir")
    print("[c] - clear terminal")
    print('.' * 30)
    print("EXAMPLES & TESTS")
    print("[b] - built-in led/beep/button")
    print("[r1] - RGB WS led test (/wr1)")
    print("[r8] - 8x RGB WS led test (/r80)")
    print("[m] - piezzo melody")
    print("[a] - analog input test")
    print("[t] - temperature")
    print("[d] - displays        --- >>>")
    print("[r] - robot/iot Board --- >>>")
    print("[p] - projects        --- >>>")
    #print("[u] * uart test")
    print("[q] - QUIT")
    print('-' * 35)

    sel = input("select: ")
    #print("your select: "+str(sel))
    return sel
    print()

# Define function callback for connecting event
def connected_callback(sta):
    global WSBindIP
    blink(led, 50, 100)
    # np[0] = (0, 128, 0)
    # np.write()
    blink(led, 50, 100)
    print(sta.ifconfig())
    WSBindIP = sta.ifconfig()[0]

def connecting_callback():
    # np[0] = (0, 0, 128)
    # np.write()
    blink(led, 50, 100)

#servo
SERVO_MIN = const(45)
SERVO_MAX = const(130)

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

def set_degree(servo, angle):
    servo.duty(map(angle, 0,150, SERVO_MIN, SERVO_MAX))

def w_connect():
    from util.wifi_connect import read_wifi_config, WiFiConnect
    time.sleep_ms(1000)
    wifi_config = read_wifi_config()
    print("config for: " + wifi_config["wifi_ssid"])
    w = WiFiConnect()
    w.events_add_connecting(connecting_callback)
    w.events_add_connected(connected_callback)
    w.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])
    print("WiFi: OK")

def neo_init(num_led):
    from neopixel import NeoPixel
    pin = Pin(pinout.WS_LED_PIN, Pin.OUT)
    npObj = NeoPixel(pin, num_led)
    return npObj

oled = 0
def oled_intit():
    global oled
    from lib import ssd1306
    time.sleep_ms(1000)
    i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#-------------
def octopus():
    print()
    #global notInitServo
    notInitServo = True
    global oled
    ###beep(pwm0,500,100) # start beep
    #tim.init(period=1000, mode=Timer.ONE_SHOT, callback=lambda t:print("test timer - thread delay"))
    #tim.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(2))
    mainOctopus()
    print("Hello, this is basic octopusLAB example (2018/12)")
    print(" (Press Ctrl+C to abort | CTRL+D to soft reboot)")
    print()

    time.sleep_us(10)       # sleep for 10 microseconds
    blink(led, 500)
    time.sleep_ms(300)     # 1s
    start = time.ticks_ms()

    run= True
    while run:
      sel = mainMenu()
      beep(pwm0, 1000, 50)

      if sel == "a":
          print("analog input test: ")
          pin_an = Pin(pinout.ANALOG_PIN, Pin.IN)
          adc = machine.ADC(pin_an)
          an = adc.read()
          print("RAW: " + str(an))
          # TODO improve mapping formula, doc: https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/adc.html
          print("volts: {0:.2f} V".format(an/4096*10.74), 20, 50)

      if sel == "b":
           count = 5
           for _ in range(count):
               beep(pwm0, 500, 100)
               blink(led, 500)

      if sel == "bt":
           butt1 = Pin(pinout.BUTT1_PIN, Pin.IN, Pin.PULL_UP)
           butt2 = Pin(pinout.BUTT2_PIN, Pin.IN, Pin.PULL_UP)
           butt3 = Pin(pinout.BUTT3_PIN, Pin.IN, Pin.PULL_UP)
           count = 10
           for _ in range(count):
               print("b1-"+str(butt1.value())),
               print("b2-"+str(butt2.value())),
               print("b3-"+str(butt3.value()))
               beep(pwm0, 500, 100)
               blink(led, 500)

      if sel == "c":
          print(chr(27) + "[2J") # clear terminal
          print("\x1b[2J\x1b[H") # cursor up
          mainOctopus()

      if sel == "f":
          print("file info /dir/ls:") #
          print(os.listdir())
          print("> lib: "+str(os.listdir("lib")))
          print("> util: "+str(os.listdir("util")))
          print("> pinouts: "+str(os.listdir("pinouts")))

          print("i2c.scann() >")
          i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))
          devices = i2c.scan()
          print(devices)

      if sel == "i":
          print("System info:")
          print("> octopus() ver: " + ver)
          from util.sys_info import sys_info
          sys_info()

      if sel == "m":
          time.sleep_ms(500)
          from util.buzzer.melody import mario
          play_melody(pwm0, mario)
          pwm0.duty(0)

      if sel == "r1":
        np = neo_init(1)

        np[0] = (128, 0, 0) #R
        np.write()
        time.sleep_ms(1000)

        np[0] = (0,128, 0) #G
        np.write()
        time.sleep_ms(1000)

        np[0] = (0, 0, 128) #B
        np.write()
        time.sleep_ms(1000)

        np[0] = (0, 0, 0) #0
        np.write()

      if sel == "r8":
       np = neo_init(8)

       np[0] = (32, 0, 0) #R
       np[1] = (0,32, 0) #G
       np[2] = (0, 0, 32) #B
       np[5] = (32, 0, 0) #R
       np[6] = (0,32, 0) #G
       np[7] = (0, 0, 32) #B
       np.write()

      if sel == "r80":
         NUMBER_LED = 8
         np = neo_init(NUMBER_LED)
         for i in range(NUMBER_LED):
           np[i] = (1, 0, 0)
           time.sleep_ms(1)# REVIEW:
         np.write()

      if sel == "s":
            from util.setup import setup
            setup()

      if sel == "t":
            print("temperature >")
            from lib.temperature import TemperatureSensor
            ts = TemperatureSensor(pinout.ONE_WIRE_PIN)
            temp = ts.read_temp()
            # print to console
            print(temp)

      if sel == "w":
            w_connect()

      if sel == "wr1":
            w_connect()
            np = neo_init(1)
            import urequests
            import json
            url1="http://octopuslab.cz/api/ws.json"
            print(url1)
            r1 = urequests.post(url1)
            j = json.loads(r1.text)
            time.sleep_ms(2000)
            print(j["r"])
            np[0] = (j["r"], j["g"], j["b"]) #R
            np.write()

      if sel == "q":
          print("machine.reset() and Exit")
          time.sleep_ms(1000)
          machine.reset()
          run = False

      if sel == "d":
         mainOctopus()
         print(">>> Display test submenu")
         print('=' * 30)
         print("--- [od] --- oled display test")
         print("--- [os] --- oled 3segment")
         print("--- [oi] --- oled display image")
         print("--- [m7] --- max display 8x7-segm")
         print("--- [m8] --- max display 8x8-matrix")
         print("--- [sd] --- serial display")
         print("-+- [nd] -+- Nextion display")
         print("-+- [id] -+- ink display")
         print('=' * 30)
         sel_d = input("select: ")

         if sel_d == "od":
              print("oled display test >")
              oled_intit()

              oled.fill(1)
              oled.show()
              time.sleep_ms(300)
              oled.fill(0)                # reset display
              oled.show()

              # write text on x, y
              oled.text('OLED test', 25, 10)
              oled.text(get_hhmm(), 45,29) #time HH:MM
              oled.hline(0,50,128,1)
              oled.text("octopusLAB 2018",5,55) #time HH:MM
              oled.show()
              time.sleep_ms(1000)

         if sel_d == "os":
              print("oled segment test >")
              oled_intit()
              #from util.display_segment import * #???
              for num in range(10):
                  threeDigits(oled,20+num,True,True)
                  time.sleep_ms(50)

         if sel_d == "oi":
             print("oled image test >")
             oled_intit()
             import framebuf

             IMAGE_WIDTH = 63
             IMAGE_HEIGHT = 63

             with open('assets/octopus_image.pbm', 'rb') as f:
                 f.readline() # Magic number
                 f.readline() # Creator comment
                 f.readline() # Dimensions
                 data = bytearray(f.read())
                 fbuf = framebuf.FrameBuffer(data, IMAGE_WIDTH, IMAGE_HEIGHT, framebuf.MONO_HLSB)
                 # To display just blit it to the display's framebuffer (note you need to invert, since ON pixels are dark on a normal screen, light on OLED).
                 oled.invert(1)
                 oled.blit(fbuf, 0, 0)

             oled.text("Octopus", 66,6)
             oled.text("Lab", 82,16)
             oled.text("Micro", 74,35)
             oled.text("Python", 70,45)
             oled.show()

         if sel_d == "m7":
             from lib.max7219_8digit import Display
             #spi = SPI(-1, baudrate=100000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(2))
             #ss = Pin(15, Pin.OUT)
             d7 = Display(spi, ss)
             d7.write_to_buffer('12345678')
             d7.display()

         if sel_d == "m8":
           from lib.max7219 import Matrix8x8
           d8 = Matrix8x8(spi, ss, 1) #1/4
           #print("SPI device already in use")

           count = 6
           for i in range(count):
             d8.fill(0)
             d8.text(str(i),0,0,1)
             d8.show()
             print(i)
             time.sleep_ms(500)

           d8.fill(0)
           d8.show()

         if sel_d == "sd":
                   from machine import UART
                   uart = UART(2, 9600) #UART2 > #U2TXD(SERVO1/PWM1_PIN)
                   uart.write('C')      #test quick clear display

                   uart.write('W7')   #change color
                   uart.write('h30')  #horizontal line
                   uart.write('h230') #horizontal line

                   uart.write('R0')
                   uart.write('W2')   #color
                   uart.write('QoctopusLAB - UART2 test*')
                   time.sleep_ms(100)
                   uart.write('R2')
                   uart.write('W1')   #color
                   uart.write('QESP32 & ROBOTboard*')
                   time.sleep_ms(100)

                   uart.write('R5')
                   uart.write('W2')   #color

                   num=9
                   for i in range(num):
                       uart.write('Q')
                       uart.write(str(num-i-1))
                       uart.write('*')
                       time.sleep_ms(500)

      if sel == "r":
             mainOctopus()
             print()
             print('=' * 30)
             print(">>> Boards special test")
             print('.' * 30)
             print("    Robot board")
             print("--- [dc] --- dc motor test")
             print("--- [se] --- servo")
             print("--- [sm] --- step motor")
             print('.' * 30)
             print("    IoT board")
             print("--- [re] --- relay test")
             print("--- [fa] --- pwm fan test")
             print('=' * 30)

             sel_r = input("select: ")
             if sel_r == "dc":
                  print("dc motor test >")
                  a1 = Pin(pinout.MOTOR_1A, Pin.OUT)
                  a2 = Pin(pinout.MOTOR_2A, Pin.OUT)
                  a12 = Pin(pinout.MOTOR_12EN, Pin.OUT)
                  a3 = Pin(pinout.MOTOR_3A, Pin.OUT)
                  a4 = Pin(pinout.MOTOR_4A, Pin.OUT)
                  a34 = Pin(pinout.MOTOR_34EN, Pin.OUT)

                  a34.value(0)
                  a12.value(1)

                  print("a12:10")
                  a1.value(1)
                  a2.value(0)
                  time.sleep_ms(3000)
                  print("a12:01")
                  a1.value(0)
                  a2.value(1)
                  time.sleep_ms(3000)

                  a12.value(0)
                  a34.value(1)

                  print("a34:01")
                  a3.value(0)
                  a4.value(1)
                  time.sleep_ms(3000)
                  print("a12:10")
                  a3.value(1)
                  a4.value(0)
                  time.sleep_ms(3000)
                  a34.value(0)

             if sel_r == "se":
                print("servo1 test >")
                #pwm_center = int(pinout.SERVO_MIN + (pinout.SERVO_MAX-pinout.SERVO_MIN)/2)
                pwm_center = 60

                #if notInitServo:
                print("init-servo:")
                pin_servo1 = Pin(pinout.PWM1_PIN, Pin.OUT)
                servo1 = PWM(pin_servo1, freq=50, duty=pwm_center)
                print("OK")
                time.sleep_ms(1500)
                #notInitServo = False

                time.sleep_ms(1500)
                servo1.duty(SERVO_MAX)
                time.sleep_ms(1500)
                servo1.duty(SERVO_MIN)
                time.sleep_ms(1500)

                print("degree45")
                set_degree(servo1,45)

             if sel_r == "sm":
                from lib.sm28byj48 import SM28BYJ48
                #PCF address = 35 #33-0x21/35-0x23
                ADDRESS = 0x23
                # motor id 1 or 2
                MOTOR_ID1 = 1
                #MOTOR_ID2 = 2

                i2c_sda = Pin(pinout.I2C_SDA_PIN, Pin.IN,  Pin.PULL_UP)
                i2c_scl = Pin(pinout.I2C_SCL_PIN, Pin.OUT, Pin.PULL_UP)

                i2c = machine.I2C(scl=i2c_scl, sda=i2c_sda, freq=100000) # 100kHz as Expander is slow :(
                motor1 = SM28BYJ48(i2c, ADDRESS, MOTOR_ID1)

                # turn right 90 deg
                motor1.turn_degree(90)
                # turn left 90 deg
                motor1.turn_degree(90, 1)

             if sel_r == "re":
                 print("relay test >")
                 rel = Pin(pinout.RELAY_PIN, Pin.OUT)
                 rel.value(1)
                 time.sleep_ms(3000)
                 rel.value(0)

      if sel == "p":
            mainOctopus()
            print()
            print(">>> Projects submenu")
            print('=' * 30)
            print("--- [1] --- temporary")
            print("--- [2] --- todo")
            print("--- [3] --- ")
            print('=' * 30)

            sel_p = input("select: ")
            if sel_p == "1":
                 print("project 1 >")


    delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    print("> delta time: "+str(delta))
    beep(pwm0, 2000, 50)
    print("all OK, press CTRL+D to soft reboot")
    blink(led, 50)
