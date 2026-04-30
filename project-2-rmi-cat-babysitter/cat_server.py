from Pyro5.api import Daemon, expose, locate_ns

from booking import register_pyro_serializers
from cat_db import CatBookingCRUD


@expose
class CatBookingService:
    def __init__(self):
        self.db = CatBookingCRUD()

    def create_booking(self, booking):
        return self.db.create_booking(booking)

    def read_booking(self, booking_id):
        return self.db.read_booking(booking_id)

    def update_booking(self, booking_id, booking):
        return self.db.update_booking(booking_id, booking)

    def delete_booking(self, booking_id):
        return self.db.delete_booking(booking_id)

    def list_bookings(self):
        return self.db.list_bookings()


def main():
    register_pyro_serializers()
    service = CatBookingService()

    with Daemon(host="127.0.0.1") as daemon:
        uri = daemon.register(service)
        ns = locate_ns(host="127.0.0.1")
        ns.register("reinaldoKN", uri)
        print("Pyro5 server running")
        print(f"URI: {uri}")
        print("Registered in Name Server as: reinaldoKN")
        daemon.requestLoop()


if __name__ == "__main__":
    main()
