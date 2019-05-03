#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import daliMaster
import defines
import time

master = daliMaster.daliMaster()

if master.begin() == defines.ERROR :
    quit()

daliAddress = master.getBroadcastAddress(defines.LW14_MODE_DACP)

while 1:

    for i in range(254, 150, -1):
        if (master.waitForReady() == defines.ERROR) or (master.directCmd(daliAddress, i) == defines.ERROR) :
            print("Error..")
        time.sleep(0.02)

    for i in range(150, 254):
        if (master.waitForReady() == defines.ERROR) or (master.directCmd(daliAddress, i) == defines.ERROR) :
            print("Error..")
        time.sleep(0.02)
