import sys
import argparse

 
def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-s', '--server', default='127.0.0.1')
    parser.add_argument('-p', '--port', default = 'none')
    parser.add_argument('-cc', '--comandkey', default = 'none') 
    return parser
parser = createParser()
namespace = parser.parse_args(sys.argv[1:])
    # print (namespace)
if namespace.port == 'none':
    print ('Не задан ком порт')
    raise SystemExit
print ("Адрес сервера {}!".format (namespace.server) )
print ("КОМ ПОРТ {}!".format (namespace.port) )

