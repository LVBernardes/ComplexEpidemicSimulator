import logging
from enum import Enum

from complex_epidemics.utils.exceptions import InvalidOptionError

LOG = logging.getLogger(__name__)


class ProtectionMeasureType(Enum):
    HANDWASHING = "HandWashing"
    MASKWEARING = "MaskWearing"
    SOCIALDISTANCING = "SocialDistancing"


class ApplicationQuality(Enum):
    POOR = 0.33
    GOOD = 0.66
    EXCELLENT = 1.0


class MaskType(Enum):
    CLOTH = 0.5
    SURGICAL = 0.7
    RESPIRATOR = 0.95


class ProtectionMeasure:

    __slots__ = ["_type", "_application", "_efficacy"]

    def __init__(self):
        self._type = None
        self._application: ApplicationQuality = ApplicationQuality.EXCELLENT
        self._efficacy: float = 0.0

    @property
    def type(self) -> ProtectionMeasureType:
        return self._type

    @type.setter
    def type(self, value: ProtectionMeasureType) -> None:
        self._type = value

    @property
    def application(self) -> ApplicationQuality:
        return self._application

    @application.setter
    def application(self, value: ApplicationQuality) -> None:
        self._application = value

    @property
    def efficacy(self) -> float:
        return self._efficacy

    @efficacy.setter
    def efficacy(self, value: float) -> None:
        self._efficacy = value

    def change_application_quality(self, new_quality: ApplicationQuality):
        self.application = new_quality

    @property
    def get_efficacy(self):
        if self.application == ApplicationQuality.POOR:
            return round(self.efficacy * self.application.value, 3)
        elif self.application == ApplicationQuality.GOOD:
            return round(self.efficacy * self.application.value, 3)
        elif self.application == ApplicationQuality.EXCELLENT:
            return round(self.efficacy * self.application.value, 3)
        else:
            LOG.debug("Application quality option not implemented.")
            raise InvalidOptionError("Application quality option not implemented.")


class HandWashing(ProtectionMeasure):
    def __init__(self):
        super().__init__()
        self._efficacy: float = 0.2


class MaskWearing(ProtectionMeasure):
    def __init__(self, mask_type: MaskType = MaskType.CLOTH):
        super().__init__()
        self._mask_type = mask_type
        self._efficacy: float = mask_type.value

    @property
    def mask_type(self) -> MaskType:
        return self._mask_type

    @mask_type.setter
    def mask_type(self, value: MaskType) -> None:
        self._mask_type = value
        self.efficacy = value.value


class SocialDistancing(ProtectionMeasure):
    def __init__(self):
        super().__init__()
        self._efficacy: float = 0.8
