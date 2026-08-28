from datetime import datetime, timezone
import pytest
from app.domain.entities.area import Area, AreaStatus, AreaType
from app.domain.value_objects.coordinate import Coordinate
from app.api.v1.mappers.area_mapper import AreaMapper

def test_area_to_response_mapper():
    coordinate = Coordinate(latitude=-6.2, longitude=106.8)
    area = Area(
        id="area_123",
        name="Pondok Kacang",
        code="PK",
        status=AreaStatus.ACTIVE,
        type=AreaType.DISTRICT,
        coordinate=coordinate,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    resp = AreaMapper.to_response(area)
    assert resp.area_id == "area_123"
    assert resp.area_name == "Pondok Kacang"
    assert resp.status == "ACTIVE"
    assert resp.location is not None
    assert resp.location.latitude == -6.2
    assert resp.location.longitude == 106.8

def test_area_to_response_mapper_no_location():
    area = Area(
        id="area_123",
        name="Pondok Kacang",
        code="PK",
        status=AreaStatus.ACTIVE,
        type=AreaType.DISTRICT,
        coordinate=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    resp = AreaMapper.to_response(area)
    assert resp.area_id == "area_123"
    assert resp.location is None
