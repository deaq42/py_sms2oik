import serial
import os
import sys
import time
#открываем порт
ser = serial.Serial('COM5', 115200, dsrdtr = 1,timeout = 0) #открываем порт
ser.write(bytes ('AT+CMGF=1 \r\n','utf8'))
time.sleep(0.2)
ser.write(bytes ('\f','utf8'))
time.sleep(2)
# #переводим режим ответетов в текст
def check_sms():
    ser.reset_output_buffer
    read_l = ser.read(600).decode('utf8').split(',')
    print (read_l[-1])
    #print (len(read_l[-1]))
    print ('------')
    #print (read_l[1])
    if read_l[-1].strip() == '1':
        print (read_l)    
        readsms(read_l[-1])
    return read_l[-1]
def readsms(cell_n):
    command_read = bytes (f'AT+CMGR={cell_n} \r\n', 'utf8')
    
    ser.write(command_read)
    time.sleep(0.5)
    sms = ser.read(600).decode('utf8').split("'")
    sms_str2_list = sms[0].split('"')
    sms_phone_number = sms_str2_list[3]
    sms_text = sms_str2_list[6].strip()
    sms_text.split('OK')
    sms_time = sms_str2_list[5]
    time.sleep(0.5)
    ser.write(bytes ('AT+CMGDA="DEL INBOX" \r\n', 'utf8')) #Удалить смс все
    #print ('full_resp ')
    print (f'Номер телефона: {sms_phone_number}')
    print (f'Время {sms_time}')
    print (f'Сообщение {sms_text}')
    #print ('Номер = ' + sms[2])
    #rint ('сообщение:' + sms[6])

    

#readsms(1)
while True:
    check_sms()

    time.sleep(2)
ser.close()