# shellControl.py

Here there is a list of commands that you can send to your Raspberry Pi by shell in order to control daliMaster Hat.

## Getting started
Launch *shellControl.py* under *examples/shellControl* folder. Digit your custom daliMaster address as program argument if it is different from default.
```
sudo python3 examples/shellControl/shellControl.py [custom I2C address if any]
```
### Hello world
```
I2C DALI master(0x23) begin..
PING I2C device 0x23..ok
device 0x23 is ready
Digit your command (press "Enter" to see all options):
```
At this point, you are asked to send command. Write your command and press return to send it. Remember that you can send up to 4 arguments each time. The program will echo the received command and if it is correct it will be execute.

### Set new I2C address
**-a [new address]**  
Set another I2C address to the daliMaster chip. You can use hex or decimal address. Values of 128(0x80) and more are not accepted.
#### example
```
-a 39
```
response:
```
received commands: [-a][39]
Setting 39(0x27) as new I2C address
Ping I2C device 39(0x27)..ok
done.
```
### Read register
**-r [register name]**

Read daliMaster register and echo result. Available registers are:
* "status" :
The status register is one byte that contains the bus status and command status flags (see further).
* "command" :
The command register has two bytes which directly represent the DALI command. Please refer to the DALI specification for details on the commands.
* "signature" :
The signature register can be used to identify the I2C chip and get the revision information for the firmware.

#### example
In this example we will ask ballast its physically minimum level and read the response.
First of all do a dummy reading to free previous message on "command" register. Do not mind output.
```
-r command
```
Query lamp with Short Address 8 with DALI_QUERY_PHYSICAL_MIN_LEVEL code (154).
```
-q -s 8 154
```
response:
```
received commands: [-q][-s][8][154]
query command function called
(now you should read command register to see the response)
done.
```
Now if we read the "status" register we will find that a reply is available.
```
-r status
```
response:
```
received commands: [-r][status]
BUS FAULT         0
BUSY              0
OVERRUN           0
FRAM ERROR        0
VALID REPLY       1
REPLY TIMEFRAME   0
2 BYTE TELEGRAM   0
1 BYTE TELEGRAM   1
read:9(00001001)
done.
```
This register has changed quickly after the query in this way.
```
BUS FAULT         0
BUSY              1
OVERRUN           0
FRAM ERROR        0
VALID REPLY       0
REPLY TIMEFRAME   0
2 BYTE TELEGRAM   0
1 BYTE TELEGRAM   0
```
BUSY = 1 indicates that the last command has not yet been transmitted. Any new command sent to register 1 will be ignored until the last command has been transmitted and the busy bit is cleared.
```
BUS FAULT         0
BUSY              0
OVERRUN           0
FRAM ERROR        0
VALID REPLY       0
REPLY TIMEFRAME   1
2 BYTE TELEGRAM   0
1 BYTE TELEGRAM   0
```
REPLY TIMEFRAME = 1 indicates that the time frame for a reply from the last addressed device has not yet timed out and is reset to zero after 22 Te (see DALI specification) or on bus activity.
```
BUS FAULT         0
BUSY              0
OVERRUN           0
FRAM ERROR        0
VALID REPLY       1
REPLY TIMEFRAME   0
2 BYTE TELEGRAM   0
1 BYTE TELEGRAM   1
```
Valid Reply = 1 if a telegram has been received within 22 Te (see DALI specification) of sending a command. 1Tel = 1 means that 1 byte telegram has been received. The bit is reset on reading command register.
So we have a Valid reply and it is a one byte telegram. So read the "command" register to get this telegram.  
```
-r command
```
response:
```
received commands: [-r][command]
read:170(10101010)
done.
```
So, ballast physical minimum is 170. Notice that even if DALI permits 254 levels, that ballast cannot dim light under this value. Now if you read the status register, you should have all bits equal to 0, nothing left to do.
```
received commands: [-r][status]
BUS FAULT         0
BUSY              0
OVERRUN           0
FRAM ERROR        0
VALID REPLY       0
REPLY TIMEFRAME   0
2 BYTE TELEGRAM   0
1 BYTE TELEGRAM   0
read:0(00000000)
done.
```
### Address
There are 3 types of addresses:
* **-s [NUMBER]** short addresses: as DALI specification, each ballast can be reached with a single address from 0 up to 63. When this short address is not already set, ballast reacts only to broadcast commands. To assign this address see the example.
* **-g [NUMBER]** group addresses: from 0 up to 15. *Please refer to the DALI specification for details on the commands*
* **-b** broadcast: commands sent with a broadcast address will reach every ballast.

### DALI forward telegram
#### direct ARC command
**-d [ADDRESS] [LEVEL]**
```
-d -s 8 200
```
Command ballast with address 8 to 200 arc power level.
```
-d -b 0
```
Command all ballast to switch to 0 (off).
#### indirect command
**-i [ADDRESS] [COMMAND]**
```
-i -b 5
```
Set all ballast arc power levels to the "MAX LEVEL" without fading.
#### configuration command
**-c [ADDRESS] [COMMAND]**
```
-c -s 8 128
```
Tell ballast 8 to store DTR as its short address.
#### query command
**-q [ADDRESS] [COMMAND]**
```
-q -s 8 160
```
Ballast will response with actual arc power level. To read the response, see register reading specifications.
#### special command
**-x [COMMAND] [COMMAND]** *Please refer to the DALI specification for details on the commands*
