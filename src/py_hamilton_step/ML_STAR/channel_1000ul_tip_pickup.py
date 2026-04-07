import dataclasses
import typing

from ..hamilton import HamiltonCommand, HamiltonResponse


@dataclasses.dataclass(kw_only=True, frozen=True)
class ChannelConfig:
    channel_number: typing.Literal[1, 2, 3, 4, 5, 6, 7, 8]
    sequence_labware: str
    sequence_position: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulTipPickup(HamiltonCommand):
    channel_configs: tuple[ChannelConfig, ...]

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        # zip channel configs into associated lists
        command_dict["channel_number"] = [config.channel_number for config in self.channel_configs]
        command_dict["sequence_labware"] = [config.sequence_labware for config in self.channel_configs]
        command_dict["sequence_position"] = [config.sequence_position for config in self.channel_configs]

        return command_dict

    def parse_response(self, data: dict) -> HamiltonResponse: ...
