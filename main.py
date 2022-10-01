import datetime
from errno import EOVERFLOW
from pprint import pprint
import serial
import serial.tools.list_ports
from lib.serial_ops import open_serial_ports, set_serials_cfg , close_serial_ports , open_serial_ports

data_com_delta_seconds          = 60*60*24
com_name                        = "stlink"
#com_name                        = "cp210x"
gn_mostrecent_at_comm	        = b'$GN @*67\n'
error_at_answer                 = b'$CMD ERR,CMD_NOTIMPLEMENTED*0d\n' 
gn_mostrecent_answer	        = b'$GN 52.2782,20.8089,84,359,2*2b\n'
eol                 	        = "\n"

at_com = serial.Serial ()
set_serials_cfg ( at_com , com_name )
open_serial_ports ( at_com )

at_com.reset_input_buffer()
at_com.reset_output_buffer()

min = datetime.datetime.utcnow().minute
frame_read_time_up = datetime.datetime.utcnow () + datetime.timedelta ( seconds = data_com_delta_seconds )
while datetime.datetime.utcnow () < frame_read_time_up :
#while True :
    frame = at_com.read ( 100 )
    if frame == gn_mostrecent_at_comm :
        print ( f"STM32 sent AT command: {frame}" )
        expected_answer = f"{datetime.datetime.utcnow ().strftime('$GN %Y,%m,%d %H.%M.%S*2b')}{eol}"
        at_com.write ( expected_answer.encode('utf-8') )
        print ( f"Python sent expected_answer: {expected_answer.encode('utf-8')}" )
    if frame != b'' and frame != gn_mostrecent_at_comm:
        print ( f"*** STM32 sent rx_buff: {frame}" )
    #if min != datetime.datetime.utcnow().minute :
    #    at_com.write ( error_at_answer )
    #    print ( f"Python sent error: {error_at_answer}" )
    #    min = datetime.datetime.utcnow().minute

close_serial_ports ( at_com )