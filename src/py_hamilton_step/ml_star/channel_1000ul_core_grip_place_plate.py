import dataclasses
import typing

from ..hamilton import HamiltonCommand, HamiltonResponse, HamiltonStepReturnBlockDataPackage


@dataclasses.dataclass(frozen=True)
class Channel1000ulCoreGripPlacePlateResponse(HamiltonResponse):
    raw_place_plate_data_with_recovery_details: str
    place_plate_data_with_recovery_details: HamiltonStepReturnBlockDataPackage = dataclasses.field(init=False)
    raw_channel_sequences_with_recovery_details: str
    channel_sequences_with_recovery_details: HamiltonStepReturnBlockDataPackage | None = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "place_plate_data_with_recovery_details",
            HamiltonStepReturnBlockDataPackage.parse_raw_step_return(self.raw_place_plate_data_with_recovery_details),
        )
        if self.raw_channel_sequences_with_recovery_details == "":
            object.__setattr__(self, "channel_sequences_with_recovery_details", None)
        else:
            object.__setattr__(
                self,
                "channel_sequences_with_recovery_details",
                HamiltonStepReturnBlockDataPackage.parse_raw_step_return(
                    self.raw_channel_sequences_with_recovery_details,
                ),
            )


_transport_mode_setting_by_name = {
    "Plate only": 0,
    "Lid only": 1,
    "Plate with lid": 2,
}

_x_acceleration_level_setting_by_name = {
    "X acceleration level 1": 0,
    "X acceleration level 2": 1,
    "X acceleration level 3": 2,
    "X acceleration level 4": 3,
    "X acceleration level 5": 4,
}

_on_off_setting_by_name = {
    "Off": 0,
    "On": 1,
}

_yes_no_setting_by_name = {
    "No": 0,
    "Yes": 1,
}


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulCoreGripPlacePlateCommand(HamiltonCommand):
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

        args = command_dict["args"]

        args["transport_mode"] = _transport_mode_setting_by_name[self.transport_mode]
        args["plate_sequence_labware"] = str(self.plate_sequence_labware)
        args["lid_sequence_labware"] = str(self.lid_sequence_labware)
        args["eject_tool_when_finish"] = _yes_no_setting_by_name[self.eject_tool_when_finish]
        args["x_acceleration_level"] = _x_acceleration_level_setting_by_name[self.x_acceleration_level]
        args["z_speed_mm_per_s"] = self.z_speed_mm_per_s
        args["plate_press_on_distance_mm"] = self.plate_press_on_distance_mm
        args["check_if_plate_exists"] = _on_off_setting_by_name[self.check_if_plate_exists]

        return command_dict

    @staticmethod
    def parse_response(data: dict) -> Channel1000ulCoreGripPlacePlateResponse:
        return Channel1000ulCoreGripPlacePlateResponse(
            command_id=data["command_id"],
            raw_place_plate_data_with_recovery_details=data["raw_place_plate_data_with_recovery_details"],
            raw_channel_sequences_with_recovery_details=data["raw_channel_sequences_with_recovery_details"],
        )
