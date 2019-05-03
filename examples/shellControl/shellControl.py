#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import daliMaster
import defines
import time

master = daliMaster.daliMaster()

masterAddress = defines.LW14_I2C_ADDRESS
if len(sys.argv) > 1 :
    masterAddress = sys.argv[1]

if master.begin(masterAddress) == defines.ERROR :
    quit()

while True :

    while True :
        userCommand = input('Digit your command (press "Enter" to see all options, "q" to exit):')
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
        elif commands[0] == "q" :
            quit("exit")
        else :
            break

    print("received commands: ", end = '')
    for command in commands:
        print("[{0}]".format(command), end = '')
    print('')

    res = True

    if len(commands) > 4 :
        res = defines.ERROR
        print("command too long")

    if res != defines.ERROR and commands[0] == "-a" :

        if len(commands) < 2 :
            res = defines.ERROR
            print("error: command too short, specify new address.")
        else :
            res = master.setNewAddress(command)

    elif res != defines.ERROR and commands[0] == "-r" :

        if len(commands) < 2 :
            res = defines.ERROR
            print('error: command too short, specify register: "status", "command" or "signature".')
        else :
            res =  master.read(commands[1]);
            if not res == defines.ERROR :
                print("read:{0}({0:08b})".format(res))

    elif res != defines.ERROR :

        if commands[0] == "-d" :
            mode = defines.LW14_MODE_DACP
        else :
            mode = defines.LW14_MODE_CMD

        if not commands[0] == "-x" :

            if commands[1] == "-s" :
                if len(commands) < 4 :
                    res = defines.ERROR
                    print("error: command too short.")
                else :
                    daliAddress = master.getShortAddress(int(commands[2]), mode)
                    daliCmd = int(commands[3])
            elif commands[1] == "-b" :
                if len(commands) < 3 :
                    res = defines.ERROR
                    print("error: command too short.")
                else :
                    daliAddress = master.getBroadcastAddress(mode)
                    daliCmd = int(commands[2])
            elif commands[1] == "-g" :
                if len(commands) < 4 :
                    res = defines.ERROR
                    print("error: command too short.")
                else :
                    daliAddress = master.getGroupAddress(int(commands[2]), mode)
                    daliCmd = int(commands[3])
            else :
                res = defines.ERROR
                print("error: wrong recipient type.")

        if not res == defines.ERROR :
            if commands[0] == "-d" :
                res = master.directCmd(daliAddress, daliCmd)
            elif commands[0] == "-i" :
                res = master.indirectCmd(daliAddress, daliCmd)
            elif commands[0] == "-c" :
                res = master.configCmd(daliAddress, daliCmd)
            elif commands[0] == "-q" :
                res = master.queryCmd(daliAddress, daliCmd)
                if not res == defines.ERROR :
                    print("(now you should read command register to see the response)")
            elif commands[0] == "-x" :
                res = master.directCmd(int(commands[1]), int(commands[2]))
            else :
                res = defines.ERROR
                print("error: wrong command.")


    if not res == defines.ERROR :
        print("done.")

    print("")
