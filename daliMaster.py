import dali
import defines
import smbus
import time


class daliMaster:


    def __init__(self) :
        self.__address = 0
        self.__bus = 0
        try :
            self.__bus = smbus.SMBus(1)
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR


    def begin(self, toSet = defines.LW14_I2C_ADDRESS):

        '''
        Initialize daliMaster and check if there is any
        responding device with that address online
        '''

        try :
            address = self.__checkAddress(toSet)
            print ("I2C DALI master {0}({1}) begin..".format(address, hex(address)))
            self.checkRange(address, 1, 127)
            self.__address = address
            self.__ping()
        except ValueError as e :
            print(e.args)
            return defines.ERROR
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR
        else:
            print("Device {0}({1}) is ready".format(self.__address, hex(self.__address)))
            return True


    def setNewAddress(self, toSet):

        '''
        Save the new I2C address to the Address Register
        and check if device has got the new one
        '''

        try:
            address = self.__checkAddress(toSet)
            self.checkRange(address, 1, 127)
            data = [address, address ^ 0xFF] # the second byte must contain the value of the first byte XORed with $FF.

            print("Setting {0}({1}) as new I2C address".format(address, hex(address)))
            # print(":{0:08b}".format(data[0]))
            # print(":{0:08b}".format(0xFF))
            # print(":{0:08b}".format(data[1]))

            self.__i2cWrite(defines.LW14_REGISTERS["address"]["address"], data)
            time.sleep(1)
            self.__ping(address) #pass new address as argument to override default
            self.__address = address
        except ValueError as e :
            print(e.args)
            return defines.ERROR
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR
        else:
            return True


    def clean(self):

        '''
        Read once the command register just to set it free
        '''

        try:
            return self.__i2cRead(defines.LW14_REGISTERS["command"]["address"])
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR


    def waitForReady(self, timeout = defines.BUS_TIMEOUT):

        '''
        Wait for bits of "status busy" and "bus fault" to be 0
        '''

        try:
            # print("waiting for bus ready")
            return self.__waitFor(timeout, 0, defines.LW14_STATUS_BUSY,  defines.LW14_STATUS_BUS_FAULT)
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR


    def waitForTelegram_1(self, timeout = defines.BUS_TIMEOUT):

        '''
        Wait for bits of "status valid" and "status 1 byte" to be 1
        '''

        try:
            return self.__waitFor(timeout, 1, defines.LW14_STATUS_VALID,  defines.LW14_STATUS_1BYTE)
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR


    def waitForTelegram_2(self, timeout = defines.BUS_TIMEOUT):

        '''
        Wait for bits of "status valid" and "status 2 byte" to be 1
        '''

        try:
            return self.__waitFor(timeout, 1, defines.LW14_STATUS_VALID,  defines.LW14_STATUS_2BYTE)
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR


    def waitForIdle(self, timeout = defines.BUS_TIMEOUT):

        '''
        Wait until all bits of status reg are equal to 0
        '''

        try:
            return self.__waitFor(timeout, 0, 255, 255)
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR


    def directCmd(self, ballast, cmd):

        print("direct command function called ({0},{1})".format(ballast,cmd))

        try:
            self.checkRange(cmd, 0, defines.DALI_DEFAULT_MAX)
            self.__write(ballast, cmd)
        except ValueError as e:
            print(e.args)
            return defines.ERROR
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR
        else:
            return True


    def indirectCmd(self, ballast, cmd):

        print("indirect command function called ({0},{1})".format(ballast,cmd))

        try:
            self.checkRange(cmd, 0, 31)
            self.__write(ballast, cmd)
        except ValueError as e:
            print(e.args)
            return defines.ERROR
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR
        else:
            return True


    def configCmd(self, ballast, cmd):

        print("config command function called ({0},{1})".format(ballast,cmd))

        try:
            self.checkRange(cmd, 32, 128)
            self.__writeTwice(ballast, cmd)
        except ValueError as e:
            print(e.args)
            return defines.ERROR
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR
        else:
            return True


    def queryCmd(self, ballast, cmd):

        print("query command function called ({0},{1})".format(ballast,cmd))

        try:
            self.checkRange(cmd, 144, 196)
            self.__write(ballast, cmd)
        except ValueError as e:
            print(e.args)
            return defines.ERROR
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR
        else:
            return True


    def specialCmd(self, cmd_1, cmd_2):

        print("special command function called ({0},{1})".format(cmd_1,cmd_2))

        try:
            # self.checkRange(cmd, 161, 255)
            self.__write(cmd_1, cmd_2)
            return True
        except ValueError as e:
            print(e.args)
            return defines.ERROR
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR
        else:
            return True


    def read(self, regName):

        try:
            regAddress = self.__getRegAddress(regName,"r")
            read = self.__i2cRead(regAddress)
            if regName == "status" :
                self.__printStatusReg(read)
        except ValueError as e:
            print(e.args)
            return defines.ERROR
        except IOError as e :
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            return defines.ERROR
        else:
            return read


    def getBroadcastAddress(self, mode) :

        return (0xFE | mode)


    def getGroupAddress(self, group, mode) :

        return (0x80 | ((group & 16) << 1) | mode)


    def getShortAddress(self, ballast, mode) :

        return (((ballast & 63) << 1) | mode)


    def checkRange(self, checkMe, rangeMin, rangeMax) :

        if checkMe < rangeMin or checkMe > rangeMax:
            raise ValueError('value out of bounds', checkMe, rangeMin, rangeMax)
        return True


    #Private
    def __ping(self, address = None) :

        '''
        Perform quick transaction just to check if device is online.
        Throws IOError if unsuccessful.
        Take master.__address as default
        '''

        if address == None :
            address = self.__address
        print("Ping I2C device {0}({1})..".format(address, hex(address)), end = '')
        self.__bus.write_quick(address) #if it fails, will raise an IOError
        print("ok")


    def __checkAddress(self, toSet) :

        if isinstance(toSet, str) :
            if not toSet.find("x") == -1  or not toSet.find("X") == -1 :
                return int(toSet, 16)
            else :
                return int(toSet)
        return toSet


    def __getRegAddress(self, name, mode, data = []) :

        '''
        Check if the wanted register is compatible with mode and data length
        and if so, return the register address, otherwise raise an Exception
        '''

        #check if the register name is correct
        if not name in defines.LW14_REGISTERS :
            raise ValueError ("register name doesn't match the avaibles ones", name)

        #check if the mode is correct
        if defines.LW14_REGISTERS[name]['mode'].find(mode)  == -1 :
            raise ValueError ("mode doesn't match the avaibles ones", mode, defines.LW14_REGISTERS[name][mode])

        #check if the data length is correct
        if len(data) > defines.LW14_REGISTERS[name]['length'] :
            raise ValueError ('data is too long to write', len(data), defines.LW14_REGISTERS[name][length])

        return defines.LW14_REGISTERS[name]['address']


    def __waitFor(self, timeout, target = 0, first_mask = 255, second_mask = 255):

        previous = time.time()

        while (time.time() - previous) < timeout:

            status = self.__i2cRead(defines.LW14_REGISTERS["status"]["address"])
            # self.__printStatusReg(status)

            if target == 0: #wait for zero
                if status & first_mask == 0 and status & second_mask == 0:
                    # self.__printStatusReg(status)
                    return True
            else: #wait for greater than zero
                if status & first_mask > 0 and status & second_mask > 0:
                    # self.__printStatusReg(status)
                    return True

        print("timeout!")
        self.__printStatusReg(status)

        return defines.ERROR


    def __write(self, data_1, data_2):

        data = [data_1, data_2] #2 byte dali telegram
        regAddress = self.__getRegAddress("command","w", data)
        return self.__i2cWrite(regAddress, data)


    def __writeTwice(self, data_1, data_2):

        self.__write(data_1, data_2)
        if self.waitForReady(0.1) == defines.ERROR : #100ms should be the max interval between
            raise ValueError('timeout in double write!')
        self.__write(data_1, data_2)
        return True


    def __i2cWrite(self, reg_address, data):

        return self.__bus.write_i2c_block_data(self.__address, reg_address, data)


    def __i2cRead(self, reg_address):

        return self.__bus.read_byte_data(self.__address, reg_address)


    def __printStatusReg(self, data):

        bits = ["1 BYTE TELEGRAM", "2 BYTE TELEGRAM", "REPLY TIMEFRAME", "VALID REPLY", "FRAM ERROR", "OVERRUN\t", "BUSY\t", "BUS FAULT"]

        for i in range(8, 0, -1) :
            bit = data & (1 << (i-1))
            if bit > 1 :
                bit = 1
            print ('{0}'.format(bits[i-1]), end = '\t\t')
            print (bit)
        print("++++++++++++++++++++++++++")
