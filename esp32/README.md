# octopuslab/esp32

vývojová deska <a href="http://www.octopuslab.cz/index.php/vyvojove-desky/robot-board">octopusLAB - ROBOT board</a> - je k následujícím testům připravena (stačí osadit konektory, případně IO)<br />
<br />
esp32-01-blink	- základní test ESP a korektního uploadu programu (není potřeba nic krom ESP32 modulu)<br />
esp32-02-ws1	- testujeme RGB LED diodu<br />
esp32-02-ws8  - test 8x RGB LED WS<br />
esp32-03-ad - měření napětí<br />
esp32-03-touch-button - kapacitní tlačítko<br />	
esp32-04-hall	- halova sonda citlivá na magnetické pole<br />
esp32-05-i2c<br />
esp32-05-spi<br />
esp32-05-spi-sd	<br />
esp32-05-spileddisplay - LED sedmisegmentový display s obvodem max<br />
esp32-06-dcmotor-pwm<br />	
esp32-06-dcmotor - dva stejnosměrné motorky pro podvozek robora<br />	
esp32-07-i2c-stepper dva krokové motory na i2c<br />	
esp32-07-servo<br />	
esp32-08-accel-MMA_7455<br />	
esp32-08-apds9930<br />	
esp32-08-bt - pokus s bt<br />
esp32-08-echo - test měřiče vzdálenosti HC-SR04<br />
esp32-09-wifi - test wifi<br />
<hr />

<pre>
oeLAB-esp32 (DoIt) 2x15 pins:                               [ROBOT Board]:
                          -----------     (GPIO)
                      EN -           - D23 (23)  MOSI       [SPI_MOSI_PIN] 
[PIN_ANALOG]    (36)  VP -           - D22 (22)  SCL(I2C)   [I2C_SCL_PIN]
[I39_PIN]       (39)  VN -           - TXD (1)   D2
[I34_PIN]            D34 -           - RXD (3)   D3
[I35_PIN]            D35 -           - D21 (21)  SDA(I2C)   [I2C_SDA_PIN]
[ONE_WIRE_PIN] DEV1  D32 -           - D19 (19)  MISO       [SPI_MISO_PIN]
               DEV2  D33 -  (ESP32)  - D18 (18)  SCLK       [SPI_CLK_PIN]
[MOTOR_12EN]         D25 -           - D5  (5)   CS0        [SPI_CS0_PIN]
[MOTOR_1A]           D26 -           - TX2 (17)             [PIN_PWM1] /Servo1
[MOTOR_4A]           D27 -           - RX2 (16)             [PIN_PWM2] /Servo2
[MOTOR_3A]           D14 -           - D4  (4)              [PIN_PWM3] /Servo3
[MOTOR_2A]           D12 -           - D2  (2)              [BUILT_IN_LED]
[MOTOR_34EN]         D13 -           - D15 (15)             [WS_LED_PIN] //v1(13)     
                     GND -           - GND
                     VIN -           - 3V3 +
                          -----------
</pre>                          
<br/> 

<pre>



240 MHz dual core Tensilica LX6 microcontroller with 600 DMIPS
Integrated 520 KB SRAM
Integrated 802.11 b/g/n HT40 Wi-Fi transceiver, baseband, stack and LWIP
Integrated dual mode Bluetooth (classic and BLE)
16 MB flash, memory-mapped to the CPU code space
2.3V to 3.6V operating voltage
-40°C to +125°C operating temperature
On-board PCB antenna / IPEX connector for external antenna

Sensors	
Ultra-low noise analog amplifier, Hall sensor, 10x capacitive touch interfaces

32 kHz crystal oscillator
34x GPIO, 3 x UARTs, including hardware flow control
3 x SPI, 2 x I2S
12 x ADC input channels
2 x DAC, 2 x I2C
PWM/timer input/output available on every GPIO pin
OpenOCD debug interface with 32 kB TRAX buffer
SDIO master/slave 50 MHz
</pre>



driver CP2102: https://www.pololu.com/docs/0J7/all [2018/05-Win10-ok]

arduino C:<br /> 
a) https://navody.arduino-shop.cz/navody-k-produktum/vyvojova-deska-esp32.html<br />
https://github.com/espressif/arduino-esp32<br />
b) soubor/vlastosti//správce dalších desek:<br />
https://dl.espressif.com/dl/package_esp32_index.json<br />
manažér desek - ESP - by Esperessif System 
DOIT ESP DEV KIT V1 [2018/07-Win10-ok]

<br /><br />
micropython: https://github.com/octopusengine/octopuslab/tree/master/esp32-micropython<br />

