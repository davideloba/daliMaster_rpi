# @Author: davide
# @Date:   2019-04-25T10:46:54+02:00
# @Last modified by:   davide
# @Last modified time: 2019-04-25T18:33:46+02:00



import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import daliMaster
import defines
import time


master = daliMaster.daliMaster()

if master.begin() == defines.ERROR :
    quit()

userCommand = input('Digit your command (press "Enter" to see all options):')
commands = userCommand.split()
if len(commands) == 0 :
    print('choose one of these commands:')
    print('\t-a, set new I2C address')
    print('\t-r, read a register')
    print('\t-d, make a direct arc power conmmand')
    print('\t-i, make a indirect arc power conmmand')
    print('\t-i, make a configuration conmmand')
    print('\t-q, make a query to ballast')
    print('\t-x, make a special command')
    quit()
if len(commands) > 4 :
    quit('too many commands')

print("received commands: ", end = '')
for command in commands:
    print("[{0}]".format(command), end = '')
print('')

res = True

if commands[0] == "-a" : #-a [new i2c address] set new address to lw14

    if len(commands) < 2 :
        quit("too less commands")

    print("Setting {0} as new I2C address".format(commands[1]))

    if commands[1].find('x') :
        command = int(commands[1], 16)
    else :
        command = int(commands[1])

    if master.setNewAddress(command) == defines.ERROR :
        quit()

elif commands[0] == "-r" : #-r [reg address] read lw14 register

    if len(commands) < 2 :
        quit('specify "status", "command" or "signature"')

    res =  master.read(commands[1]);
    if not res == defines.ERROR :
        print("read:{0}({0:08b})".format(res))

else :
    if commands[0] == "-d" :
        mode = defines.LW14_MODE_DACP
    else :
        mode = defines.LW14_MODE_CMD

    if not commands[0] == "-x" : #do this just for non-special(x) cmd

        if commands[1] == "-s" :
            if len(commands) < 4 :
                quit("command too short")
            daliAddress = master.getShortAddress(int(commands[2]), mode)
            daliCmd = int(commands[3])
        elif commands[1] == "-b" :
            if len(commands) < 3 :
                quit("command too short")
            daliAddress = master.getBroadcastAddress(mode)
            daliCmd = int(commands[2])
        elif commands[1] == "-g" :
            if len(commands) < 4 :
                quit("command too short")
            daliAddress = master.getGroupAddress(int(commands[2]), mode)
            daliCmd = int(commands[3])
        else :
            quit("wrong recipient type")

    if commands[0] == "-d" :
        res = master.directCmd(daliAddress, daliCmd)
    elif commands[0] == "-i" :
        res = master.indirectCmd(daliAddress, daliCmd)
    elif commands[0] == "-c" :
        res = master.configCmd(daliAddress, daliCmd)
    elif commands[0] == "-q" :
        res = master.queryCmd(daliAddress, daliCmd)
        if not res == defines.ERROR :
            print("now you should read command reg to see the response")
    elif commands[0] == "-x" :
        res = master.directCmd(int(commands[1]), int(commands[2]))
    else :
        quit("wrong command")


if not res == defines.ERROR :
    print("done")
else :
    print("error")
