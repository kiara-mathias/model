from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator

INCH_TO_CM = 2.54


class Unit(str, Enum):
    cm = "cm"
    inches = "in"


# Plausible adult ranges in cm: (min, max). Tune these later.
RANGES = {
    "height":    (120, 230),
    "bust":      (60, 170),
    "waist":     (45, 150),
    "hips":      (70, 180),
    "shoulders": (30, 60),   # shoulder width, seam to seam across the back
    "inseam":    (50, 110),
}


class MeasurementsInput(BaseModel):
    unit: Unit = Unit.cm
    height: float = Field(gt=0)
    bust: float = Field(gt=0)
    waist: float = Field(gt=0)
    hips: float = Field(gt=0)
    shoulders: float = Field(gt=0)
    inseam: Optional[float] = Field(default=None, gt=0)

    @model_validator(mode="after")
    def convert_to_cm_and_validate(self):
        # Convert everything to cm so the rest of the app only deals with one unit
        if self.unit == Unit.inches:
            for name in RANGES:
                value = getattr(self, name)
                if value is not None:
                    setattr(self, name, round(value * INCH_TO_CM, 1))
            self.unit = Unit.cm

        # Range checks (done after conversion so they work for both units)
        for name, (low, high) in RANGES.items():
            value = getattr(self, name)
            if value is not None and not (low <= value <= high):
                raise ValueError(
                    f"{name} must be between {low} and {high} cm (got {value} cm)"
                )

        # Basic sanity check between measurements
        if self.waist > max(self.bust, self.hips) * 1.3:
            raise ValueError("waist looks too large compared to bust and hips")

        return self