import hashlib
import time
commandkey='1234'
timestamp = str(time.time())
timestamp.split('.')
timestamp = timestamp[1] + '000'
str = f'!IP-gate@{commandkey}@{timestamp}!'
sha_str = hashlib.sha256(str.encode())
print (sha_str.hexdigest())
print (timestamp)

query = {   "query": "set-ts",  
            "ts": "0:10:100",  
            "value": 1,  
            "hash": "d6f66188167a7b97939400817bea6dad8e45c26893ae16d564bc329c7bd32582",  
            "timestamp": 1360918299956 } 
