import crc8
import crc16

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

seq = 0

def create_packet(cmd, pkt, length):
    l = length + 11
    array_bytes = []
    array_bytes.append(messageStart.to_bytes(1,byteorder='little'))
    array_bytes.append((l << 3).to_bytes(1,byteorder='little'))
    array_bytes.append((0).to_bytes(1,byteorder='little'))
    digested= crc8.crc8(b''.join(array_bytes[:3])).digest()
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
    return array_bytes

def land():
    global seq
    array_bytes = create_packet(landCommand,0x68, 1)
    seq += 1
    instructions=seq.to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    instructions=(crc16.calculate_crc16(array_bytes)).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    return array_bytes

def start_video():
    array_bytes = create_packet(landCommand,0x60, 0)
    instructions=(0).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    instructions=(crc16.calculate_crc16(array_bytes)).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    return array_bytes

def set_videoencoder_rate(rate):
    global seq
    array_bytes = create_packet(videoEncoderRateCommand,0x68, 1)
    seq += 1
    instructions=seq.to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    array_bytes.append(rate.to_bytes(1,byteorder='little'))
    instructions=(crc16.calculate_crc16(array_bytes)).to_bytes(2,byteorder='little')
    array_bytes+=[instructions[0].to_bytes(1,byteorder='little'),instructions[1].to_bytes(1,byteorder='little')]
    return array_bytes
