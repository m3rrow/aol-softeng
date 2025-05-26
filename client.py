import qrcode, requests, json
from time import sleep
from os import system

uuid = input('uuid> ')
username = input('username> ')
data = {
    'uuid': uuid,
    'username': username,
    'privilege': 'pembeli',
}

resp = requests.post('http://127.0.0.1:8080/create_room', json=data)
print(resp.text)

def print_message(data):
    for msg in data:
        print(msg)

while True:
    system("cls")
    resp = requests.post('http://127.0.0.1:8080/get_message', json=data)
    msg_text = json.loads(resp.text)['message']
    print_message(msg_text)
    inp = input('[ADMIN SYSTEM] Konfirmasi Oleh Pembeli (Y/N) : ')
    if inp in ['Y', 'y']:
        msg = '[Y][ADMIN SYSTEM] PEMBAYARAN TELAH DILAKUKAN OLEH PEMBELI'
        data = {
            'uuid': uuid,
            'msg': msg
        }
        requests.post('http://127.0.0.1:8080/send_message', json=data)
        print(msg)
        break
    elif inp in ['N', 'n']:
        msg = '[N][ADMIN SYSTEM] CHATROOM DITUTUP PAKSA OLEH PEMBELI'
        data = {
            'uuid': uuid,
            'msg': msg
        }
        requests.post('http://127.0.0.1:8080/send_message', json=data)
        print(msg)
        exit(1)
    else:
        print('[ERR SYSTEM] KONFIRMASI KEMBALI!')