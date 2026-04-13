import dataclasses
import typing

from .errors import HamiltonError, _main_error_by_id

_err_flag_by_id: dict[int, typing.Literal["No error", "Recoverable error", "Fatal error"]] = {
    0: "No error",
    1: "Recoverable error",
    2: "Fatal error",
}

_recovery_button_by_id: dict[
    int,
    None
    | typing.Literal[
        "Abort",
        "Cancel",
        "Initialize",
        "Repeat",
        "Exclude",
        "Waste",
        "Air",
        "Bottom",
        "Continue",
        "Barcode",
        "Next",
        "Available",
        "Refill",
    ],
] = {
    0: None,
    1: "Abort",
    2: "Cancel",
    3: "Initialize",
    4: "Repeat",
    5: "Exclude",
    6: "Waste",
    7: "Air",
    8: "Bottom",
    9: "Continue",
    10: "Barcode",
    11: "Next",
    12: "Available",
    13: "Refill",
}


@dataclasses.dataclass(frozen=True)
class HamiltonStepReturnBlockDataPackage:
    """Base class for hamilton block data package."""

    @dataclasses.dataclass(frozen=True)
    class _StepReturnBlockData:
        """Base class for hamilton block data."""

        num: int
        main_err: None | type[HamiltonError]
        slave_err: None | str
        recovery_button: (
            None
            | typing.Literal[
                "Abort",
                "Cancel",
                "Initialize",
                "Repeat",
                "Exclude",
                "Waste",
                "Air",
                "Bottom",
                "Continue",
                "Barcode",
                "Next",
                "Available",
                "Refill",
            ]
        )
        step_data: typing.Any | None
        labware_name: str
        labware_pos: str

    err_flag: typing.Literal["No error", "Recoverable error", "Fatal error"]
    block_data: list[_StepReturnBlockData]

    @staticmethod
    def parse_raw_step_return(raw_step_return: str) -> "HamiltonStepReturnBlockDataPackage":
        raw_block_data = raw_step_return.split("[")
        err_flag_id = raw_block_data.pop(0)

        block_data = []
        for data in raw_block_data:
            values = data.split(",")
            if len(values) != 7:
                raise ValueError(f"Invalid block data: {data}")

            block_data.append(
                HamiltonStepReturnBlockDataPackage._StepReturnBlockData(
                    num=int(values[0]),
                    main_err=_main_error_by_id[int(values[1])],
                    slave_err=values[2] if values[2] != "0" else None,
                    recovery_button=_recovery_button_by_id[int(values[3])],
                    step_data=values[4] if values[4] != "" else None,
                    labware_name=values[5],
                    labware_pos=values[6],
                ),
            )

        return HamiltonStepReturnBlockDataPackage(
            err_flag=_err_flag_by_id[int(err_flag_id)],
            block_data=block_data,
        )


@dataclasses.dataclass(frozen=True)
class HamiltonStepReturnStructuredDataPackage:
    """Base class for hamilton block data package."""

    @dataclasses.dataclass(frozen=True)
    class _StepReturnStructuredData:
        """Base class for hamilton block data."""

        num: int
        data: typing.Any

    structured_data: list[_StepReturnStructuredData]

    @staticmethod
    def parse_raw_step_return(raw_step_return: str) -> "HamiltonStepReturnStructuredDataPackage":
        raw_description_data = raw_step_return.split("[")
        raw_description_data.pop(0)  # First element is always empty.

        structured_data = []
        for data in raw_description_data:
            values = data.split(",")
            if len(values) != 2:
                raise ValueError(f"Invalid description data: {data}")

            structured_data.append(
                HamiltonStepReturnStructuredDataPackage._StepReturnStructuredData(
                    num=int(values[0]),
                    data=values[1],
                ),
            )

        return HamiltonStepReturnStructuredDataPackage(
            structured_data=structured_data,
        )
