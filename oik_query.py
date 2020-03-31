import hashlib
import time
import requests
import urllib
SERVER_ADRESS = 'http://localhost/?query='
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
oik_set_ts('1:1:5')