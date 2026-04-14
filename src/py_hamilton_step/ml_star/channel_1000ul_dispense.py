import dataclasses
import typing

from ..venus import VenusCommand, VenusResponse, VenusStepReturnBlockDataPackage


@dataclasses.dataclass(frozen=True)
class Channel1000ulDispenseResponse(VenusResponse):
    raw_channel_sequences_with_recovery_details: str
    channel_sequences_with_recovery_details: VenusStepReturnBlockDataPackage = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "channel_sequences_with_recovery_details",
            VenusStepReturnBlockDataPackage.parse_raw_step_return(self.raw_channel_sequences_with_recovery_details),
        )


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulDispenseChannelConfig:
    channel_number: typing.Literal[1, 2, 3, 4, 5, 6, 7, 8]
    sequence_labware: str
    sequence_position: str
    volume_ul: float
    dispense_mode: typing.Literal[
        "Jet part volume",
        "Jet empty tip",
        "Surface part volume",
        "Surface empty tip",
        "Drain tip in jet mode",
        "From liquid class definition",
        "Blowout tip",
    ] = "From liquid class definition"
    fix_height_from_bottom_mm: float = 5
    capacitive_lld_sensitivity: typing.Literal[
        "Off",
        "Very high",
        "High",
        "Medium",
        "Low",
        "From labware definition",
    ] = "From labware definition"
    touch_off: typing.Literal["Off", "On"] = "Off"
    retract_distance_for_transport_air_mm: float = 5
    submerge_depth_mm: float = 2
    dispense_position_above_touch_mm: float = 0.5

    # Advanced
    liquid_class: str
    liquid_following_during_dispense_and_mix: typing.Literal["Off", "On"] = "On"

    # Mix settings
    cycles: int = 0
    mix_position_mm: float = 2
    mix_volume_ul: float = 0


_lld_sensitivity_setting_by_name = {
    "Off": 0,
    "Very high": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
    "From labware definition": 5,
}

_dispense_mode_setting_by_name = {
    "Jet part volume": 0,
    "Jet empty tip": 1,
    "Surface part volume": 2,
    "Surface empty tip": 3,
    "Drain tip in jet mode": 4,
    "From liquid class definition": 8,
    "Blowout tip": 9,
}

_on_off_setting_by_name = {
    "Off": 0,
    "On": 1,
}

_z_move_setting_by_name = {
    "normal": 0,
    "minimized": 1,
}


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulDispenseCommand(VenusCommand):
    side_touch: typing.Literal["Off", "On"] = "Off"
    z_move_after_step: typing.Literal["normal", "minimized"] = "normal"
    channel_configs: tuple[Channel1000ulDispenseChannelConfig, ...]

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        channel_configs = sorted(self.channel_configs, key=lambda config: config.channel_number)

        args = command_dict["args"]

        args["side_touch"] = _on_off_setting_by_name[self.side_touch]
        args["z_move_after_step"] = _z_move_setting_by_name[self.z_move_after_step]

        # zip channel configs into associated lists
        args["channel_number"] = [config.channel_number for config in channel_configs]
        args["sequence_labware"] = [config.sequence_labware for config in channel_configs]
        args["sequence_position"] = [config.sequence_position for config in channel_configs]
        args["volume_ul"] = [config.volume_ul for config in channel_configs]
        args["dispense_mode"] = [_dispense_mode_setting_by_name[config.dispense_mode] for config in channel_configs]
        args["fix_height_from_bottom_mm"] = [config.fix_height_from_bottom_mm for config in channel_configs]
        args["capacitive_lld_sensitivity"] = [
            _lld_sensitivity_setting_by_name[config.capacitive_lld_sensitivity] for config in channel_configs
        ]
        args["touch_off"] = [_on_off_setting_by_name[config.touch_off] for config in channel_configs]

        args["retract_distance_for_transport_air_mm"] = [
            config.retract_distance_for_transport_air_mm for config in channel_configs
        ]
        args["submerge_depth_mm"] = [config.submerge_depth_mm for config in channel_configs]
        args["dispense_position_above_touch_mm"] = [
            config.dispense_position_above_touch_mm for config in channel_configs
        ]
        args["liquid_class"] = [config.liquid_class for config in channel_configs]
        args["liquid_following_during_dispense_and_mix"] = [
            _on_off_setting_by_name[config.liquid_following_during_dispense_and_mix] for config in channel_configs
        ]

        args["cycles"] = [config.cycles for config in channel_configs]
        args["mix_position_mm"] = [config.mix_position_mm for config in channel_configs]
        args["mix_volume_ul"] = [config.mix_volume_ul for config in channel_configs]

        # create a channel_variable from channel_number
        args["channel_variable"] = "".join(
            ["1" if i + 1 in args["channel_number"] else "0" for i in range(16)],
        )

        return command_dict

    @staticmethod
    def parse_response(data: dict) -> Channel1000ulDispenseResponse:
        return Channel1000ulDispenseResponse(
            command_id=data["command_id"],
            raw_channel_sequences_with_recovery_details=data["raw_channel_sequences_with_recovery_details"],
        )
