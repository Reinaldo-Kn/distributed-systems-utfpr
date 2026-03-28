import socket
import struct

HOST = '127.0.0.1'
PORT = 65535
MAX_BYTE_VALUE = 255
MAX_ID = 65535

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

CAT_ASCII = r"""
 /\_/\
( o.o )  What do you want to do?
 > ^ <
"""


def recv_exact(size):
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Connection closed while receiving data")
        data += chunk
    return data


def input_int_range(label, min_value, max_value):
    while True:
        raw = input(f"{label}: ")
        try:
            value = int(raw)
        except ValueError:
            print(f"Invalid {label.lower()}. Enter an integer.")
            continue

        if value < min_value or value > max_value:
            print(f"{label} must be between {min_value} and {max_value}.")
            continue

        return value


def input_float_min(label, min_value):
    while True:
        raw = input(f"{label}: ")
        try:
            value = float(raw)
        except ValueError:
            print(f"Invalid {label.lower()}. Enter a number.")
            continue

        if value < min_value:
            print(f"{label} must be >= {min_value}.")
            continue

        return value


def input_text_max_bytes(label, max_bytes):
    while True:
        value = input(f"{label}: ")
        value_b = value.encode()

        if len(value_b) > max_bytes:
            print(f"{label} is too long. Maximum is {max_bytes} bytes.")
            continue

        return value


def create():
    owner = input_text_max_bytes("Owner", MAX_BYTE_VALUE)
    cat = input_text_max_bytes("Cat", MAX_BYTE_VALUE)
    days = input_int_range("Days", 0, MAX_BYTE_VALUE)
    price = input_float_min("Price", 0.0)
    city = input_text_max_bytes("City", MAX_BYTE_VALUE)

    msg = b'c'

    owner_b = owner.encode()
    cat_b = cat.encode()
    city_b = city.encode()

    msg += len(owner_b).to_bytes(1, 'big') + owner_b
    msg += len(cat_b).to_bytes(1, 'big') + cat_b
    msg += days.to_bytes(1, 'big')
    msg += struct.pack('>d', price)
    msg += len(city_b).to_bytes(1, 'big') + city_b

    sock.send(msg)

    id = int.from_bytes(recv_exact(2), 'big', signed=True)
    print("Created ID:", id)


def read():
    id = input_int_range("ID", 0, MAX_ID)

    msg = b'r' + id.to_bytes(2, 'big')
    sock.send(msg)

    data = sock.recv(1024)

    if len(data) == 2 and int.from_bytes(data, 'big', signed=True) == -1:
        print("Not found")
        return

    idx = 0

    owner_len = data[idx]
    idx += 1
    owner = data[idx:idx+owner_len].decode()
    idx += owner_len

    cat_len = data[idx]
    idx += 1
    cat = data[idx:idx+cat_len].decode()
    idx += cat_len

    days = data[idx]
    idx += 1

    price = struct.unpack('>d', data[idx:idx+8])[0]
    idx += 8

    city_len = data[idx]
    idx += 1
    city = data[idx:idx+city_len].decode()

    print("owner_name | cat_name | days | price_per_day | city")
    print(f"{owner} | {cat} | {days} | {price:.2f} | {city}")


def update():
    id = input_int_range("ID", 0, MAX_ID)
    owner = input_text_max_bytes("Owner", MAX_BYTE_VALUE)
    cat = input_text_max_bytes("Cat", MAX_BYTE_VALUE)
    days = input_int_range("Days", 0, MAX_BYTE_VALUE)
    price = input_float_min("Price", 0.0)
    city = input_text_max_bytes("City", MAX_BYTE_VALUE)

    msg = b'u' + id.to_bytes(2, 'big')

    owner_b = owner.encode()
    cat_b = cat.encode()
    city_b = city.encode()

    msg += len(owner_b).to_bytes(1, 'big') + owner_b
    msg += len(cat_b).to_bytes(1, 'big') + cat_b
    msg += days.to_bytes(1, 'big')
    msg += struct.pack('>d', price)
    msg += len(city_b).to_bytes(1, 'big') + city_b

    sock.send(msg)

    resp = recv_exact(1)
    print("Updated!" if resp == b'\x01' else "Error")


def delete():
    id = input_int_range("ID", 0, MAX_ID)

    msg = b'd' + id.to_bytes(2, 'big')
    sock.send(msg)

    resp = recv_exact(1)
    print("Deleted!" if resp == b'\x01' else "Error")


def list_all():
    sock.send(b'l')

    count = int.from_bytes(recv_exact(2), 'big')

    if count == 0:
        print("No bookings found")
        return

    print("id | owner_name | cat_name | days | price_per_day | city")

    for _ in range(count):
        id = int.from_bytes(recv_exact(2), 'big')

        owner_len = recv_exact(1)[0]
        owner = recv_exact(owner_len).decode()

        cat_len = recv_exact(1)[0]
        cat = recv_exact(cat_len).decode()

        days = recv_exact(1)[0]

        price = struct.unpack('>d', recv_exact(8))[0]

        city_len = recv_exact(1)[0]
        city = recv_exact(city_len).decode()

        print(f"{id} | {owner} | {cat} | {days} | {price:.2f} | {city}")


print("Welcome to the Cat Babysitter Service!")
print(CAT_ASCII)

while True:
    try:
        op = input("c=create, r=read, u=update, d=delete, l=list, q=quit: ").strip().lower()

        if op == 'c':
            create()
        elif op == 'r':
            read()
        elif op == 'u':
            update()
        elif op == 'd':
            delete()
        elif op == 'l':
            list_all()
        elif op == 'q':
            break
        else:
            print("Invalid option. Use: c, r, u, d, l, q.")
    except (ConnectionError, OSError, struct.error) as error:
        print(f"Connection/protocol error: {error}")
        break