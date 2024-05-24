from rplidar import RPLidar, RPLidarException
# import smbus2 as smbus
import math
import RPi.GPIO as GPIO
from time import sleep

GPIO.cleanup(False)

# GPIO pinleri tanımlama
motor_in1 = 4
motor_in2 = 17
motor_in3 = 27
motor_in4 = 22
motor_enA = 23
motor_enB = 24

# GPIO ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_in1, GPIO.OUT)
GPIO.setup(motor_in2, GPIO.OUT)
GPIO.setup(motor_in3, GPIO.OUT)
GPIO.setup(motor_in4, GPIO.OUT)
GPIO.setup(motor_enA, GPIO.OUT)
GPIO.setup(motor_enB, GPIO.OUT)

pwmA = GPIO.PWM(motor_enA, 100)
pwmB = GPIO.PWM(motor_enB, 100)
pwmA.start(0)
pwmB.start(0)


# bus = smbus.SMBus(1)
# address = 8

# def send_data_to_arduino(data):
#     bus.write_byte(address,data)
#     print("raspberry pi sent: ", data)

lidar = RPLidar('/dev/ttyUSB0')

lidar.__init__('/dev/ttyUSB0', 256000, 4, None)

lidar.connect()
print('lidar connected')
info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)


try:

    for i, scan in enumerate(lidar.iter_scans()):

        one_sent = False
        last_angle = None
        
        for d in scan:
            angle = d[1]
            distance = d[2] / 10
            
            
            if 290 <= angle <= 310:

                uzaklik = distance / 2
                sol_son_deger = uzaklik * math.sqrt(3)
                

            if 50 <= angle <= 70:

                uzaklik = distance / 2
                sag_son_deger = uzaklik * math.sqrt(3)
                

                x = sol_son_deger - sag_son_deger
                if (sag_son_deger - sol_son_deger) >= 10:
                    print(f'aracın sol değeri: {sol_son_deger}, sağ değeri: {sag_son_deger}, x = {x}')
                    print("Araç sağ gitsin")
                    GPIO.output(motor_in1, GPIO.HIGH)
                    GPIO.output(motor_in2, GPIO.HIGH)
                    GPIO.output(motor_in3, GPIO.LOW)
                    GPIO.output(motor_in4, GPIO.HIGH)
                    pwmA.ChangeDutyCycle(40)
                    pwmB.ChangeDutyCycle(50)
                    #sleep(0.1)
                elif (sol_son_deger - sag_son_deger) >= 10:
                    print(f'aracın sol değeri: {sol_son_deger}, sağ değeri: {sag_son_deger}, x = {x}')
                    print("Araç sola gitsin")
                    GPIO.output(motor_in1, GPIO.LOW)
                    GPIO.output(motor_in2, GPIO.HIGH)
                    GPIO.output(motor_in3, GPIO.HIGH)
                    GPIO.output(motor_in4, GPIO.LOW)
                    pwmA.ChangeDutyCycle(50)
                    pwmB.ChangeDutyCycle(40)
                    #sleep(0.1)
                else:
                    print(f'aracın sol değeri: {sol_son_deger}, sağ değeri: {sag_son_deger}, x = {x}')
                    print("Araç düz gitsin")
                    
                    GPIO.output(motor_in1, GPIO.LOW)
                    GPIO.output(motor_in2, GPIO.HIGH)
                    GPIO.output(motor_in3, GPIO.LOW)
                    GPIO.output(motor_in4, GPIO.HIGH)
                    pwmA.ChangeDutyCycle(75)
                    pwmB.ChangeDutyCycle(75)

            
                '''if (d[2] / 10) <= 50:
                    one_sent = True
                    print(1)
                    send_data_to_arduino(1)
                    break
                
                else:
                    one_sent = False'''
            
            if last_angle is not None and abs((last_angle - d[1]) % 360) > 345:
                one_sent = False
            
            last_angle = d[1]
            
        # if not one_sent:
        #     print(0)
        #     send_data_to_arduino(0)
        #     one_sent = False

        if False:
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()
            break
        
except KeyboardInterrupt as err:
    print('key board interupt')
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

except RPLidarException as err:
    print(err)
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    
except AttributeError:
    print('hi attribute error')
