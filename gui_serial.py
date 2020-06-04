import time
import serial

port = "COM3"
boudrate = 9600

def import_module(module_name):
    serial_write("import sys", 0)
    serial_write("del sys.modules['{}']".format(module_name), 0)
    time.sleep(0.1)
    serial_write("import {}".format(module_name), 0)
    time.sleep(0.1)

def serial_write(command, timeout=1):
    """
        Parameters
        ----------
        command : str
            python command to execute on a microcontroller
        
        timeout : int (float supported)
            read timeout in seconds
    """

    if timeout == None:
        # Do not allow "wait forever"
        timeout = 0

    with serial.Serial(port, boudrate, timeout=timeout) as ser:
      #  print(command)
        # Sending a command
        ser.write('{}\r'.format(command).encode())
        
        output = ser.read_until("0xDEADBEEF".encode())
        lines = output.decode().split("\r\n")

        # drop first and last lines. first is command itself, last is deadbeef
        ret = lines[1:-1]
        
        return ret
