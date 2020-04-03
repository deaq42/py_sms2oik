import serial
import os
import sys
import time
import hashlib
import requests
import urllib
import sys
import argparse

SERVER_ADRESS = '' #+++
PHONE_NUM = {}   #Словарь в котором будут хранится данные об известных номерах и соответсвующий ТС. {'phone_number':'К:КП:Объект'}
COM_PORT = ''
COM_SPEED = ''
commandkey='' #ключ для соления хеша, задается в параметрах запуска оик_хттп_гейт

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', default='127.0.0.1')
    parser.add_argument('-p', '--port', default = 'none')
    parser.add_argument('-cc', '--comandkey', default = 'none') 
    parser.add_argument('-cs', '--comspeed', default = '115200')

    return parser
parser = createParser()
namespace = parser.parse_args(sys.argv[1:])
    # print (namespace)
if namespace.port == 'none':
    print ('Не задан ком порт')
    raise SystemExit
if namespace.comandkey == 'none':
    print ('не задан ключ управления ОИК!')
    raise SystemExit
SERVER_ADRESS = 'http://'+namespace.server+'/'
COM_PORT = namespace.port
commandkey = namespace.comandkey
COM_SPEED = namespace.comspeed
print ("Адрес сервера {}".format (SERVER_ADRESS) )
print ("КОМ ПОРТ {}".format (namespace.port) )
print ("КОМ ПОРТ СКОРОСТЬ {}".format (namespace.comspeed) )
print ("КЛЮЧ {}".format (namespace.comandkey) )


def load_settings():
    f = open('settings.ini', 'r')
    tp_numbers = f.read().splitlines()
    #first = tp_numbers[0].split(';')
    f.close()
    print (f'Количество записей в бд : {len(tp_numbers)}')
    for number in tp_numbers: #ТУТ ВЫЛЕТАЕТ ОШИБКА ЕСЛИ В БАЗЕ ТОЛЬКО ОДИН НОМЕР
        number = number.split(';')
        PHONE_NUM[number[0]] = number[1] #Сделать нормальный разбор по разделителям а не по количеству символов
        print (number[0:12])
    #print (PHONE_NUM)
    #return tp_numbers

    #Инициализация порта
load_settings()
try:
    ser = serial.Serial(COM_PORT, COM_SPEED, dsrdtr = 1,timeout = 0) #открываем порт
except:
    print (f'Невозоможно открыть {COM_PORT}')
    raise SystemExit
ser.write(bytes ('AT+CMGF=1 \r\n','utf8')) # #переводим режим ответетов в текст
time.sleep(0.2)
#ser.write(bytes ('\f','utf8')) #Очищаем экран, не уверен что нужно
time.sleep(2)
    #конец инициализации

def oik_set_ts(ts_adress):       
    timestamp = str(time.time())
    timestamp = timestamp.split('.')
    timestamp = timestamp[0] + '000' #Готовим метку времени формата ОИК диспетчер
    str2 = f'!IP-gate@{commandkey}@{timestamp}!' #Готовим и солим хеш запроса
    sha_str = hashlib.sha256(str2.encode())
    query2 = '?query={%22query%22:%20%22set-ts%22,%22ts%22:%20%22'+ts_adress+'%22,%20%20%22value%22:%201,%22hash%22:%20"'+sha_str.hexdigest()+'",%22timestamp%22:%20'+timestamp+'%20}' 
    print (urllib.parse.unquote(query2))
    #print (query.items())            
    full_url = SERVER_ADRESS + query2
    print (full_url)
    #responce = requests.get(SERVER_ADRESS, params = query)
    responce = requests.get(full_url)
    print (responce.text)
    print (responce.url)


def oik_switch_ts(ts_adress):
    timestamp = str(time.time())
    timestamp = timestamp.split('.')
    timestamp = timestamp[0] + '000' #Готовим метку времени формата ОИК диспетчер
    str2 = f'!IP-gate@{commandkey}@{timestamp}!' #Готовим и солим хеш запроса
    sha_str = hashlib.sha256(str2.encode())
    query2 = '?query={%22query%22:%20%22switch-ts%22,%22ts%22:%20%22'+ts_adress+'%22,%22hash%22:%20"'+sha_str.hexdigest()+'",%22timestamp%22:%20'+timestamp+'%20}'    
    full_url = SERVER_ADRESS + query2
    #responce = requests.get(SERVER_ADRESS, params = query)
    responce = requests.get(full_url)
    print (responce.text)
    print (responce.url)    



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
def check_at():
    ser.reset_output_buffer
    ser.write(bytes (f'AT\r\n', 'utf8'))
    read_l = ser.read(600).decode('utf8').split(',')#Читаем данные из ком порта и разделяем их по запятой
    #print ('AT')
    print (read_l[0])
    #print (len(read_l[-1]))
    print ('------')
    #print (read_l[1])

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
    print ('---\n Входящее сообщение!\n')
    if sms_phone_number in PHONE_NUM:
        print (f'Номер телефона: {sms_phone_number}, этот номер должен изменить ТС {PHONE_NUM[sms_phone_number]}')
        print (f'Время: {sms_time}')
        print (f'Текст сообщения: {sms_text[0]}')
        print ('\n')
    #Добавить условие наличия sms_phone_number в словаре PHONE_NUM
        oik_switch_ts(PHONE_NUM[sms_phone_number])
        str_2_log = f'{sms_phone_number};{PHONE_NUM[sms_phone_number]};{sms_time};{sms_text[0]} \n'#Генерируем строку для записи в файл лога
    else:
        print ('Номер не числится в базе!')
        print (f'Номер телефона: {sms_phone_number}, Отсутствует в базе! ОШИБКА!')
        print (f'Время: {sms_time}')
        print (f'Текст сообщения: {sms_text[0]}')
        print ('\n')
    str_2_log = f'{sms_phone_number};*UNKNOW NUBER*;{sms_time};{sms_text[0]} \n'#Генерируем строку с отсутвующим номером
    f_log = open('py_gsm_log.log', 'a')
    f_log.writelines(str_2_log)
    f_log.close
    #print ('Номер = ' + sms[2])
    #rint ('сообщение:' + sms[6])

    

#readsms(1)
a=0
while True:
    
    a=a+1
    check_sms()
    if a == 10:
        check_at()
        a = 0
    time.sleep(2)
ser.close()