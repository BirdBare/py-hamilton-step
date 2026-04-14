import dataclasses
import typing

from ..venus import (
    VenusCommand,
    VenusResponse,
    VenusStepReturnBlockDataPackage,
)


@dataclasses.dataclass(frozen=True)
class LockUnlockFrontCoverResponse(VenusResponse):
    raw_cover_lock_status_as_block_data: str
    cover_lock_status_as_block_data: VenusStepReturnBlockDataPackage = dataclasses.field(init=False)

    raw_cover_lock_status_flag: int
    cover_lock_status_flag: str = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "cover_lock_status_as_block_data",
            VenusStepReturnBlockDataPackage.parse_raw_step_return(self.raw_cover_lock_status_as_block_data),
        )

        object.__setattr__(
            self,
            "cover_lock_status_flag",
            "unlocked" if self.raw_cover_lock_status_flag == 0 else "locked",
        )


_front_setting_by_name = {
    "unlocked": 0,
    "locked": 1,
}


@dataclasses.dataclass(kw_only=True, frozen=True)
class LockUnlockFrontCoverCommand(VenusCommand):
    front: typing.Literal["unlocked", "locked"] = "locked"

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        args = command_dict["args"]

        args["front"] = _front_setting_by_name[self.front]

        return command_dict

    @staticmethod
    def parse_response(data: dict) -> LockUnlockFrontCoverResponse:
        return LockUnlockFrontCoverResponse(
            command_id=data["command_id"],
            raw_cover_lock_status_as_block_data=data["raw_cover_lock_status_as_block_data"],
            raw_cover_lock_status_flag=data["raw_cover_lock_status_flag"],
        )
