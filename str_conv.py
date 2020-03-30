str = ['AT+CMGR=1\r\r\n+CMGR: "REC UNREAD","+79090025706",,"20/03/30,13:01:55+16"\r\nLkkl\r\n \r\r\nOK\r\n']

str2 = str[0].split('"')

print (str2[3]) 


str4 = str