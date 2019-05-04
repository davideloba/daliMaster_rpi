# daliMaster

This is a Python3 library to control your DALI lamps with the brand new [daliMaster](https://www.ebay.it/itm/DALI-Master-hat-for-Raspberry-pi/254220148656?hash=item3b30b39fb0:g:LmwAAOSwNZxczZC9) hat for Raspberry Pi, with built-in DALI bus power supply system. B:boom::boom:m!

Are you looking for Arduino™ library and DALI shield? See [here](https://github.com/davideloba/daliMaster).

## Description

### What is DALI?

DALI (Digital Addressable Lighting Interface) is a powerful protocol to control lighting. Through DALI you can dimmer your led lamps, ask them status, recall a predefined scenario and so on. If you want more information about DALI you can find many useful links to the bottom of this page.

### Can I use DALI with my Raspberry Pi?

Well, the answer is YES.

### How?

With [daliMaster](https://www.ebay.it/itm/DALI-Master-hat-for-Raspberry-pi/254220148656?hash=item3b30b39fb0:g:LmwAAOSwNZxczZC9) hat! As the name suggests, that hat transforms your Raspberry Pi in a DALI master, acting as a bridge between I2C interface and DALI bus. Let's make an example to explain how it works.

## Getting Started

### Hardware stuff

* Turn your Raspberry Pi off.

* Fit [daliMaster](https://www.ebay.it/itm/DALI-Master-hat-for-Raspberry-pi/254220148656?hash=item3b30b39fb0:g:LmwAAOSwNZxczZC9) hat on your Raspberry Pi

* Make connections (you can find an example [here](https://))
  * Connect your lamps to their ballasts
  * Connect your ballasts to mains..be careful!
  * Connect your ballasts and [daliMaster](https://www.ebay.it/itm/DALI-Master-hat-for-Raspberry-pi/254220148656?hash=item3b30b39fb0:g:LmwAAOSwNZxczZC9) hat to DALI bus
  * Connect your 24V DC power supply to mains and to [daliMaster](https://www.ebay.it/itm/DALI-Master-hat-for-Raspberry-pi/254220148656?hash=item3b30b39fb0:g:LmwAAOSwNZxczZC9)..again, be careful!

* If I'm right, now you should have all lamps on.

* Turn your Raspberry Pi on.

### Software stuff

Enable I2C interface of your Raspberry Pi
```
sudo raspi-config
```
Select "Interfacing option">"I2C">"Yes" to enable the interface.
Then install the I2C utilities:
```
sudo apt-get update
sudo apt-get install python3-smbus i2c-tools
```
Now digit
```
sudo i2cdetect -y 1
```
and you should see something like that:
```
    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- 23 -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
If you see '23' (I2C address 0x23), your [daliMaster](https://www.ebay.it/itm/DALI-Master-hat-for-Raspberry-pi/254220148656?hash=item3b30b39fb0:g:LmwAAOSwNZxczZC9) is online: well done!


### Let's do something

Download this library and digit:
```
sudo python3 examples/shellControl/shellControl.py
```
Remember: "sudo" is needed because we are trying to access system resources such as I2C. Now you should see something like that:
```
I2C DALI master(0x23) begin..
PING I2C device 0x23..ok
device 0x23 is ready
Digit your command (press "Enter" to see all options):
```
Well, write and send this command:
```
-d -b 0
```
If everything went well your lamps now are off. But we don't like darkness, so let's switch them on to the minimum:
```
-d -b 1
```
Cool! Let's push them to maximum:
```
-d -b 254
```
Easy, isn't it? Now you can modulate all lamps from 0 up to 254 with those simple commands. :thumbsup:

## Next

See more informations about shell commands [here](/examples/shellControl/README.MD). See other examples to play with your lamps (try [Pulse.py](/examples/pulse)). See also the following links to know more about [daliMaster](https://www.ebay.it/itm/DALI-Master-hat-for-Raspberry-pi/254220148656?hash=item3b30b39fb0:g:LmwAAOSwNZxczZC9) and DALI.

## Useful links

### Raspberry Pi  and I2C Interface
* [raspberry-projects.com](https://raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2)

### DALI
* [main commands](https://www.acmesystems.it/www_raspberry/openhab_dali/dali_commands.pdf)
* DALI international standard (English/French) [60929 © IEC:2006](http://jnhb.fszjzx.com/upload/biaozhun/pdf/IEC60929Y2006.PDF)

### LW14
* [LW14 datasheet](https://www.codemercs.com/downloads/ledwarrior/LW14_Datasheet.pdf)

## This library is built With

* [Atom](https://atom.io/)

## Versioning

* v.1 First release April 2019

## Credits

See [credits.md](credits.md) file for details.
Raspberry Pi is a trademark of the Raspberry Pi Foundation.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
