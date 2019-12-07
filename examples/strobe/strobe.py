#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import daliMaster
import dali
import defines
import time

master = daliMaster.daliMaster()

if master.begin() == defines.ERROR :
    quit()

daliAddress = master.getBroadcastAddress(defines.LW14_MODE_DACP)

while 1:


    if (master.waitForReady() == defines.ERROR) or (master.indirectCmd(daliAddress, dali.DALI_OFF) == defines.ERROR) :
        print("Error..")
    time.sleep(0.2)


    if (master.waitForReady() == defines.ERROR) or (master.indirectCmd(daliAddress, dali.DALI_MAX_LEVEL) == defines.ERROR) :
        print("Error..")
    time.sleep(0.2)
