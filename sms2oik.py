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
    parser.add_argument('-s', '--server', default='172.18.49.4:952')
    parser.add_argument('-p', '--port', default = 'COM4')
    parser.add_argument('-cc', '--comandkey', default = '1234') 
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

def del_inb_mess():
    ser.write(bytes ('AT+CMGDA="DEL INBOX" \r\n', 'utf8')) #Удалить смс все

try:
    ser = serial.Serial(COM_PORT, COM_SPEED, dsrdtr = 1,timeout = 0) #открываем порт
except:
    print (f'Невозоможно открыть {COM_PORT}')
    raise SystemExit
ser.write(bytes ('AT+CMGF=1 \r\n','utf8')) # #переводим режим ответетов в текст
time.sleep(0.2)
#ser.write(bytes ('\f','utf8')) #Очищаем экран, не уверен что нужно
ser.write(bytes ('AT+CMGDA="DEL INBOX" \r\n', 'utf8'))
time.sleep(0.2)
print (ser.read(300).decode('utf8'))
time.sleep(2)
    #конец инициализации

def oik_set_ts(ts_adress, val):       
    timestamp = str(time.time())
    timestamp = timestamp.split('.')
    timestamp = timestamp[0] + '000' #Готовим метку времени формата ОИК диспетчер
    str2 = f'!IP-gate@{commandkey}@{timestamp}!' #Готовим и солим хеш запроса
    sha_str = hashlib.sha256(str2.encode())
    query2 = '?query={%22query%22:%20%22set-ts%22,%22ts%22:%20%22'+ts_adress+'%22,%20%20%22value%22:%20'+str(val)+',%22hash%22:%20"'+sha_str.hexdigest()+'",%22timestamp%22:%20'+timestamp+'%20}' 
    print (urllib.parse.unquote(query2))
    #print (query.items())            
    full_url = SERVER_ADRESS + query2
    #print (full_url)    
    responce = requests.get(full_url)
    print (responce.text)
    print (responce.url)

def oik_set_ti(ts_adress, val):       
    timestamp = str(time.time())
    timestamp = timestamp.split('.')
    timestamp = timestamp[0] + '000' #Готовим метку времени формата ОИК диспетчер
    str2 = f'!IP-gate@{commandkey}@{timestamp}!' #Готовим и солим хеш запроса
    sha_str = hashlib.sha256(str2.encode())
    query2 = '?query={%22query%22:%20%22set-ti%22,%22ti%22:%20%22'+ts_adress+'%22,%20%20%22value%22:%20'+str(val)+',%22hash%22:%20"'+sha_str.hexdigest()+'",%22timestamp%22:%20'+timestamp+'%20}' 
    print (urllib.parse.unquote(query2))
    #print (query.items())            
    full_url = SERVER_ADRESS + query2
    #print (full_url)    
    responce = requests.get(full_url)
    print (responce.text)
    print (responce.url)

def oik_switch_ts(ts_adress):
    timestamp = str(time.time())
    timestamp = timestamp.split('.')
    timestamp = timestamp[0] + '000' #Готовим метку времени формата ОИК диспетчер
    str2 = f'!IP-gate@{commandkey}@{timestamp}!' #Готовим и солим хеш запроса
    sha_str = hashlib.sha256(str2.encode())
    print (ts_adress)
    query2 = '?query={%22query%22:%20%22switch-ts%22,%22ts%22:%20%22'+ts_adress+'%22,%22hash%22:%20"'+sha_str.hexdigest()+'",%22timestamp%22:%20'+timestamp+'%20}'    
    full_url = SERVER_ADRESS + query2
    print (full_url)
    responce = requests.get(full_url)
    print (responce.text)
    print (responce.url)    



