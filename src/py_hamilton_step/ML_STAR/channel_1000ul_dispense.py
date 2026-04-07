import dataclasses
import typing

from ..hamilton import HamiltonCommand, HamiltonResponse


@dataclasses.dataclass(kw_only=True, frozen=True)
class ChannelConfig:
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
    side_touch: typing.Literal["Off", "On"] = "Off"
    retract_distance_for_transport_air_mm: float = 5
    submerge_depth_mm: float = 2
    dispense_position_above_touch_mm: float = 0.5

    # Advanced
    liquid_class: str
    liquid_following_during_aspirate_and_mix: typing.Literal["Off", "On"] = "On"
    z_move_after_step: typing.Literal["normal", "minimized"] = "normal"

    # Mix settings
    cycles: int = 0
    mix_position_mm: float = 2
    mix_volume_ul: float = 0


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulDispense(HamiltonCommand):
    channel_configs: tuple[ChannelConfig, ...]

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        # zip channel configs into associated lists
        command_dict["channel_number"] = [config.channel_number for config in self.channel_configs]
        command_dict["sequence_labware"] = [config.sequence_labware for config in self.channel_configs]
        command_dict["sequence_position"] = [config.sequence_position for config in self.channel_configs]
        command_dict["volume_ul"] = [config.volume_ul for config in self.channel_configs]
        command_dict["dispense_mode"] = [config.dispense_mode for config in self.channel_configs]
        command_dict["fix_height_from_bottom_mm"] = [
            config.fix_height_from_bottom_mm for config in self.channel_configs
        ]
        command_dict["capacitive_lld_sensitivity"] = [
            config.capacitive_lld_sensitivity for config in self.channel_configs
        ]
        command_dict["touch_off"] = [config.touch_off for config in self.channel_configs]
        command_dict["side_touch"] = [config.side_touch for config in self.channel_configs]
        command_dict["retract_distance_for_transport_air_mm"] = [
            config.retract_distance_for_transport_air_mm for config in self.channel_configs
        ]
        command_dict["submerge_depth_mm"] = [config.submerge_depth_mm for config in self.channel_configs]
        command_dict["dispense_position_above_touch_mm"] = [
            config.dispense_position_above_touch_mm for config in self.channel_configs
        ]
        command_dict["liquid_class"] = [config.liquid_class for config in self.channel_configs]
        command_dict["liquid_following_during_aspirate_and_mix"] = [
            config.liquid_following_during_aspirate_and_mix for config in self.channel_configs
        ]
        command_dict["z_move_after_step"] = [config.z_move_after_step for config in self.channel_configs]
        command_dict["cycles"] = [config.cycles for config in self.channel_configs]
        command_dict["mix_position_mm"] = [config.mix_position_mm for config in self.channel_configs]
        command_dict["mix_volume_ul"] = [config.mix_volume_ul for config in self.channel_configs]

        return command_dict

    def parse_response(self, data: dict) -> HamiltonResponse: ...
