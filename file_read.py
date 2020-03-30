def load_settings():
    f = open('settings.ini', 'r')
    tp_numbers = f.readlines()

    #first = tp_numbers[0].split(';')
    f.close()
    for tp in tp_numbers:
        tp = tp.split(';')
        user_dict = {tp[0]:tp[1]}
    return user_dict.items()


print (load_settings())
