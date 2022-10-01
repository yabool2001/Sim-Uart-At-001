import datetime
from errno import EOVERFLOW
from pprint import pprint
from re import I
import serial
import serial.tools.list_ports
from lib.serial_ops import open_serial_ports, set_serials_cfg , close_serial_ports , open_serial_ports

data_com_delta_seconds          = 60*60*24
com_name                        = "stlink"
#com_name                        = "cp210x"
stm32_request                   = "request"
python_answer                   = "answer"
gn_mostrecent_at_comm	        = b'$GN @*67\n'
error                           = b'$CMD ERR,CMD_NOTIMPLEMENTED*0d\n' 
answer                          = b'$GN 52.2782,20.8089,84,359,2*2b\n'
eol                 	        = "\n"
p                               = 0

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
    if frame.decode('utf-8')[:7] == stm32_request :
        print ( f"STM32 sent AT command: {frame.decode('utf-8')}" )
        answer = f"{python_answer}{p+1}"
        at_com.write ( answer.encode ( 'utf-8' ) )
        print ( f"Python sent answer: {answer.encode ( 'utf-8' )}" )
        p += 1
    if frame.decode('utf-8')[:6] == python_answer :
        print ( f"***STM32 transfer python answer: {frame.decode('utf-8')}" )
    #if frame != b'' and frame.decode('utf-8')[:7] != stm32_request :
    #    print ( f"*** STM32 sent rx_buff: {frame}" )
    if min != datetime.datetime.utcnow().minute :
        at_com.write ( error )
        print ( f"Python sent error: {error}" )
        min = datetime.datetime.utcnow().minute

close_serial_ports ( at_com )