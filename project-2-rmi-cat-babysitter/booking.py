from dataclasses import dataclass


@dataclass
class Booking:
    id: int | None
    owner_name: str
    cat_name: str
    days: int
    price_per_day: float
    city: str


def booking_to_dict(obj: Booking) -> dict:
    return {
        "__class__": "Booking",
        "id": obj.id,
        "owner_name": obj.owner_name,
        "cat_name": obj.cat_name,
        "days": obj.days,
        "price_per_day": obj.price_per_day,
        "city": obj.city,
    }


def booking_from_dict(class_name: str, data: dict):
    if class_name == "Booking":
        return Booking(
            id=data.get("id"),
            owner_name=data["owner_name"],
            cat_name=data["cat_name"],
            days=data["days"],
            price_per_day=data["price_per_day"],
            city=data["city"],
        )
    return data


def register_pyro_serializers():
    from Pyro5.api import register_class_to_dict, register_dict_to_class

    register_class_to_dict(Booking, booking_to_dict)
    register_dict_to_class("Booking", booking_from_dict)

