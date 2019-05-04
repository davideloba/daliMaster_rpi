# default I2C address
LW14_I2C_ADDRESS            = 0x23

# registers addresses
LW14_REGISTERS              = {
    "status"    : {"name": "status", "address" : 0x00, "mode" : "r", "length" : 1},
    "command"   : {"name": "command", "address" : 0x01, "mode" : "rw", "length" : 2},
    "config"    : {"name": "config", "address" : 0x02, "mode" : "w", "length" : 1},
    "signature" : {"name": "signature", "address" : 0xF0, "mode" : "r", "length" : 6},
    "address"   : {"name": "address", "address" : 0xFE, "mode" : "w", "length" : 2},
}

#Answers of 'status' register (see further for specification)
LW14_STATUS_BUS_FAULT       = 0x80 #1000 0000
LW14_STATUS_BUSY            = 0x40 #0100 0000
LW14_STATUS_OVERRUN         = 0x20 #0010 0000
LW14_STATUS_FRAMEERROR      = 0x10 #0001 0000
LW14_STATUS_VALID           = 0x08 #0000 1000
LW14_STATUS_TIMEFRAME       = 0x04 #0000 0100
LW14_STATUS_2BYTE           = 0x02 #0000 0010
LW14_STATUS_1BYTE           = 0x01 #0000 0001
LW14_STATUS_NONE            = 0x00 #0000 0000

#Special bits for DALI address
LW14_MODE_DACP              = 0x00
LW14_MODE_CMD               = 0x01
LW14_ADRR_SINGLE            = 0x00
LW14_ADRR_GROUP             = 0x80

BUS_TIMEOUT                 = 2 #sec
DALI_YES                    = 255
ERROR                       = -1

#DALI default values
DALI_DEFAULT_MAX            = 254
DALI_DEFAULT_MIN            = 1
DALI_DEFAULT_SYSTEM_FAIL    = 254
DALI_DEFAULT_POWER_ON       = 254
DALI_DEFAULT_FADE_RATE      = 7
DALI_DEFAULT_FADE_TIME      = 0

# 0x00 STATUS REGISTER bits:
#   7 - Bus Error Status, 0 = OK, 1 = Bus fault
#   6 - Busy, 0 = ready, 1 = Busy
#   5 - Overrun
#   4 - Frame Error
#   3 - Valid REPLY (reset by reading 0x01)
#   2 - Reply Timeframe, <22 Te since last command
#   1 - 2 Bytes telegram received (reset by reading 0x01)
#   0 - 1 Byte telegram received (reset by reading 0x01)
