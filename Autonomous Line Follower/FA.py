"""Formula AllCode Robot Buggy functions"""


import time
import serial as _serial
import sys as _sys
from sys import platform as _platform


if _platform == "win32":
    if (_sys.version_info.major == 2):
        import _winreg as _winreg
    else:
        import winreg as _winreg


class Create:
    __ser = _serial.Serial()
    __verbose = 0
    
    def __init__(self):
        self.__ser.close()
        return;
    
    def ComOpen(self, port):
        """Open a communication link to the robot

        Args:
            port: The COM port to open
        """
        
        if _platform == "linux" or _platform == "linux2":
            # linux
            s = '/dev/rfcomm{0}'.format(port)
        elif _platform == "darwin":
            # MAC OS X
            print("Error - MAC OS TODO")
        elif _platform == "win32":
            # Windows
            s = '\\\\.\\COM{0}'.format(port)
        else:
            print("Error - unsupported platform")

        self.__ser = _serial.Serial(port=s,\
                            baudrate=115200,\
                            parity=_serial.PARITY_NONE,\
                            stopbits=_serial.STOPBITS_ONE,\
                            bytesize=_serial.EIGHTBITS,\
                            timeout=1)
        #TODO: add checking to ensure port is open
        return;

    def ComClose(self):
        """Close the communication link to the robot
        """
        self.__ser.close()
        return;

##    def _comlist(self):
##        #TODO: this is Windows-only at the moment
##        if _platform == "win32":
##            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\\DEVICEMAP\\SERIALCOMM')
##            i = 0
##            while True:
##                try:
##                    name = _winreg.EnumValue(key, i)[1][3:]
##                except OSError:
##                    #no more COM ports
##                    break
##                yield name #, '\\\\.\\{0}'.format(name)
##                i += 1
##
##            _winreg.CloseKey(key)
        
##    def ComQuery(self, port):
##        #TODO
##        comlist = self._comlist()
##        print (comlist)
##        return;
##
##    def ComFindFirst(self):
##        #TODO
##        return;

