import qrcode, uuid, requests, json
from time import sleep
from os import system

uuid = str(uuid.uuid4())
print(f"Generated UID: {uuid}")
username = input('username> ')
data = {
    'uuid': uuid,
    'username': username,
    'privilege': 'penjual',
    'partner': 'none',
    # 'amount': 500_000# set amount with real money
    'amount': int(input('total transaksi> '))
}

resp = requests.post('http://127.0.0.1:8080/create_room', json=data)
print(resp.text)

def print_message(data):
    for msg in data:
        print(msg[0])

# konfirmasi buyer masuk ke chatroom
while True:
    system("cls")
    resp = requests.post('http://127.0.0.1:8080/get_message', json=data)
    msg_text = json.loads(resp.text)['message']
    confirmation_msg = msg_text[-1][-1][:3]
    print_message(msg_text)
    if confirmation_msg in ['[Y]', '[N]']:
        if confirmation_msg == '[Y]':
            break
        else:
            exit(1)
    sleep(5)

# konfirmasi pembayaran
while True:
    system("cls")
    resp = requests.post('http://127.0.0.1:8080/get_message', json=data)
    msg_text = json.loads(resp.text)['message']
    print_message(msg_text)
    inp = input('[ADMIN SYSTEM] Konfirmasi (Y/N) : ')
    if inp in ['Y', 'y']:
        msg = '[Y][ADMIN SYSTEM] PEMBAYARAN DIKONFIRMASI OLEH PENJUAL'
        data = {
            'uuid': uuid,
            'msg': msg
        }
        requests.post('http://127.0.0.1:8080/send_message', json=data)
        print(msg)
        break
    elif inp in ['N', 'n']:
        msg = '[N][ADMIN SYSTEM] CHATROOM DITUTUP PAKSA OLEH PENJUAL'
        data = {
            'uuid': uuid,
            'msg': msg
        }
        requests.post('http://127.0.0.1:8080/send_message', json=data)
        print(msg)
        exit(1)
    else:
        print('[ERR SYSTEM] KONFIRMASI KEMBALI!')