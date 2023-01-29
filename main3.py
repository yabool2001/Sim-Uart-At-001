import datetime
from pprint import pprint
import random
import serial
import serial.tools.list_ports
from lib.serial_ops import open_serial_ports, set_serials_cfg , close_serial_ports , open_serial_ports

com_name                        = "stlink"
#com_name                        = "cp210x"
stm32_request                   = "request"
stm32_dbg                       = "DBG: "
python_answer                   = "answer answer"
error                           = b'$CMD ERR,CMD_NOTIMPLEMENTED*0d\n' 
eol                 	        = " "

at_com = serial.Serial ()
set_serials_cfg ( at_com , com_name )
open_serial_ports ( at_com )

at_com.reset_input_buffer()
at_com.reset_output_buffer()

while True :
    frame = at_com.read ( 100 )
    if frame.decode('utf-8')[:7] == stm32_request :
        ts = f"{datetime.datetime.utcnow ().strftime('%H:%M:%S.%f')}{eol}"
        print ( f"{ts}1. STM32 sent AT command: {frame.decode('utf-8')}" )
        answer = f"{python_answer}"
        at_com.write ( answer.encode ( 'utf-8' ) )
        ts = f"{datetime.datetime.utcnow ().strftime('%H:%M:%S.%f')}{eol}"
        print ( f"{ts}2. Python sent answer: {answer.encode ( 'utf-8' )}" )
    if frame.decode('utf-8')[:6] == python_answer[:6] :
        ts = f"{datetime.datetime.utcnow ().strftime('%H:%M:%S.%f')}{eol}"
        print ( f"{ts}3. ***STM32 transfer python answer: {frame.decode('utf-8')}" )
    if frame.decode('utf-8')[:5] == stm32_dbg :
        ts = f"{datetime.datetime.utcnow ().strftime('%H:%M:%S.%f')}{eol}"
        print ( f"{ts}STM32 {frame.decode('utf-8')}" )
    if random.randrange ( 1 , 2000 ) == 1 :
        ts = f"{datetime.datetime.utcnow ().strftime('%H:%M:%S.%f')}{eol}"
        at_com.write ( error )
        print ( f"{ts}Python sent error: {error}" )

close_serial_ports ( at_com )