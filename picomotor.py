"""
Library to control the picomotor driver.
"""

import serial, time


class MSerial:
    axis_names = dict(x=0, y=1)
    unit = dict(x=1, y=1)
    
    def __init__(self, port, echo=True, max_retry=2, wait=0.1, sendwidget=None, recvwidget=None, **serial_kws):
        kws = dict(baudrate=19200, bytesize=serial.EIGHTBITS, 
                   parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
                   timeout=0, xonxoff=True, rtscts=False, dsrdtr=False)
        kws.update(serial_kws)
        self.serial = serial.Serial(port, **kws)
        self.echo = echo
        self.wait = wait
        self.sendwidget = sendwidget
        self.recvwidget = recvwidget

    def send(self, cmd):
        """Send a command to the picomotor driver."""
        line = cmd + '\r\n'
        retval = self.serial.write(bytes(line, encoding='ascii'))
        self.serial.flush()
        if self.echo:
            self.log(cmd, widget=self.sendwidget)
        return retval
    
    def readlines(self):
        """Read response from picomotor driver."""
        return ''.join([l.decode('ASCII') for l in self.serial.readlines()])
    
    def log(self, msg, widget=None):
        if widget is None:
            print(msg, flush=True)
        else:
            widget.value = msg
        
    def sendrecv(self, cmd):
        """Send a command and (optionally) printing the picomotor driver's response."""
        res = self.send(cmd) 
        if self.echo:
            time.sleep(self.wait)
            ret_str = self.readlines()
            self.log(ret_str, widget=self.recvwidget)
        return res

    def set_axis(self, axis, vel=None, acc=None, driver='a1'):
        """Set current axis ('x' or 'y') and (optionally) its velocity."""
        assert axis in self.axis_names
        fmt = dict(driver=driver, axis=self.axis_names[axis])
        basecmd = '{cmd} {driver} {axis}={value}'
        if acc is not None:
            assert 0 < acc <= 32000, 'Acceleration out of range (1..32000).'
            cmd = basecmd.format(cmd='ACC', value=acc, **fmt)
            self.sendrecv(cmd)
        if vel is not None:
            assert 0 < vel <= 2000, 'Velocity out of range (1..2000).'
            cmd = basecmd.format(cmd='VEL', value=vel, **fmt)
            self.sendrecv(cmd)
        cmd = 'chl {driver}={axis}'.format(**fmt)
        return self.sendrecv(cmd)

    def move_steps(self, steps, axis, vel=None, acc=None, driver='a1', go=True):
        """Send command to move `axis` of the given `steps`."""
        self.set_axis(axis, vel=vel, acc=acc, driver=driver)
        cmd = 'rel {driver}={steps}'.format(driver=driver, steps=steps)
        if go:
            cmd = cmd + ' g'
        return self.sendrecv(cmd)

    def move(self, units, axis, vel=None, acc=None, driver='a1', go=True):
        """Send command to move `axis` of the given `units`. 
        Uses self.unit for conversion.
        """
        steps = round(units * self.unit[axis])
        return self.move_steps(steps, axis, vel=None, acc=None, driver='a1', go=True)
    
    def go(self):
        """Send 'go' command to execute all previously sent move commands."""
        return self.sendrecv('go')
    
    def halt(self):
        """Send 'HAL' command to stop motion with deceleration."""
        return self.sendrecv('hal')
    
    def joystick_enable(self, enable=True):
        """Enable or disable the joystick."""
        cmd = 'JON' if enable else 'JOF'
        return self.sendrecv(cmd)

    def status_msg(self):
        """Return the driver status byte as an integer (see manual pag. 185)."""
        self.send('STA')
        time.sleep(self.wait)
        ret_str = self.readlines()
        if self.echo:
            self.log(repr(ret_str), widget=self.recvwidget)
        return ret_str
    
    def status(self):
        ret_str = self.status_msg()
        i = ret_str.find('A1=')
        if i >= 0:
            status = int(ret_str[i+5:i+7], 16)
        else:
            raise IOError("Received: '%s'" % ret_str)
        return status
    
    def is_moving(self):
        """Return True if motor is moving, else False."""
        status = self.status()
        return status & 0x01