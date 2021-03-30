#!/usr/bin/env python3
import socket
import time
import sys
from product import Product
import pickle 
import argparse

'''
Socket programming demo

laddr       local address
raddr       remote address

pickie      to serialize  and deserialize objects
serialize   python object to byte stream
deserialize byte stream to python object 

'''
def hosts_info():
    print('Host name: {}'.format(socket.gethostname()))
    print('Host by name 1: {}'.format(socket.gethostbyname('localhost')))
    print('Host by name 2: {}'.format(socket.gethostbyname(socket.gethostname())))
    print('Host by addr 1: {}'.format(socket.gethostbyaddr('127.0.0.1')))
    print('Host by addr 2: {}'.format(socket.gethostbyaddr('127.0.1.1')))
    print('Host by name 3: {}'.format(socket.gethostbyname('')))


def start_server():

    print('*** Creating server ***')

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP SOCKET
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((socket.gethostname(), 4571))
        # set timeout 10 sec to wait connection
        s.settimeout(10)
        try:

            # maximum number of queued connections (5)
            s.listen(5)

            print('*** Server is up. Listening for connections***')
            client, address = s.accept()
            print(f'*** Connection to {address} established ***')
            print(f'*** Client object {client} ***')

            msg = client.recv(1024)
            obj_type = msg.decode('utf-8')

            if obj_type == 'bytes':
                client.send(bytes('Hello! Alex ', 'utf-8'))

            if obj_type == 'dict':
                python_dic = {'a': 1, 'b': 2}
                pickled_dic = pickle.dumps(python_dic)
                print(f'*** Seialized dictionary type:  {type(pickled_dic)} ***')
                client.send(pickled_dic)

            if obj_type == 'class':
                custom_object =Product('P024', 'Torch', 14)
                pickled_object = pickle.dumps(custom_object)
                print(f'*** Seialized object type:  {type(pickled_object)} ***')
                client.send(pickled_object)

            if obj_type == 'text':
                custom_file = open('server_files/sample_100k.txt', 'rb' )
                custom_data = custom_file.read(40960)
                while (custom_data):
                    client.send(custom_data)
                    custom_data = custom_file.read(40960)
                print('Custom file sent successfully')   

        except socket.timeout as e: 
            print(f'Exception appeared: {e}')
            print(f'Closing the connection')
            pass 

# s.close()

def simple_client():
    print('*** Creating client ***')

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP SOCKET 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((socket.gethostname(), 4571))
        msg = 'bytes'
        s.sendall(msg.encode())
        time.sleep(1)
        msg = s.recv(1024)
        print('*** Message from server: {}'.format(msg.decode('utf-8')))


def receive_dictionary_object():
    print('*** Creating client ***')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((socket.gethostname(), 4571))
        msg = 'dict'
        s.sendall(msg.encode())
        time.sleep(1)
        while True:
            msg = s.recv(2048)
            if not msg:
                print('*** No messages from server')
                break

            print('\n*** Type of received message : {}'.format(type(msg)))
            print('***  Received data : {}'.format(msg))
            unplickled = pickle.loads(msg)

            print(f'\n*** Deseialized type:  {type(unplickled)} ***')
            print(f'*** Deseialized data:  {unplickled} ***')


def receive_class_object():
    print('*** Creating client ***')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((socket.gethostname(), 4571))
        msg = 'class'
        s.sendall(msg.encode())
        time.sleep(1)

        while True:
            msg = s.recv(1024)
            if not msg:
                print('*** No messages from server')
                break

            print('\n*** Type of received message : {}'.format(type(msg)))
            print('***  Received data : {}'.format(msg))
            unplickled = pickle.loads(msg)
            print(f'\n*** Deseialized type:  {type(unplickled)} ***')
            print(f'*** Deseialized data:  {unplickled} ***')
            print(f'Product ID    : {unplickled.pid}')
            print(f'Product Name  : {unplickled.pname}')
            print(f'Product Price : {unplickled.pprice}')


def receive_text_file():
    print('*** Creating client ***')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((socket.gethostname(), 4571))
        msg = 'text'
        s.sendall(msg.encode())
        time.sleep(1)

        custom_file = open('client_files/received_file.txt', 'wb')
        while True:
            data = s.recv(40960)
            if not data:
                print('*** No messages from server')
                break

            custom_file.write(data)
            print('Batch of data written to file...')
        
        custom_file.close()



def parse_arguments():
    parser = argparse.ArgumentParser(
                      description='Socket programming demo ',
                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-s', '--server', action='store_true', required=False,
                        help='Simple server  demo')

    parser.add_argument('-c', '--client', action='store_true', required=False,
                        help='Client requests and receives byte stream')

    parser.add_argument('-d', '--dic', action='store_true', required=False,
                        help='Client requests and receives dictionary instance')

    parser.add_argument('-p', '--product', action='store_true', required=False,
                            help='Client requests and receives class "Product" instance')

    parser.add_argument('-l', '--hosts', action='store_true', required=False,
                        help='Print hosts info')

    parser.add_argument('-t', '--text', action='store_true', required=False,
                        help='Client requests and receives large text file')


    args = parser.parse_args()
    return parser, args


def main():
    parser,args = parse_arguments()
    # print (args)
    # print (args._get_kwargs())

    for arg in args._get_kwargs():
        if True in arg:
            break
    else:
        parser.print_help()

    if args.hosts:      hosts_info()
    if args.server:     start_server()
    if args.client:     simple_client()
    if args.dic:        receive_dictionary_object()
    if args.product:    receive_class_object()
    if args.text:       receive_text_file()

# Note: transfer of images is same. In addition, PIL library cna be used

if __name__ == "__main__":
    main()
