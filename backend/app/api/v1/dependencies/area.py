"""Area Dependencies."""
from fastapi import Depends
from typing import List, Optional
from app.domain.interfaces.area_repository import IAreaRepository as AreaRepository
from app.api.v1.services.area_service import AreaApplicationService
from app.domain.entities.area import Area, AreaStatus
from app.domain.value_objects.geography import Coordinate, AreaCode, Latitude, Longitude

class MockAreaRepository(AreaRepository):
    def __init__(self):
        self.areas = [
            Area(
                id="area-1",
                code=AreaCode(value="JKT-001"),
                name="Jakarta Pusat",
                province="DKI Jakarta",
                city="Jakarta Pusat",
                district="Menteng",
                village="Menteng",
                postal_code="10310",
                center_coordinate=Coordinate(latitude=Latitude(value=-6.1944), longitude=Longitude(value=106.8229)),
                elevation=5.0,
                area_size=10.0,
                status=AreaStatus.ACTIVE
            ),
            Area(
                id="area-2",
                code=AreaCode(value="JKT-002"),
                name="Jakarta Selatan",
                province="DKI Jakarta",
                city="Jakarta Selatan",
                district="Kebayoran Baru",
                village="Senayan",
                postal_code="12190",
                center_coordinate=Coordinate(latitude=Latitude(value=-6.2333), longitude=Longitude(value=106.8000)),
                elevation=10.0,
                area_size=15.0,
                status=AreaStatus.ACTIVE
            )
        ]
        
    async def save(self, area: Area) -> Area:
        return area
        
    async def find_by_id(self, id: str) -> Optional[Area]:
        for a in self.areas:
            if a.id == id:
                return a
        return None
        
    async def find_by_code(self, code: str) -> Optional[Area]:
        return self.areas[0] if self.areas else None
        
    async def exists(self, id: str) -> bool:
        return any(a.id == id for a in self.areas)
        
    async def list(self) -> List[Area]:
        return self.areas
        
    async def delete(self, id: str) -> None:
        pass

def get_area_repository() -> AreaRepository:
    return MockAreaRepository()

def get_area_service(repository: AreaRepository = Depends(get_area_repository)) -> AreaApplicationService:
    return AreaApplicationService(repository)
