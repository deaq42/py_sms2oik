import serial
import os
import sys
import time
import hashlib
import requests
import urllib
SERVER_ADRESS = 'http://localhost/?query='
PHONE_NUM = {}   #Словарь в котором будут хранится данные об известных номерах и соответсвующий ТС. {'phone_number':'К:КП:Объект'}
commandkey='1234'

def oik_set_ts(ts_adress):       
    timestamp = str(time.time())
    timestamp = timestamp.split('.')
    timestamp = timestamp[0] + '000' #Готовим метку времени формата ОИК диспетчер
    str2 = f'!IP-gate@{commandkey}@{timestamp}!' #Готовим и солим хеш запроса
    sha_str = hashlib.sha256(str2.encode())
    #print (sha_str.hexdigest())
    #print (timestamp)
    #query_test='{%22id%22:%22test-client%22,%22query%22:%22test%22}'
    #print (urllib.parse.unquote(query_test))
    query2 = '{%22query%22:%20%22set-ts%22,%22ts%22:%20%22'+ts_adress+'%22,%20%20%22value%22:%201,%22hash%22:%20"'+sha_str.hexdigest()+'",%22timestamp%22:%20'+timestamp+'%20}' 
    print (urllib.parse.unquote(query2))
    #print (query.items())            
    full_url = SERVER_ADRESS + query2
    #responce = requests.get(SERVER_ADRESS, params = query)
    responce = requests.get(full_url)
    print (responce.text)
    print (responce.url)


def load_settings():
    f = open('settings.ini', 'r')
    tp_numbers = f.read().splitlines()
    #first = tp_numbers[0].split(';')
    f.close()
    print (len(tp_numbers))
    for number in tp_numbers:
        #number.split(';')
        PHONE_NUM[number[0:12]] = number[13:21]
        print (number[0:12])
    print (PHONE_NUM)
    #return tp_numbers
load_settings()

ser = serial.Serial('COM5', 115200, dsrdtr = 1,timeout = 0) #открываем порт
ser.write(bytes ('AT+CMGF=1 \r\n','utf8')) # #переводим режим ответетов в текст
time.sleep(0.2)
ser.write(bytes ('\f','utf8')) #Очищаем экран, не уверен что нужно
time.sleep(2)

def check_sms():
    ser.reset_output_buffer
    read_l = ser.read(600).decode('utf8').split(',')#Читаем данные из ком порта и разделяем их по запятой
    print (read_l[-1])
    #print (len(read_l[-1]))
    print ('------')
    #print (read_l[1])
    if read_l[-1].strip() == '1':#Если новое непрочитаное сообщение запускаем функцию реадсмс, добавить исключение если смс больше 1. надо перевести в int для сравнения
        print (read_l)    
        readsms(read_l[-1]) #Вызываем функцию реадсмс с аргументом в котором передается номер ячейки памяти с новым сообщением
    return read_l[-1]
def readsms(cell_n):
    command_read = bytes (f'AT+CMGR={cell_n} \r\n', 'utf8')   
    ser.write(command_read)
    time.sleep(0.5)
    sms = ser.read(600).decode('utf8').split("'")
    sms_str2_list = sms[0].split('"')
    sms_phone_number = sms_str2_list[3]
    sms_text = sms_str2_list[6].strip()
    
    sms_text = sms_text.split('\r')
    sms_time = sms_str2_list[5]
    time.sleep(0.5)
    ser.write(bytes ('AT+CMGDA="DEL INBOX" \r\n', 'utf8')) #Удалить смс все
    #print ('full_resp ')
    print (f'Номер телефона: {sms_phone_number}, этот номер должен изменить ТС {PHONE_NUM[sms_phone_number]}')
    print (f'Время {sms_time}')
    print (f'Сообщение {sms_text}')
    oik_set_ts(PHONE_NUM[sms_phone_number])
    str_2_log = f'{sms_phone_number};{PHONE_NUM[sms_phone_number]}{sms_time};{sms_text[0]} \n'#Довести до ума строку. удалить лишние символы в конце
    f_log = open('py_gsm_log.log', 'a')
    f_log.writelines(str_2_log)
    f_log.close
    #print ('Номер = ' + sms[2])
    #rint ('сообщение:' + sms[6])

    

#readsms(1)
while True:
    check_sms()

    time.sleep(2)
ser.close()