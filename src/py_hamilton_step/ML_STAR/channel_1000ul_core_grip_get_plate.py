import dataclasses
import typing

from ..hamilton import HamiltonCommand, HamiltonResponse


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulCoreGripGetPlate(HamiltonCommand):
    transport_mode: typing.Literal["Plate only", "Lid only", "Plate with lid"] = "Plate only"
    plate_sequence_labware: str | None = None
    lid_sequence_labware: str | None = None

    # Gripper tool parameters
    gripper_tool_sequence_labware: str
    used_front_channel: typing.Literal[
        "Channel 2",
        "Channel 3",
        "Channel 4",
        "Channel 5",
        "Channel 6",
        "Channel 7",
        "Channel 8",
    ] = "Channel 8"

    # Grip parameters
    grip_height_mm: float = 3
    grip_width_mm: float
    opening_width_before_access: float

    # Advanced
    # grip_force: typing.Literal[
    #    "Grip Force 1",
    #    "Grip Force 2",
    #    "Grip Force 3",
    #    "Grip Force 4",
    #    "Grip Force 5",
    #    "Grip Force 6",
    #    "Grip Force 7",
    #    "Grip Force 8",
    #    "Grip Force 9",
    # ] = "Grip Force 5"
    # Most likely does not apply if we overwrite the grip width...

    grip_speed_mm_per_s: float = 277.8
    z_speed_mm_per_s: float = 128.7
    check_if_plate_exists: typing.Literal["Off", "On"] = "Off"

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        command_dict["transport_mode"] = self.transport_mode
        command_dict["plate_sequence_labware"] = self.plate_sequence_labware
        command_dict["lid_sequence_labware"] = self.lid_sequence_labware
        command_dict["gripper_tool_sequence_labware"] = self.gripper_tool_sequence_labware
        command_dict["used_front_channel"] = self.used_front_channel
        command_dict["grip_height_mm"] = self.grip_height_mm
        command_dict["grip_width_mm"] = self.grip_width_mm
        command_dict["opening_width_before_access"] = self.opening_width_before_access
        command_dict["grip_speed_mm_per_s"] = self.grip_speed_mm_per_s
        command_dict["z_speed_mm_per_s"] = self.z_speed_mm_per_s
        command_dict["check_if_plate_exists"] = self.check_if_plate_exists

        return command_dict

    def parse_response(self, data: dict) -> HamiltonResponse: ...
