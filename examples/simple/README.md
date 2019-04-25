# simple.py

Simple program that set one lamp with a direct arc command and query its actual level to confirm the right receiving of the message. Remember to change *DALISA* and *LEVEL* definitions according with your setup.

Note the use of those methods:

* **master.clean()**


Read 0x01 LW14 command register just to reset LW14 status register bits of incoming messages.
* **master.waitForReady()**


Wait for bit *LW14_STATUS_BUSY* and bit *LW14_STATUS_BUS_FAULT* of *0x00 LW14 STATUS REGISTER* to be '0'.
* **master.waitForTelegram_1()**


Wait for bit *LW14_STATUS_VALID* and bit *LW14_STATUS_1BYTE* of *0x01 LW14 COMMAND REGISTER* to be '1'. After that, a new message is available into command register.
