PHONE_NUM = {}
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
