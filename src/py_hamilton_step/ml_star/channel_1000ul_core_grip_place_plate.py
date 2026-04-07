import dataclasses
import typing

from ..hamilton import HamiltonCommand, HamiltonResponse


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulCoreGripPlacePlate(HamiltonCommand):
    transport_mode: typing.Literal["Plate only", "Lid only", "Plate with lid"] = "Plate only"
    plate_sequence_labware: str | None = None
    lid_sequence_labware: str | None = None
    eject_tool_when_finish: typing.Literal["No", "Yes"] = "No"

    # Advanced
    x_acceleration_level: typing.Literal[
        "X acceleration level 1",
        "X acceleration level 2",
        "X acceleration level 3",
        "X acceleration level 4",
        "X acceleration level 5",
    ] = "X acceleration level 4"
    z_speed_mm_per_s: float = 128.7
    plate_press_on_distance_mm: float = 1
    check_if_plate_exists: typing.Literal["Off", "On"] = "Off"

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        command_dict["transport_mode"] = self.transport_mode
        command_dict["plate_sequence_labware"] = self.plate_sequence_labware
        command_dict["lid_sequence_labware"] = self.lid_sequence_labware
        command_dict["eject_tool_when_finish"] = self.eject_tool_when_finish
        command_dict["x_acceleration_level"] = self.x_acceleration_level
        command_dict["z_speed_mm_per_s"] = self.z_speed_mm_per_s
        command_dict["plate_press_on_distance_mm"] = self.plate_press_on_distance_mm
        command_dict["check_if_plate_exists"] = self.check_if_plate_exists

        return command_dict

    def parse_response(self, data: dict) -> HamiltonResponse: ...