##    def Test(self):
##        #TODO: this is Windows-only at the moment
##        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\\DEVICEMAP\\SERIALCOMM')
##        i = 0
##        while True:
##            try:
##                name = _winreg.EnumValue(key, i)[1][3:]
##            except OSError:
##                #no more COM ports
##                break
##            yield name #, '\\\\.\\{0}'.format(name)
##            i += 1
##
##        _winreg.CloseKey(key)


    def _readval(self, cmd, loop_max):
        r = -1
        loop = 0
        while (loop < loop_max):
            try:
                r = int(self.__ser.readline().rstrip())
                if (self.__verbose != 0):
                    msg = '{0}: {1}'.format(cmd, r)
                    print(msg)
                loop = loop_max + 1   #break out of loop
            except ValueError:
                if (self.__verbose != 0):
                    msg = '{0}: No return({1})'.format(cmd,loop)
                    print(msg)
            loop = loop + 1
        return(r);

    def _flush(self):
        count = self.__ser.in_waiting
        while (count > 0):
            self.__ser.readline().rstrip()
            count = self.__ser.in_waiting
        return;

    def _set_verbose(self, value):
        self.__verbose = value
        return;

    
    
    def GetAPIVersion(self):
        """Retrieves the API version from the robot

        Returns:
            int: The API version in the robot
        """
        self._flush()
        s = 'GetAPIVersion\n'
        self.__ser.write(s.encode())
        r = self._readval("GetAPIVersion", 1)
        return(r);


        

    def ReadSwitch(self, index):
        """Read the switch value

        Args:
            index: 0 (left) or 1 (right)

        Returns:
            int: 0 (false) or 1 (true)
        """
        self._flush()
        s = 'ReadSwitch {0}\n'.format(int(index))
        self.__ser.write(s.encode())
        r = self._readval("ReadSwitch", 1)
        return(r);

    def ReadIR(self, index):
        """Read the IR value

        Args:
            index: IR sensor to query (0 to 7)

        Returns:
            int: Value of IR sensor (0 to 4095)
        """
        self._flush()
        s = 'ReadIR {0}\n'.format(int(index))
        self.__ser.write(s.encode())
        r = self._readval("ReadIR", 1)
        return(r);

    def ReadLine(self, index):
        """Read the line sensor value

        Args:
            index: Line sensor to query (0 to 1)

        Returns:
            int: Value of Line sensor (0 to 4095)
        """
        self._flush()
        s = 'ReadLine {0}\n'.format(int(index))
        self.__ser.write(s.encode())
        r = self._readval("ReadLine", 1)
        return(r);

    def ReadLight(self):
        """Read the light sensor value

        Returns:
            int: Value of light sensor (0 to 4095)
        """
        self._flush()
        s = 'ReadLight\n'
        self.__ser.write(s.encode())
        r = self._readval("ReadLight", 1)
        return(r);

    def ReadMic(self):
        """Read the microphone sensor value

        Returns:
            int: Value of microphone sensor (0 to 4095)
        """
        self._flush()
        s = 'ReadMic\n'
        self.__ser.write(s.encode())
        r = self._readval("ReadMic", 1)
        return(r);

    def ReadAxis(self, index):
        """Read the axis value of the accelerometer

        Args:
            index: Axis to query (0 to 3)

        Returns:
            int: Value of accelerometer axis (-32768 to 32767)
        """
        self._flush()
        s = 'ReadAxis {0}\n'.format(int(index))
        self.__ser.write(s.encode())
        r = self._readval("ReadAxis", 1)
        return(r);



    def SetMotors(self, left, right):
        """Set the motors speed

        Args:
            left: value of left motor (0 to 100)
            right: value of right motor (0 to 100)
        """
        s = 'SetMotors {0} {1}\n'.format(int(left),int(right))
        self.__ser.write(s.encode())
        return;

    def Forwards(self, distance):
        """Set the robot moving forward

        Args:
            distance: distance to move (0 to 1000) in mm
        """
        self._flush()
        s = 'Forwards {0}\n'.format(int(distance))
        self.__ser.write(s.encode())
        timeout = abs(int(distance / 50))
        if (timeout <= 0):
            timeout = 1
        r = self._readval("Forwards", timeout)
        return(r);

    def Backwards(self, distance):
        """Set the robot moving backwards

        Args:
            distance: distance to move (0 to 1000) in mm
        """
        self._flush()
        s = 'Backwards {0}\n'.format(int(distance))
        self.__ser.write(s.encode())
        timeout = abs(int(distance / 50))
        if (timeout <= 0):
            timeout = 1
        r = self._readval("Backwards", timeout)
        return(r);

    def Left(self, angle):
        """Set the robot to turn left

        Args:
            angle: angle to rotate (0 to 360) in degrees
        """
        self._flush()
        s = 'Left {0}\n'.format(int(angle))
        self.__ser.write(s.encode())
        timeout = abs(int(angle / 45))
        if (timeout <= 0):
            timeout = 1
        r = self._readval("Left", timeout)
        return(r);

    def Right(self, angle):
        """Set the robot to turn right

        Args:
            angle: angle to rotate (0 to 360) in degrees
        """
        self._flush()
        s = 'Right {0}\n'.format(int(angle))
        self.__ser.write(s.encode())
        timeout = abs(int(angle / 45))
        if (timeout <= 0):
            timeout = 1
        r = self._readval("Right", timeout)
        return(r);

    

    def LEDWrite(self, value):
        """Set the value of the LEDs

        Args:
            value: Value to set the LEDS (0 to 255)
        """
        s = 'LEDWrite {0}\n'.format(int(value))
        self.__ser.write(s.encode())
        return;

    def LEDOn(self, index):
        """Turn an LED on

        Args:
            index: The LED to turn on (0 to 7)
        """
        s = 'LEDOn {0}\n'.format(int(index))
        self.__ser.write(s.encode())
        return;

    def LEDOff(self, index):
        """Turn an LED off

        Args:
            index: The LED to turn off (0 to 7)
        """
        s = 'LEDOff {0}\n'.format(int(index))
        self.__ser.write(s.encode())
        return;

    def PlayNote(self, note, length):
        """Play a note on the speaker

        Args:
            note: The frequency of the note (1 to 10000) in Hz
            length: The duration of the note (1 to 10000) in ms
        """
        s = 'PlayNote {0} {1}\n'.format(int(note),int(length))
        self.__ser.write(s.encode())
        time.sleep(length/1000)
        return;
        
    def GetBattery():
        s = 'GetBattery\n'
        self.__ser.write(s.encode())
        r = self._readval("Battery", timeout)
        return(r);
    
    def ExpDDR(bitnumber,direction):
        s = 'ExpDDR {0} {1}\n'.format(bitnumber,direction)
        self.__ser.write(s.encode())
        return;
     
    def ExpRead(bitnumber):
        s = 'ExpRead {0}\n'.format(bitnumber)
        self.__ser.write(s.encode())
        r = self._readval("Bit", timeout)
        return(r);
        
    def ExpWrite(bitnumber,value):
        s = 'ExpWrite {0} {1}\n'.format(bitnumber,value)
        self.__ser.write(s.encode())
        return;
        
    def ExpAn(annumber):
        s = 'ExpAn {0}\n'.format(annumber)
        self.__ser.write(s.encode())
        r = self._readval("An", timeout)
        return(r);

