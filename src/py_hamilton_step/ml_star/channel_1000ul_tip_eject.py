import dataclasses
import typing

from ..venus import VenusCommand, VenusResponse, VenusStepReturnBlockDataPackage


@dataclasses.dataclass(frozen=True)
class Channel1000ulTipEjectResponse(VenusResponse):
    raw_channel_sequences_with_recovery_details: str
    channel_sequences_with_recovery_details: VenusStepReturnBlockDataPackage = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "channel_sequences_with_recovery_details",
            VenusStepReturnBlockDataPackage.parse_raw_step_return(self.raw_channel_sequences_with_recovery_details),
        )


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulTipEjectChannelConfig:
    channel_number: typing.Literal[1, 2, 3, 4, 5, 6, 7, 8]
    sequence_labware: str
    sequence_position: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulTipEjectCommand(VenusCommand):
    channel_configs: tuple[Channel1000ulTipEjectChannelConfig, ...]

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        channel_configs = sorted(self.channel_configs, key=lambda config: config.channel_number)

        args = command_dict["args"]

        # zip channel configs into associated lists
        args["channel_number"] = [config.channel_number for config in channel_configs]
        args["sequence_labware"] = [config.sequence_labware for config in channel_configs]
        args["sequence_position"] = [config.sequence_position for config in channel_configs]

        # create a channel_variable from channel_number
        args["channel_variable"] = "".join(
            ["1" if i + 1 in args["channel_number"] else "0" for i in range(16)],
        )

        return command_dict

    @staticmethod
    def parse_response(data: dict) -> Channel1000ulTipEjectResponse:
        return Channel1000ulTipEjectResponse(
            command_id=data["command_id"],
            raw_channel_sequences_with_recovery_details=data["raw_channel_sequences_with_recovery_details"],
        )
