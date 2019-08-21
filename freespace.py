"""
Library to control the picomotor driver.
"""

import serial, time


class MSerial:
    axis_names = dict(x1=0, y1=1, x2=2, y2=3)
    unit = dict(x=1, y=1)
    
    def __init__(self, port, echo=True, max_retry=2, wait=0.1, sendwidget=None, recvwidget=None, **serial_kws):
        kws = dict(baudrate=9600, bytesize=serial.EIGHTBITS, 
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
    
    def set_accl(self, axis, acc=None):
        """"Set acceleration for channel(axis)"""
        assert axis in self.axis_names:
        fmt=dict(axis=self.axis_names[axis])
        basefmt='{axis} {cmd} {value}'
        if acc is not None: 
            assert 0 < acc <= 32000, 'Acceleration out of range!!'
            cmd=basefmt.format(cmd="AC", value=acc, **fmt)
        return self.sendrecv(cmd)
    
    def set_vel(self, axis, vel=None):
        """Set VElocity for channel(axis)"""
        assert axis in self.axis_names:
        fmt=dict(axis=self.axis_names[axis])
        basefmt='{axis} {cmd} {value}'
        if vel is not None: 
            assert 0 < vel <= 2000, 'Velocity out of range!!'
            cmd=basefmt.format(cmd="VA", value=vel, **fmt)
        return self.sendrecv(cmd)
            
    def set_home(self, axis, steps=None):
        """set home position for selected motor(channel)"""
        assert axis in self.axis_names:
        fmt=dict(axis=self.axis_names[axis])
        basefmt='{axis} {cmd} {value}'
        if steps is not None: 
            assert -423333 <= steps <= 423333, 'steps out of range!!'
            cmd=basefmt.format(cmd="DH", value=steps, **fmt)
        return self.sendrecv(cmd)
            
    def move_target(self, steps, axis):
        """Moves to target position"""
        assert axis in self.axis_names:
        fmt=dict(axis=self.axis_names[axis])
        basefmt='{axis} {cmd} {value}'
        if steps is not None: 
            assert -423333 <= steps <= 423333, 'steps out of range!!'
            cmd=basefmt.format(cmd="PA", value=steps, **fmt)
        return self.sendrecv(cmd)
            
    def move_rel(self, steps, axis):
        """Moves to relative position"""
        assert axis in self.axis_names:
        fmt=dict(axis=self.axis_names[axis])
        basefmt='{axis} {cmd} {value}'
        if steps is not None: 
            assert -423333 <= steps <= 423333, 'steps out of range!!'
            cmd=basefmt.format(cmd="PR", value=steps, **fmt)
        return self.sendrecv(cmd)
        
    def set_motor(self, axis, value):
        """set type of motor: 0=No motor, 1=Unknown, 2=Tiny, 3=Standard"""
        assert axis in self.axis_names:
        fmt=dict(axis=self.axis_names[axis])
        basefmt='{axis} {cmd} {value}'
        if value is not None: 
            assert 0 <= value <= 3, 'motor value out of range!!'
            cmd=basefmt.format(cmd="QM", value=value, **fmt)
        return self.sendrecv(cmd)
            
    def set_cont(self, driver='1'):
        """Set controller address, default=1, range= 1 to 31"""
        basefmt='{cmd} {value}'
        if driver is not None: 
            assert 1 <= driver <= 31, 'driver value out of range!!'
            cmd=basefmt.format(cmd="SA", value=driver, **fmt)
        return self.sendrecv(cmd)
            
    def rst(self):
        """reset controller parameters (Vel and acc)"""
        return self.sendrecv('RST')
    
    def rs(self):
        """reset controller parameters (Vel, acc and home position)"""
        return self.sendrecv('RS')
    
    def stop(self, axis):
        """Stop motion for an axis/motor"""
        assert axis in self.axis_names:
        fmt=dict(axis=self.axis_names[axis])
        basefmt='{axis} {cmd}' 
        cmd=basefmt.format(cmd="ST", **fmt)
        return self.sendrecv(cmd)
        
    def save(self):
        """save parameters to controller memory"""
        return self.sendrecv('SM')