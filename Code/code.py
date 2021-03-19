import time


from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket

from adafruit_motorkit import MotorKit
kit = MotorKit()

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

print("running rc-bot-02 code.py...")

while True:

    kit.motor1.throttle = m1t = 0
    kit.motor2.throttle = m2t = 0
    kit.motor3.throttle = m3t = 0
    kit.motor4.throttle = m4t = 0
    time.sleep(0.25)

    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Now we're connected

    while ble.connected:
        if uart.in_waiting:
            packet = Packet.from_stream(uart)
            if isinstance(packet, ButtonPacket):
                if packet.button == ButtonPacket.UP:
                    if packet.pressed:
                        #print("UP")
                        m1t = m2t = -1.0
                        m3t = m4t = 1.0
                    else:
                        m1t = m2t = m3t = m4t = 0
                elif packet.button == ButtonPacket.RIGHT:
                    if packet.pressed:
                        #print("RIGHT")
                        m1t = m2t = m3t = m4t = -1.0
                    else:
                        m1t = m2t = m3t = m4t = 0
                elif packet.button == ButtonPacket.DOWN:
                    if packet.pressed:
                        #print("DOWN")
                        m1t = m2t = 1.0
                        m3t = m4t = -1.0
                    else:
                        m1t = m2t = m3t = m4t = 0
                elif packet.button == ButtonPacket.LEFT:
                    if packet.pressed:
                        #print("LEFT")
                        m1t = m2t = m3t = m4t = 1.0
                    else:
                        m1t = m2t = m3t = m4t = 0

        kit.motor1.throttle = m1t
        kit.motor2.throttle = m2t
        kit.motor3.throttle = m3t
        kit.motor4.throttle = m4t
        time.sleep(0.1)

    # If we got here, we lost the connection. Go up to the top and start
    # advertising again and waiting for a connection.