class HamiltonError(Exception):
    """
    Errors that can be returned by the Hamilton device.
    """


class HamiltonSyntaxError(HamiltonError):
    """
    There is an incorrect set of parameters or parameter ranges.
    """


class HardwareError(HamiltonError):
    """
    Steps lost on one or more hardware components, or component not initialized or not functioning.
    """


class NotExecutedError(HamiltonError):
    """
    There was an error in previous part command.
    """


class ClotError(HamiltonError):
    """
    Blood clot detected.
    """


class BarcodeError(HamiltonError):
    """
    Barcode could not be read or is missing.
    """


class InsufficientLiquidError(HamiltonError):
    """
    Not enough liquid available.
    """


class TipPresentError(HamiltonError):
    """
    A tip has already been picked up.
    """


class NoTipError(HamiltonError):
    """
    Tip is missing or not picked up.
    """


class NoCarrierError(HamiltonError):
    """
    No carrier present for loading.
    """


class ExecutionError(HamiltonError):
    """
    A step or a part of a step could not be processed.
    """


class PressureLLDError(HamiltonError):
    """
    A dispense with pressure liquid level detection is not allowed.
    """


class CalibrateError(HamiltonError):
    """
    No capacitive signal detected during carrier calibration procedure.
    """


class UnloadError(HamiltonError):
    """
    Not possible to unload the carrier due to occupied loading tray position.
    """


class ParameterError(HamiltonError):
    """
    Dispense in jet mode with pressure liquid level detection is not allowed.
    """


class CoverOpenError(HamiltonError):
    """
    Cover not closed or can not be locked.
    """


class ImproperAspirationError(HamiltonError):
    """
    Improper Dispense Error
    The pressure-based aspirate/dispense control reported an error ( not enough liquid ).
    """


class WashLiquidError(HamiltonError):
    """
    Waste is full or no more wash liquid is available.
    """


class TemperatureError(HamiltonError):
    """
    Incubator temperature out of range.
    """


class TADMovershot(HamiltonError):
    """
    Overshot of limits during aspirate or dispense.

    Note:
    On aspirate this error is returned as main error 17.
    On dispense this error is returned as main error 4.

    """


class LabwareError(HamiltonError):
    """
    Labware not available.
    """


class LabwareGrippedError(HamiltonError):
    """
    Labware already gripped.
    """


class LabwareLostError(HamiltonError):
    """
    Labware lost during transport.
    """


class Illegaltargetplateposition(HamiltonError):
    """
    Unable to place plate; plate was gripped in the wrong direction.
    """


class IllegalInterventionError(HamiltonError):
    """
    Cover was opened or a carrier was removed manually.
    """


class TADMundershot(HamiltonError):
    """
    Undershot of limits during aspirate or dispense.

    Note:
    On aspirate this error is returned as main error 4.
    On dispense this error is returned as main error 17.

    """


class PositionError(HamiltonError):
    """
    The position is out of range.
    """


class UnexpectedcLLDError(HamiltonError):
    """
    The cLLD detected a liquid level above start height of liquid level search.
    """


class Areaalreadyoccupied(HamiltonError):
    """
    Instrument region already reserved.
    """


class Impossibletooccupyarea(HamiltonError):
    """
    Unable to reserve a region on the instrument.
    """


class Antidropcontrolerror(HamiltonError):
    """
    Anti drop controlling out of tolerance.
    """


class Decappererror(HamiltonError):
    """
    Decapper lock error while screw / unscrew a cap by twister channels.
    """


class Decapperhandlingerror(HamiltonError):
    """
    Decapper station error while lock / unlock a cap.
    """


class SlaveError(HamiltonError):
    """
    Slave error.
    """


class WrongCarrierError(HamiltonError):
    """
    Incorrect carrier barcode detected.
    """


class NoCarrierBarcodeError(HamiltonError):
    """
    Carrier barcode could not be read or is missing.
    """


class LiquidLevelError(HamiltonError):
    """
    Liquid surface not detected.
    This error is created from main/slave errors 06/70, 06/73 and 06/87.
    """


class NotDetectedError(HamiltonError):
    """
    Carrier not detected at deck end position.
    """


class NotAspiratedError(HamiltonError):
    """
    Dispense volume exceeds the aspirated volume.
    This error is created from main / slave error 02/54.
    """


class ImproperDispensationError(HamiltonError):
    """
    The dispensed volume is out of tolerance (may only occur for Nano Pipettor Dispense steps).
    This error is created from main/slave errors 02/52 and 02/54.
    """


class NoLabwareError(HamiltonError):
    """
    The labware to be loaded was not detected by autoload module.

    Note:
    Can only occur on a Reload Carrier step if the labware property 'MlStarCarPosAreRecognizable' is set to 1.

    """


class UnexpectedLabwareError(HamiltonError):
    """
    The labware contains an unexpected barcode (can only occur on a Reload Carrier step).
    """


class WrongLabwareError(HamiltonError):
    """
    The labware to be reloaded contains the incorrect barcode (can only occur on a Reload Carrier step).
    """


class BarcodeMaskError(HamiltonError):
    """
    The barcode read doesn't match the barcode mask defined.
    """


class BarcodeNotUniqueError(HamiltonError):
    """
    The barcode read is not unique. Previously loaded labware with the same barcode was loaded without unique barcode check.
    """


class BarcodeAlreadyUsedError(HamiltonError):
    """
    The barcode read is already loaded as unique barcode (i.e., it's not possible to load the same barcode twice ).
    """


class KitLotExpiredError(HamiltonError):
    """
    Kit Lot expired.
    """


class DelimiterError(HamiltonError):
    """
    Barcode contains a character that is used as a delimiter in the result string.
    """


error_by_main_error_number = {
    1: HamiltonSyntaxError,
    2: HardwareError,
    3: NotExecutedError,
    4: ClotError,
    5: BarcodeError,
    6: InsufficientLiquidError,
    7: TipPresentError,
    8: NoTipError,
    9: NoCarrierError,
    10: ExecutionError,
    11: PressureLLDError,
    12: CalibrateError,
    13: UnloadError,
    14: PressureLLDError,
    15: ParameterError,
    16: CoverOpenError,
    17: ImproperAspirationError,
    18: WashLiquidError,
    19: TemperatureError,
    20: TADMovershot,
    21: LabwareError,
    22: LabwareGrippedError,
    23: LabwareLostError,
    24: Illegaltargetplateposition,
    25: IllegalInterventionError,
    26: TADMundershot,
    27: PositionError,
    28: UnexpectedcLLDError,
    29: Areaalreadyoccupied,
    30: Impossibletooccupyarea,
    31: Antidropcontrolerror,
    32: Decappererror,
    33: Decapperhandlingerror,
    99: SlaveError,
    100: WrongCarrierError,
    101: NoCarrierBarcodeError,
    102: LiquidLevelError,
    103: NotDetectedError,
    104: NotAspiratedError,
    105: ImproperDispensationError,
    106: NoLabwareError,
    107: UnexpectedLabwareError,
    108: WrongLabwareError,
    109: BarcodeMaskError,
    110: BarcodeNotUniqueError,
    111: BarcodeAlreadyUsedError,
    112: KitLotExpiredError,
    113: DelimiterError,
}
