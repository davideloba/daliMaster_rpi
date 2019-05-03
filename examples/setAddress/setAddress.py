#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import daliMaster
import defines
import dali

master = daliMaster.daliMaster()

if master.begin() == defines.ERROR :
    quit()

try:
    userSA = int(input('Digit dali address to set (0-63):'))
    master.checkRange(userSA, 0, 63)
except ValueError as e:
    print(e.args)
    quit()

print("This command will assign {0} as new address with a broadcasted command.".format(userSA))
print("Be sure that just one ballast will receive it.".format(userSA))


res = input('Continue? (digit "Y" for YES)')

if res == "Y" or res == "y" :

    # 60929 © IEC:2006
    # Only one ballast connected separately to the control unit for a simplified addressing method:
    # Send first the new short address (0AAA AAA1) by command 257 "DATA TRANSFER REGISTER (DTR)",
    # verify the content of the DTR and send command 128 "STORE DTR AS SHORT ADDRESS" two times.

    dtr = master.getShortAddress(userSA, defines.LW14_MODE_CMD) #DTR structure 0AAA AAA1
    broadcastAddr = master.getBroadcastAddress(defines.LW14_MODE_CMD);


    print("\n##### Store new address into DTR #####")

    if master.clean() == defines.ERROR or master.specialCmd(dali.DALI_STORE_TO_DTR, dtr) == defines.ERROR :
        quit("unable to set DTR!")

    if master.waitForIdle() == defines.ERROR :
        quit("Idle timeout!")


    print("\n##### Read DTR back and check it again #####")

    if master.clean() == defines.ERROR or master.queryCmd(broadcastAddr, dali.DALI_QUERY_CONTENT_DTR)== defines.ERROR :
        quit("unable to read DTR back!")

    if master.waitForTelegram_1() == defines.ERROR :
        quit()

    regVal = master.read("command")
    if not regVal == dtr :
        quit("DTR does not match! {0}:{1}").format(regVal, dtr)


    print("\n##### DTR and Address match! Now save as new address #####")

    if master.configCmd(broadcastAddr, dali.DALI_DTR_AS_SHORT_ADDRESS) == defines.ERROR :
        quit()

    if master.waitForIdle() == defines.ERROR :
        quit("Idle timeout!")


    print("\n##### Ask if there is a ballast with the given address that is able to communicate #####")

    shortAddress = master.getShortAddress(userSA, defines.LW14_MODE_CMD)
    if master.clean() == defines.ERROR or master.queryCmd(shortAddress, dali.DALI_QUERY_BALLAST) == defines.ERROR :
        quit()

    if master.waitForTelegram_1() == defines.ERROR :
        quit("response timeout!")

    if master.read("command") != defines.DALI_YES :
        quit()


    print("\n##### Well, now make it flash (just for fun)! #####")

    if master.indirectCmd(shortAddress, dali.DALI_OFF) == defines.ERROR :
        quit()

    if master.waitForReady() == defines.ERROR :
        quit()

    time.sleep(0.2)

    if master.indirectCmd(shortAddress, dali.DALI_MAX_LEVEL) == defines.ERROR :
        quit()


    print("\n##### New address assigned and verified. Done. #####")
else :
	quit('bye')
