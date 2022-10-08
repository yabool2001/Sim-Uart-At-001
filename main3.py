from pprint import pprint
import random
import serial
import serial.tools.list_ports
from lib.serial_ops import open_serial_ports, set_serials_cfg , close_serial_ports , open_serial_ports

com_name                        = "stlink"
#com_name                        = "cp210x"
stm32_request                   = "request"
python_answer                   = "answer answer"
error                           = b'$CMD ERR,CMD_NOTIMPLEMENTED*0d\n' 
p                               = 0

at_com = serial.Serial ()
set_serials_cfg ( at_com , com_name )
open_serial_ports ( at_com )

at_com.reset_input_buffer()
at_com.reset_output_buffer()

while True :
    rand1 = random.randrange ( 1 , 2 ) 
    frame = at_com.read ( 100 )
    if frame.decode('utf-8')[:7] == stm32_request :
        print ( f"STM32 sent AT command: {frame.decode('utf-8')}" )
        answer = f"{python_answer}"
        at_com.write ( answer.encode ( 'utf-8' ) )
        print ( f"Python sent answer: {answer.encode ( 'utf-8' )}" )
    if frame.decode('utf-8')[:6] == python_answer :
        print ( f"***STM32 transfer python answer: {frame.decode('utf-8')}" )
    if rand1 == random.randrange ( 1 , 2 )  :
        at_com.write ( error )
        print ( f"Python sent error: {error}" )

close_serial_ports ( at_com )