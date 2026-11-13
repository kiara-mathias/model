import pytest
from pydantic import ValidationError
from app.models import MeasurementsInput


def test_valid_cm_input():
    m = MeasurementsInput(height=165, bust=90, waist=70, hips=96, shoulders=38)
    assert m.height == 165


def test_inches_are_converted_to_cm():
    m = MeasurementsInput(unit="in", height=65, bust=36, waist=28, hips=38, shoulders=15)
    assert m.unit == "cm"
    assert m.height == 165.1


def test_impossible_waist_rejected():
    with pytest.raises(ValidationError):
        MeasurementsInput(height=165, bust=90, waist=200, hips=96, shoulders=38)


def test_missing_field_rejected():
    with pytest.raises(ValidationError):
        MeasurementsInput(height=165, bust=90, waist=70, hips=96)