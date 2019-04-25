# @Author: davide
# @Date:   2018-02-18T10:54:08+01:00
# @Last modified by:   davide
# @Last modified time: 2019-04-25T15:26:53+02:00



import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import daliMaster
import defines
import dali
import time


DALISA = 7 #set your ballast address
LEVEL = 254 #set wanted level

master = daliMaster.daliMaster()

if master.begin() == defines.ERROR :
    quit()

print("\n##### Set lamp {0} to {1} #####".format(DALISA, LEVEL))

shortAddress = master.getShortAddress(DALISA, defines.LW14_MODE_DACP);

if master.waitForReady() == defines.ERROR or master.directCmd(shortAddress, LEVEL) == defines.ERROR :
    quit('error')

print("\n##### Now ask lamp level #####")
time.sleep(1) #wait a moment

shortAddress = master.getShortAddress(DALISA, defines.LW14_MODE_CMD);

if master.clean() == defines.ERROR :
    quit('error')

if master.waitForReady() == defines.ERROR  or master.queryCmd(shortAddress, dali.DALI_QUERY_ACTUAL_LEVEL) == defines.ERROR :
    quit('error')

if master.waitForTelegram_1() == defines.ERROR :
    quit('error')

res = master.read("command")

if res == defines.ERROR :
    quit('error')

print("\n##### Actual lamp level is {0}. Done. #####".format(res))
