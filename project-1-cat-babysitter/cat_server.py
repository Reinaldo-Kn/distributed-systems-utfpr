import socket
import struct
import cat_db

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
endereco = ('127.0.0.1', 65535)

db = cat_db.BD()

sock.bind(endereco)
sock.listen()
print(f"Server started on {endereco[0]}:{endereco[1]}")
print("Waiting for client connection...")

dados, _ = sock.accept()

while True:
    opcode = dados.recv(1)
    if not opcode:
        break

    opcode = opcode.decode()
    match opcode:

        # CREATE
        case 'c':
            owner_len = int.from_bytes(dados.recv(1), 'big')
            owner = dados.recv(owner_len).decode()

            cat_len = int.from_bytes(dados.recv(1), 'big')
            cat = dados.recv(cat_len).decode()

            days = int.from_bytes(dados.recv(1), 'big')
            price = struct.unpack('>d', dados.recv(8))[0]

            city_len = int.from_bytes(dados.recv(1), 'big')
            city = dados.recv(city_len).decode()

            id = db.insert(owner, cat, days, price, city)
            if id is None:
                id = -1

            dados.send(id.to_bytes(2, 'big', signed=True))

        # READ
        case 'r':
            id = int.from_bytes(dados.recv(2), 'big')
            result = db.get(id)

            if result is None:
                dados.send((-1).to_bytes(2, 'big', signed=True))
                continue

            owner = result[1]
            cat = result[2]
            days = result[3]
            price = result[4]
            city = result[5]

            owner_b = owner.encode()
            cat_b = cat.encode()
            city_b = city.encode()

            msg = len(owner_b).to_bytes(1, 'big') + owner_b
            msg += len(cat_b).to_bytes(1, 'big') + cat_b
            msg += days.to_bytes(1, 'big')
            msg += struct.pack('>d', price)
            msg += len(city_b).to_bytes(1, 'big') + city_b

            dados.send(msg)

        # UPDATE
        case 'u':
            id = int.from_bytes(dados.recv(2), 'big')

            owner_len = int.from_bytes(dados.recv(1), 'big')
            owner = dados.recv(owner_len).decode()

            cat_len = int.from_bytes(dados.recv(1), 'big')
            cat = dados.recv(cat_len).decode()

            days = int.from_bytes(dados.recv(1), 'big')
            price = struct.unpack('>d', dados.recv(8))[0]

            city_len = int.from_bytes(dados.recv(1), 'big')
            city = dados.recv(city_len).decode()

            db.update(id, owner, cat, days, price, city)

            dados.send(b'\x01')

        # DELETE
        case 'd':
            id = int.from_bytes(dados.recv(2), 'big')

            db.delete(id)

            dados.send(b'\x01')

        # LIST
        case 'l':
            lista = db.list()

            # Just for debug process
            dados.send(len(lista).to_bytes(2, 'big'))

            for item in lista:
                owner_b = item[1].encode()
                cat_b = item[2].encode()
                city_b = item[5].encode()

                msg = item[0].to_bytes(2, 'big')
                msg += len(owner_b).to_bytes(1, 'big') + owner_b
                msg += len(cat_b).to_bytes(1, 'big') + cat_b
                msg += item[3].to_bytes(1, 'big')
                msg += struct.pack('>d', item[4])
                msg += len(city_b).to_bytes(1, 'big') + city_b

                dados.send(msg)