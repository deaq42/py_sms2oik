str1 = ''

str2 = str1.encode()
str3 = str2.decode('utf8')

print (f'{str2}') 
print (chr(int(str3)))