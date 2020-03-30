import serial
import os
import sys
import time
#открываем порт
ser = serial.Serial('COM3', 9600, dsrdtr = 1,timeout = 0) #открываем порт
#ser.write(bytes ('AT+CMGF=1\r\n','utf8'))
time.sleep(2)
# #переводим режим ответетов в текст
def check_sms():
    read_l = ser.read(600).decode('utf8')
    if read_l[0] == '+':
        
    return read_l
def readsms(cell_n):
    command_read = bytes (f'AT+CMGR={cell_n}\r\n', 'utf8')
    
    ser.write(command_read)
    time.sleep(0.5)
    sms = ser.read(600).decode('utf8').split('"')

    print ('Номер = ' + sms[3])
    print ('сообщение:' + sms[6])

    ser.close()

#readsms()
while True:
    print (check_sms())

    time.sleep(2)