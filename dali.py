# DALI TELEGRAM
#
# 1 start bit
# 8 address bits: 1 individual or group address bit (Y) , 6 address bits, 1 select bit (S)
# 8 data bits
# 2 stop bits
#
# ADDRESS BYTE:
# Short or group address            YAAAAAAS
# Short addresses (from 0 to 63)    0AAAAAAS
# Group addresses (from 0 to 15)    100AAAAS
# Broadcast                         1111111S
#
# Special command                   101CCCC1
# Special command                   110CCCC1
#
#
# S: selector bit:
#   S = ‘0’ direct arc power level following
#   S = ‘1’ command following (indirect)
#   Y = ‘0’ short address
#   Y = ‘1’ group address or broadcast
#
# A: significant address bit
# C: significant command bit
#
# examples:
#
# Direct arc power control command
# YAAA AAA0 XXXX XXXX
#
# indirect arc power control commands
# YAAA AAA1 XXXX XXXX (16-31)
#
# configuration commands
# YAAA AAA1 XXXX XXXX (32-128)
#
# query commands
# YAAA AAA1 XXXX XXXX (144-196)
#
# special commands
# 101CCCC1 XXXX XXXX or
# 110CCCC1 XXXX XXXX


# Indirect commands (0 ... 31)
DALI_OFF                                = 0   #Switches off the light immediately
DALI_UP                                 = 1   #200 ms dimming up
DALI_DOWN                               = 2   #200 ms dimming down
DALI_STEP_UP                            = 3   #Increases the brightness by one step
DALI_STEP_DOWN                          = 4   #Decreases the brightness by one step
DALI_MAX_LEVEL                          = 5   #Maximum brightness
DALI_MIN_LEVEL                          = 6   #Minimum brightness
DALI_STEP_DOWN_OFF                      = 7   #Decrease brightness by one step (including switching off)
DALI_ON_STEP_UP                         = 8   #Increase brightness by one step (including switching on)
DALI_ENABLE_DAPC_SEQUENCE               = 9   #Commence DACP sequence
#10 - 15 RESERVED
DALI_GO_TO_SCENE                        = 16  #16 - 31, Enables scene 0 to 15

# Configuration commands (32 ... 41)
DALI_RESET					            = 32  #Resets nonvolatile memory
DALI_DTR_ACTUAL_LEVEL		            = 33  #Reads out the current power level
#34 - 41 RESERVED

# DALI Save DTR value (42 ... 63)
DALI_DTR_MAX_LEVEL			            = 42  #Save as maximum power value
DALI_DTR_MIN_LEVEL			            = 43  #Save as minimum power value
DALI_DTR_SYS_FAIL_LEVEL		            = 44  #Save power value as value for event of error
DALI_DTR_POWER_ON_LEVEL		            = 45  #Save power value as switch-on value
DALI_DTR_FADE_TIME			            = 46  #Save value as dimming time
DALI_DTR_FADE_RATE			            = 47  #Save value as dimming speed
#48 - 63 RESERVED

# Used for setting system parameters (64 ... 143)
DALI_ADD_SCENE				            = 64  #64 - 79, Save DTR value as selected scene 0 to 15
DALI_REMOVE_SCENE			            = 80  #80 - 95, Removes DALI slave from scene 0 to 15
DALI_ADD_GROUP				            = 96  #96 - 111, Adds DALI slave to group 0 to 15
DALI_REMOVE_GROUP			            = 112 #112 - 127, Removes DALI slave from group 0 to 15
DALI_DTR_AS_SHORT_ADDRESS 	            = 128 #Save DTR value as short address
#129 - 143 RESERVED

