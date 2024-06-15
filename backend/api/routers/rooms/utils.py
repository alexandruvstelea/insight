from ...database.models.room import Room
from .schemas import RoomOut, RoomOutMinimal


def room_to_out(room: Room) -> RoomOut:
    from ..buildings.utils import building_to_minimal

    return RoomOut(
        id=room.id,
        name=room.name,
        building_id=room.building_id,
        building=building_to_minimal(room.building),
    )


def room_to_minimal(room: Room) -> RoomOutMinimal:
    return RoomOutMinimal(id=room.id, name=room.name, building_id=room.building_id)