def check_sms():
    ser.reset_output_buffer
    ser.write(bytes (f'\r\n', 'utf8'))
    time.sleep(0.01)
    read_l = ser.read(800).decode('utf8').split(',')#Читаем данные из ком порта и разделяем их по запятой
    print (read_l[-1])
    #print (len(read_l[-1]))
    print ('------')
    #print (read_l[1])
    
    co = read_l[-1].strip()
    if co.isdigit() == True:
        str_int = int(co)
        if str_int >= 1 :#Если новое непрочитаное сообщение запускаем функцию реадсмс, добавить исключение если смс больше 1. надо перевести в int для сравнения
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
    ser.reset_output_buffer
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
    ser.write(bytes (f'AT+CMGD={cell_n} \r\n', 'utf8')) #Удалить смс все
    #print ('full_resp ')
    print ('---\n Входящее сообщение!\n')
    if sms_phone_number in PHONE_NUM:
        print (f'Номер телефона: {sms_phone_number}, этот номер должен изменить ТС {PHONE_NUM[sms_phone_number]}')
        print (f'Время: {sms_time}')
        encoded_text = str(sms_text[0])
        print (f'Текст сообщения: {encoded_text}')
        print ('\n')
        ts_end = linetroll_decode(encoded_text)
        print (len(ts_end))
        if ts_end:
            if ts_end == 'ok': #если ответ лайнтролла ОК то сбрасываем все 4 тс в ноль
                oik_set_ts(PHONE_NUM[sms_phone_number]+'1', 0)
                time.sleep(1)
                oik_set_ts(PHONE_NUM[sms_phone_number]+'2', 0)
                time.sleep(1)
                oik_set_ts(PHONE_NUM[sms_phone_number]+'3', 0)
                time.sleep(1)
                oik_set_ts(PHONE_NUM[sms_phone_number]+'4', 0)
                time.sleep(1)
                str_2_log = f'{sms_phone_number};{PHONE_NUM[sms_phone_number]};{sms_time};{sms_text[0]} Лайнтролл ОК \n'#Генерируем строку для записи в файл лога ИЗМЕНИТЬ
            
            elif len(ts_end) == 2:    
                for t in ts_end:
                    ts_all = PHONE_NUM[sms_phone_number] + t
                    oik_set_ts(ts_all, 1)
                    time.sleep(1)
                    str_2_log = f'{sms_phone_number};{PHONE_NUM[sms_phone_number]};{sms_time};{sms_text[0]} \n'#Генерируем строку для записи в файл лога
            elif len(ts_end) > 2:
                ts_all = PHONE_NUM[sms_phone_number] + '1'
                oik_set_ti(ts_all, ts_end)
                str_2_log = f'{sms_phone_number};{PHONE_NUM[sms_phone_number]};{sms_time};{sms_text[0]} \n'#Генерируем строку для записи в файл лога
            else:
                ts_all = PHONE_NUM[sms_phone_number] + ts_end
                oik_set_ts(ts_all, 1)    
                str_2_log = f'{sms_phone_number};{PHONE_NUM[sms_phone_number]};{sms_time};{sms_text[0]} \n'#Генерируем строку для записи в файл лога
                #elif ts_end == 'load':
                #    oik_set_ti(PHONE_NUM[sms_phone_number]+':1', ts_end[1])
            #else:                    
                
        else:
            print ('error')
            str_2_log = f'{sms_phone_number};{PHONE_NUM[sms_phone_number]};{sms_time};{sms_text[0]} \n'#Генерируем строку для записи в файл лога
    #Добавить условие наличия sms_phone_number в словаре PHONE_NUM

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

def linetroll_decode(ln_msg):
    ln_msg = ln_msg.split()
    print (ln_msg[0])
    if ln_msg[0] == '3':
        print ('Is Lintroll!') 
        if ln_msg[1] == '18':
            print ('Is alarm message')
            if ln_msg[2] == '0':
                print ('OK')
                return 'ok'
                
            elif ln_msg[2] == '1':
                print ('Неустойчивое повреждение')
                return '1'
            elif ln_msg[2] == '2':
                print ('Устойчивое повреждение')
                return '2'
            elif ln_msg[2] == '4':
                print ('Потеря напряжения в сети')
                return '3'
            elif ln_msg[2] == '6':
                print ('Устойчивое повреждение  + потеря напряжения в сети')
                return ['2','3']
            elif ln_msg[2] == '8':
                print ('Низкий заряд батареи')
                return '4'
            elif ln_msg[2] == '9':
                print ('Неустойчивое повреждение + Низкий заряд батареи')
                return ['1','4']
            elif ln_msg[2] == '10':
                print ('Устойчивое повреждение + Низкий заряд батареи')
                return ['2','4']
            elif ln_msg[2] == '12':
                print ('Потеря напряжения в сети + Низкий заряд батареи ')
                return ['3','4']
        elif ln_msg[1] == '3':
            print (f'Лайнтролл включен, уровень сети {ln_msg[2]}')
            return (ln_msg[2])
        #elif ln_msg[1] == '19':
    else:
        print ('Is not Linetroll!')    
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