# Query commands (144 ... 223)
DALI_QUERY_STATUS						= 144 #Checks the general status (see further for specification)
DALI_QUERY_BALLAST				        = 145 #Checks communication readiness, answer: "Yes" or "No"
DALI_QUERY_LAMP_FAILURE					= 146 #Checks for light failure, answer: "Yes" or "No"
DALI_QUERY_LAMP_POWER_ON				= 147 #Checks whether light is currently on, answer: "Yes" or "No"
DALI_QUERY_LIMIT_ERROR					= 148 #Checks whether the last requested power value was applied, answer: "Yes" or "No"
DALI_QUERY_RESET_STATE					= 149 #Checks whether the DALI slave is in reset state, answer: "Yes" or "No"
DALI_QUERY_MISSING_SHORT_ADDRESS		= 150 #Checks whether the DALI slave has a short address, answer: "Yes" or "No"
DALI_QUERY_VERSION_NUMBER				= 151 #Checks whether the DALI slave has a version number
DALI_QUERY_CONTENT_DTR					= 152 #Checks the DTR value
DALI_QUERY_DEVICE_TYPE					= 153 #Checks the device type, answer: 0 - 255
DALI_QUERY_PHYSICAL_MIN_LEVEL			= 154 #Checks the physical minimum level (greater than 0)
DALI_QUERY_POWER_FAILURE				= 155 #Checks for power failure, answer: "Yes" or "No"
#156 - 159 RESERVED
DALI_QUERY_ACTUAL_LEVEL					= 160 #Checks the current power level, answer: 0 - 255
DALI_QUERY_MAX_LEVEL					= 161 #Checks the maximum value
DALI_QUERY_MIN_LEVEL					= 162 #Checks the minimum value
DALI_QUERY_POWER_ON_LEVEL				= 163 #Checks the switch-on power level
DALI_QUERY_SYSTEM_FAILURE_LEVEL			= 164 #Checks the power level in the event of error
DALI_QUERY_FADE_TIME_RATE				= 165 #Checks the dimming time and dimming speed  (see further for specification)
#166 - 175 RESERVED
DALI_QUERY_SCENE_LEVEL					= 176 #176 - 191, Checks the light level for scene 0 to 15
DALI_QUERY_GROUPS_0_7					= 192 #Checks groups 0 to 7
DALI_QUERY_GROUPS_8_15					= 193 #Checks groups 8 to 15
DALI_QUERY_RANDOM_ADDRESS_H				= 194 #Checks the 8 high bits of the random address
DALI_QUERY_RANDOM_ADDRESS_M				= 195 #Checks the 8 mids bits of the random address
DALI_QUERY_RANDOM_ADDRESS_L				= 196 #Checks the 8 low bits of the random address
#197 - 223 RESERVED

#224 - 255 Checks application-specific defined commands

# Special commands
# Special commands shall be broadcast and received by all ballasts.
# This means that the main address shall be 101C CCC1or 110C CCC1. CCCC is the significant "SPECIAL COMMAND".
# e.g.:
# Command 169: 1010 1001 0000 0000 "COMPARE"
# 1010 1011 = 169
DALI_TERMINATE                          = 161 #Switches all DALI slaves on the bus in normal mode
DALI_STORE_TO_DTR                       = 163 #10100011 XXXXXXXX, Writes the bit pattern XXXXXXXX to the Data Transfer Register (DTR)
DALI_INITIALISE                         = 165 #Allows commands for special addressing within the next 15 minutes
DALI_RANDOMISE                          = 167 #The ballast shall generate a new random address on the request of this command
DALI_COMPARE                            = 169 #The ballast shall compare it's random address with the combined search address
DALI_WITHDRAW                           = 171 #The selected slave is excluded from the subsequent search with "COMPARE" statements but remains initialized and can be selected
#173 - 175 Reserved
DALI_SEARCHADDR_H                       = 177 #The 8 high bits of the search address
DALI_SEARCHADDR_M                       = 179 #The 8 mid bits of the search address
DALI_SEARCHADDR_L                       = 181 #The 8 low bits of the search address

DALI_PROGRAM_SHORT_ADDRESS              = 183 #10110111 0AAAAAA1, The selected slave takes on the short address assigned to AAAAAA.
DALI_VERIFY_SHORT_ADDRESS               = 185 #The selected slave responds with YES if the value specified on aaaaaa corresponds to its short address
DALI_QUERY_SHORT_ADDRESS                = 187 #The selected slave responds with its current short address
DALI_PHYSICAL_SELECTION                 = 189 #The selected slave is excluded from the subsequent search with "COMPARE" statements, no longer initialized and can no longer be selected

#Additional special commands can be found in the DALI standard.


# DALI_QUERY_STATUS
# Answer is the following "STATUS INFORMATION" byte:
# bit 0     Status of ballast; "0" = OK, "1" = KO
# bit 1     Lamp failure; "0" = OK , "1" = KO
# bit 2     Lamp arc power on; "0" = OFF , "1" = ON
# bit 3     Query: Limit Error; "0" = Last requested arc power level is between MIN..MAX LEVEL or OFF
# bit 4     Fade ready; "0" = fade is ready; "1" = fade is running
# bit 5     Query: "RESET STATE"? "0" = "No", "1" = "Yes"
# bit 6     Query: Missing short address? "0" = "No", "1" = "Yes"
# bit 7     Query: "POWER FAILURE"? "0" = "No"; "RESET" or an arc power control command has been received after last power-on.

# DALI_QUERY_FADE_TIME_RATE
# Answer 8 bit, FADE TIME(X) and FADE RATE(Y): XXXX YYYYY
# values for Fadetime and fade rate. Time is in seconds, Rate is in steps/second
# fadetime = [0,0.7,1.0,1.4,2.0,2.8,4.0,5.7,8.0,11.3,16.0,22.6,32.0,45.3,64.0,90.5] #value to dali -> 0 ... 15
# faderate = [0,358,253,179,127,89.4,63.3,44.7,31.6,22.4,15.8,11.2,7.9,5.6,4.0,2.8] #value to dali -> 0 ... 15  -> 0 is impossible!
