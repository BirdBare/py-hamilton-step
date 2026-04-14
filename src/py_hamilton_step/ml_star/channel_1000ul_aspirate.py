import dataclasses
import typing

from ..venus import VenusCommand, VenusResponse, VenusStepReturnBlockDataPackage


@dataclasses.dataclass(frozen=True)
class Channel1000ulAspirateResponse(VenusResponse):
    raw_channel_sequences_with_recovery_details: str
    channel_sequences_with_recovery_details: VenusStepReturnBlockDataPackage = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "channel_sequences_with_recovery_details",
            VenusStepReturnBlockDataPackage.parse_raw_step_return(self.raw_channel_sequences_with_recovery_details),
        )


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulAspirateChannelConfig:
    channel_number: typing.Literal[1, 2, 3, 4, 5, 6, 7, 8]
    sequence_labware: str
    sequence_position: str
    volume_ul: float
    aspirate_mode: typing.Literal["Aspiration", "Consecutive aspiration", "Aspirate all"] = "Aspiration"
    liquid_class: str
    capacitive_lld_sensitivity: typing.Literal[
        "Off",
        "Very high",
        "High",
        "Medium",
        "Low",
        "From labware definition",
    ] = "From labware definition"
    pressure_lld_sensitivity: typing.Literal[
        "Off",
        "Very high",
        "High",
        "Medium",
        "Low",
        "From labware definition",
    ] = "Off"
    fix_height_from_bottom_mm: float = 5
    touch_off: typing.Literal["Off", "On"] = "Off"
    submerge_depth_mm: float = 2
    max_height_difference_mm: float = 0
    retract_distance_for_transport_air_mm: float = 5
    aspiration_position_above_touch_mm: float = 0.5

    # Advanced
    liquid_following_during_aspirate_and_mix: typing.Literal["Off", "On"] = "On"

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

_aspiration_mode_setting_by_name = {
    "Aspiration": 0,
    "Consecutive aspiration": 1,
    "Aspirate all": 2,
}

_on_off_setting_by_name = {
    "Off": 0,
    "On": 1,
}


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulAspirateCommand(VenusCommand):
    channel_configs: tuple[Channel1000ulAspirateChannelConfig, ...]

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        channel_configs = sorted(self.channel_configs, key=lambda config: config.channel_number)

        args = command_dict["args"]

        # zip channel configs into associated lists
        args["channel_number"] = [config.channel_number for config in channel_configs]
        args["sequence_labware"] = [config.sequence_labware for config in channel_configs]
        args["sequence_position"] = [config.sequence_position for config in channel_configs]
        args["volume_ul"] = [config.volume_ul for config in channel_configs]
        args["aspirate_mode"] = [_aspiration_mode_setting_by_name[config.aspirate_mode] for config in channel_configs]
        args["liquid_class"] = [config.liquid_class for config in channel_configs]
        args["capacitive_lld_sensitivity"] = [
            _lld_sensitivity_setting_by_name[config.capacitive_lld_sensitivity] for config in channel_configs
        ]
        args["pressure_lld_sensitivity"] = [
            _lld_sensitivity_setting_by_name[config.pressure_lld_sensitivity] for config in channel_configs
        ]
        args["fix_height_from_bottom_mm"] = [config.fix_height_from_bottom_mm for config in channel_configs]
        args["touch_off"] = [_on_off_setting_by_name[config.touch_off] for config in channel_configs]
        args["submerge_depth_mm"] = [config.submerge_depth_mm for config in channel_configs]
        args["max_height_difference_mm"] = [config.max_height_difference_mm for config in channel_configs]
        args["retract_distance_for_transport_air_mm"] = [
            config.retract_distance_for_transport_air_mm for config in channel_configs
        ]
        args["aspiration_position_above_touch_mm"] = [
            config.aspiration_position_above_touch_mm for config in channel_configs
        ]
        args["liquid_following_during_aspirate_and_mix"] = [
            _on_off_setting_by_name[config.liquid_following_during_aspirate_and_mix] for config in channel_configs
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
    def parse_response(data: dict) -> Channel1000ulAspirateResponse:
        return Channel1000ulAspirateResponse(
            command_id=data["command_id"],
            raw_channel_sequences_with_recovery_details=data["raw_channel_sequences_with_recovery_details"],
        )