##    #blocking...
##    def PlayNote(self, note, time):
##        self._flush()
##        s = 'PlayNote {0} {1}\n'.format(int(note),int(time))
##        self.__ser.write(s.encode())
##        timeout = abs(int(time / 1000))
##        if (timeout <= 0):
##            timeout = 1
##        r = self._readval("PlayNote", timeout)
##        return;


    def ServoEnable(self, index):
        """Enable a servo motor

        Args:
            index: The servo to control (0 to 3)
        """
        s = 'ServoEnable {0}\n'.format(int(index))
        self.__ser.write(s.encode())
        return;

    def ServoDisable(self, index):
        """Disable a servo motor

        Args:
            index: The servo to control (0 to 3)
        """
        s = 'ServoDisable {0}\n'.format(int(index))
        self.__ser.write(s.encode())
        return;

    def ServoSetPos(self, index, position):
        """Move a servo immediately to a position

        Args:
            index: The servo to control (0 to 3)
            position: The position of the servo (0 to 255)
        """
        s = 'ServoSetPos {0} {1}\n'.format(int(index),int(position))
        self.__ser.write(s.encode())
        return;

    def ServoAutoMove(self, index, position):
        """Auto-move a servo to a position

        Args:
            index: The servo to control (0 to 3)
            position: The position of the servo (0 to 255)
        """
        s = 'ServoAutoMove {0} {1}\n'.format(int(index),int(position))
        self.__ser.write(s.encode())
        return;

    def ServoMoveSpeed(self, speed):
        """Set the auto-move speed

        Args:
            speed: The servo speed (1 to 50)
        """
        s = 'ServoMoveSpeed {0}\n'.format(int(speed))
        self.__ser.write(s.encode())
        return;





    def LCDClear(self):
        """Clear the LCD
        """
        s = 'LCDClear\n'
        self.__ser.write(s.encode())
        return;

    def LCDPrint(self, x, y, text):
        """Display text on the LCD

        Args:
            x: The x-coordinate (0 to 127)
            y: The y-coordinate (0 to 31)
            text: The text to display
        """
        s = 'LCDPrint {0} {1} {2}\n'.format(int(x),int(y),text)
        self.__ser.write(s.encode())
        return;

    def LCDNumber(self, x, y, value):
        """Display a number on the LCD

        Args:
            x: The x-coordinate (0 to 127)
            y: The y-coordinate (0 to 31)
            value: The number to display (-32768 to 32767)
        """
        s = 'LCDNumber {0} {1} {2}\n'.format(int(x),int(y),int(value))
        self.__ser.write(s.encode())
        return;

    def LCDPixel(self, x, y, state):
        """Display a pixel on the LCD

        Args:
            x: The x-coordinate (0 to 127)
            y: The y-coordinate (0 to 31)
            state: 0 (off) or 1 (on)
        """
        s = 'LCDPixel {0} {1} {2}\n'.format(int(x),int(y),int(state))
        self.__ser.write(s.encode())
        return;

    def LCDLine(self, x1, y1, x2, y2):
        """Display a line on the LCD between points A and B

        Args:
            x1: The x-coordinate of point A (0 to 127)
            y1: The y-coordinate of point A (0 to 31)
            x2: The x-coordinate of point B (0 to 127)
            y2: The y-coordinate of point B (0 to 31)
        """
        s = 'LCDLine {0} {1} {2} {3}\n'.format(int(x1),int(y1),int(x2),int(y2))
        self.__ser.write(s.encode())
        return;

    def LCDRect(self, x1, y1, x2, y2):
        """Display a rectangle on the LCD between points A and B

        Args:
            x1: The x-coordinate of point A (0 to 127)
            y1: The y-coordinate of point A (0 to 31)
            x2: The x-coordinate of point B (0 to 127)
            y2: The y-coordinate of point B (0 to 31)
        """
        s = 'LCDRect {0} {1} {2} {3}\n'.format(int(x1),int(y1),int(x2),int(y2))
        self.__ser.write(s.encode())
        return;

    def LCDBacklight(self, value):
        """Control the backlight of the display

        Args:
            value: The brightness of the backlight (0 to 100)
        """
        s = 'LCDBacklight {0}\n'.format(int(value))
        self.__ser.write(s.encode())
        return;

    def LCDOptions(self, foreground, background, transparent):
        """Set the options for the display

        Args:
            foreground: The foreground colour, 0 (white) or 1 (black)
            background: The background colour, 0 (white) or 1 (black)
            transparent: The transparency, 0 (false) or 1 (true)
        """
        s = 'LCDOptions {0} {1} {2}\n'.format(int(foreground), int(background), int(transparent))
        self.__ser.write(s.encode())
        return;

    def _LCDVerbose(self, value):
        s = 'LCDVerbose {0}\n'.format(int(value))
        self.__ser.write(s.encode())
        return;



    def CardInit(self):
        self._flush()
        s = 'CardInit\n'
        self.__ser.write(s.encode())
        r = self._readval("CardInit", 2)
        return(r);

    def CardCreate(self, filename):
        self._flush()
        s = 'CardCreate {0}\n'.format(filename)
        self.__ser.write(s.encode())
        r = self._readval("CardCreate", 2)
        return(r);

    def CardOpen(self, filename):
        self._flush()
        s = 'CardOpen {0}\n'.format(filename)
        self.__ser.write(s.encode())
        r = self._readval("CardOpen", 2)
        return(r);

    def CardDelete(self, filename):
        self._flush()
        s = 'CardDelete {0}\n'.format(filename)
        self.__ser.write(s.encode())
        r = self._readval("CardDelete", 2)
        return(r);

    def CardWriteByte(self, data):
        #self._flush()
        s = 'CardWriteByte {0}\n'.format(int(data))
        self.__ser.write(s.encode())
        #r = self._readval("CardWriteByte", 2)
        return();

    def CardReadByte(self):
        self._flush()
        s = 'CardReadByte\n'
        self.__ser.write(s.encode())
        r = self._readval("CardReadByte", 2)
        return(r);

    def CardRecordMic(self, bitdepth, samplerate, time, filename):
        self._flush()
        s = 'CardRecordMic {0} {1} {2} {3}\n'.format(int(bitdepth),int(samplerate),int(time),filename)
        self.__ser.write(s.encode())
        r = self._readval("CardRecordMic", time+1)
        return(r);

    def CardPlayback(self, filename):
        self._flush()
        s = 'CardPlayback {0}\n'.format(filename)
        self.__ser.write(s.encode())
        r = self._readval("CardPlayback", 50)
        return(r);

    def CardBitmap(self, x, y, filename):
        self._flush()
        s = 'CardBitmap {0} {1} {2}\n'.format(int(x),int(y),filename)
        self.__ser.write(s.encode())
        r = self._readval("CardBitmap", 5)
        return(r);




    
