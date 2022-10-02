import platform
from pprint import pprint
import serial
import serial.tools.list_ports

def set_serials_cfg ( com , com_name ) :
    serial_ports =  serial.tools.list_ports.comports()
    for s_p in serial_ports:
        pprint ( s_p.description.lower () )
        if com_name.lower () in s_p.description.lower () :
            if platform.system () == "Windows":
                com.port = s_p.name
            elif platform.system () == "Linux":
                com.port = '/dev/' + s_p.name
            else:
                print ( f"Error: No compatible os!" )
    com.baudrate       = 115200
    com.bytesize       = serial.EIGHTBITS
    com.parity         = serial.PARITY_NONE
    com.stopbits       = serial.STOPBITS_ONE
    com.timeout        = 0.15
    com.write_timeout  = 0.15


def close_serial_ports ( *sp ) :
    for i in sp :
        if i.is_open :
            try:
                i.close ()
                print ( f"{i.name} port is closed" )
            except serial.SerialException as e :
                print ( f"{i.name} port closing error: {str(e)}" )

def open_serial_ports ( *sp ) :
    for i in sp :
        try: 
            i.open ()
            print ( f"{i.name} port opened" )
        except serial.SerialException as e :
            print ( f"{i.name} port error opening: {str(e)}" )