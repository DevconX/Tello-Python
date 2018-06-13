import crc8
import crc16
import time
import datetime

messageStart   = 0x00cc
wifiMessage    = 0x001a
videoRateQuery = 0x0028
lightMessage   = 0x0035
flightMessage  = 0x0056
logMessage     = 0x1050

videoEncoderRateCommand = 0x0020
videoStartCommand       = 0x0025
exposureCommand         = 0x0034
timeCommand             = 0x0046
stickCommand            = 0x0050
takeoffCommand          = 0x0054
landCommand             = 0x0055
flipCommand             = 0x005c
throwtakeoffCommand     = 0x005d
palmLandCommand         = 0x005e
bounceCommand           = 0x1053

FlipFront = 0
FlipLeft = 1
FlipBack = 2
FlipRight = 3
FlipForwardLeft = 4
FlipBackLeft = 5
FlipBackRight = 6
FlipForwardRight = 7

seq = 0
rx, ry, lx, ly = 0, 0, 0, 0
throttle = 0

def create_packet(cmd, pkt, length):
    l = length + 11
    array_bytes = []
    array_bytes.append(messageStart.to_bytes(1,byteorder='little'))
    array_bytes.append((l << 3).to_bytes(1,byteorder='little'))
    array_bytes.append((0).to_bytes(1,byteorder='little'))
    digested= crc8.calculate_crc8(array_bytes).to_bytes(1,byteorder='little')
    array_bytes.append(digested)
    array_bytes.append((pkt).to_bytes(1,byteorder='little'))
    instructions=(cmd).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    return array_bytes

def take_off():
    global seq
    array_bytes = create_packet(takeoffCommand,0x68, 0)
    seq += 1
    instructions=seq.to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    instructions=(crc16.calculate_crc16(array_bytes)).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    return b''.join(array_bytes)

def land():
    global seq
    array_bytes = create_packet(landCommand,0x68, 1)
    seq += 1
    instructions=seq.to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    instructions=(crc16.calculate_crc16(array_bytes)).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    return b''.join(array_bytes)

def start_video():
    array_bytes = create_packet(videoStartCommand,0x60, 0)
    instructions=(0).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    instructions=(crc16.calculate_crc16(array_bytes)).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    return b''.join(array_bytes)

def set_videoencoder_rate(rate):
    global seq
    array_bytes = create_packet(videoEncoderRateCommand,0x68, 1)
    seq += 1
    instructions=seq.to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    array_bytes.append(rate.to_bytes(1,byteorder='little'))
    instructions=(crc16.calculate_crc16(array_bytes)).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    return b''.join(array_bytes)

def connection_string(port):
    instructions=port.to_bytes(2,byteorder='little')
    array_bytes=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    array_bytes=b'conn_req:'+b''.join(array_bytes)
    return array_bytes

def up(val):
    global ly
    ly = float(val) / 100.0

def down(val):
    global ly
    ly = float(val) / 100.0 * -1

def forward(val):
    global ry
    ry = float(val) / 100.0

def backward(val):
    global ry
    ry = float(val) / 100.0 * -1

def right(val):
    global rx
    rx = float(val) / 100.0

def left(val):
    global rx
    rx = float(val) / 100.0 * -1

def clockwise(val):
    global lx
    lx = float(val) / 100.0

def counter_clockwise(val):
    global lx
    lx = float(val) / 100.0 * -1

def flip(direction):
    global seq
    array_bytes = create_packet(flipCommand,0x70, 1)
    seq += 1
    instructions=seq.to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    array_bytes.append(direction.to_bytes(1,byteorder='little'))
    instructions=(crc16.calculate_crc16(array_bytes)).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    return b''.join(array_bytes)

def front_flip():
    return flip(FlipFront)

def back_flip():
    return flip(FlipBack)

def right_flip():
    return flip(FlipRight)

def left_flip():
    return flip(FlipLeft)

def send_stickcommand():
    array_bytes = create_packet(stickCommand, 0x60, 11)
    instructions=(0).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    axis1 = int(660.0*rx + 1024.0)
    axis2 = int(660.0*ry + 1024.0)
    axis3 = int(660.0*ly + 1024.0)
    axis4 = int(660.0*lx + 1024.0)
    axis5 = int(throttle)
    packed = (axis1)&0x7FF | (axis2&0x7FF)<<11 | (0x7FF&axis3)<<22 | (0x7FF&axis4)<<33 | (axis5)<<44
    array_bytes.append((0xFF&packed).to_bytes(1,byteorder='little'))
    array_bytes.append((packed>>8&0xFF).to_bytes(1,byteorder='little'))
    array_bytes.append((packed>>16&0xFF).to_bytes(1,byteorder='little'))
    array_bytes.append((packed>>24&0xFF).to_bytes(1,byteorder='little'))
    array_bytes.append((packed>>32&0xFF).to_bytes(1,byteorder='little'))
    array_bytes.append((packed>>40&0xFF).to_bytes(1,byteorder='little'))
    now = datetime.datetime.now()
    array_bytes.append((now.hour).to_bytes(1,byteorder='little'))
    array_bytes.append((now.minute).to_bytes(1,byteorder='little'))
    array_bytes.append((now.second).to_bytes(1,byteorder='little'))
    array_bytes.append((int(time.time() * 10)&0xff).to_bytes(1,byteorder='little'))
    array_bytes.append((int(time.time() * 10)>>8).to_bytes(4,byteorder='little')[0].to_bytes(1,byteorder='little'))
    instructions=(crc16.calculate_crc16(array_bytes)).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    return b''.join(array_bytes)

print(send_stickcommand())
