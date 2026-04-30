from Pyro5.api import Proxy

from booking import Booking, register_pyro_serializers

MAX_BYTE_VALUE = 255
MAX_ID = 65535

CAT_ASCII = r"""
 /\_/\
( o.o )  What do you want to do?
 > ^ <
"""


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

    booking = Booking(
        id=None,
        owner_name=owner,
        cat_name=cat,
        days=days,
        price_per_day=price,
        city=city,
    )
    created = remote.create_booking(booking)
    print("Created ID:", created.id)


def read():
    id = input_int_range("ID", 0, MAX_ID)

    result = remote.read_booking(id)
    if result is None:
        print("Not found")
        return

    print("owner_name | cat_name | days | price_per_day | city")
    print(
        f"{result.owner_name} | {result.cat_name} | "
        f"{result.days} | {result.price_per_day:.2f} | {result.city}"
    )


def update():
    id = input_int_range("ID", 0, MAX_ID)
    owner = input_text_max_bytes("Owner", MAX_BYTE_VALUE)
    cat = input_text_max_bytes("Cat", MAX_BYTE_VALUE)
    days = input_int_range("Days", 0, MAX_BYTE_VALUE)
    price = input_float_min("Price", 0.0)
    city = input_text_max_bytes("City", MAX_BYTE_VALUE)

    booking = Booking(
        id=id,
        owner_name=owner,
        cat_name=cat,
        days=days,
        price_per_day=price,
        city=city,
    )
    ok = remote.update_booking(id, booking)
    print("Updated!" if ok else "Error")


def delete():
    id = input_int_range("ID", 0, MAX_ID)

    ok = remote.delete_booking(id)
    print("Deleted!" if ok else "Error")


def list_all():
    bookings = remote.list_bookings()
    count = len(bookings)

    if count == 0:
        print("No bookings found")
        return

    print("id | owner_name | cat_name | days | price_per_day | city")

    for item in bookings:
        print(
            f"{item.id} | {item.owner_name} | {item.cat_name} | "
            f"{item.days} | {item.price_per_day:.2f} | {item.city}"
        )

print("Welcome to the Cat Babysitter Service!")
print(CAT_ASCII)

register_pyro_serializers()
remote = Proxy("PYRONAME:reinaldoKN@127.0.0.1")

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
    except (OSError, RuntimeError) as error:
        print(f"Connection/protocol error: {error}")
        break
