"""Normalizes BMKG Parsed Data into Canonical NormalizedData DTO."""
from datetime import datetime, timezone
from app.collectors.providers.bmkg.models import BMKGParsedData
from app.collectors.dto.normalized import NormalizedData
from app.core.logger import get_logger

logger = get_logger(__name__)

class BMKGNormalizer:
    @staticmethod
    def normalize(parsed_data: BMKGParsedData) -> NormalizedData:
        logger.debug("Normalization Started for BMKG data.")
        
        time_series = []
        
        lokasi_meta = parsed_data.lokasi
        
        for data_block in parsed_data.data:
            block_lokasi = data_block.get("lokasi", {})
            # Fallback to top-level adm4 if block doesn't have it
            area_id = block_lokasi.get("adm4") or lokasi_meta.get("adm4")
            
            # cuaca is a list of lists of objects
            for cuaca_list in data_block.get("cuaca", []):
                for item in cuaca_list:
                    dt_str = item.get("datetime")
                    if dt_str:
                        try:
                            timestamp = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                        except ValueError:
                            timestamp = datetime.utcnow()
                    else:
                        timestamp = datetime.utcnow()
                        
                    # Extract fields
                    for param in ["t", "hu", "tp", "ws", "wd", "wd_deg", "weather", "weather_desc", "tcc"]:
                        if param in item:
                            time_series.append({
                                "area_id": area_id,
                                "timestamp": timestamp,
                                "parameter": param,
                                "value": item[param]
                            })
                            
        return NormalizedData(
            provider_id="BMKG",
            normalized_time=datetime.now(timezone.utc),
            location_data=lokasi_meta,
            time_series=time_series
        )
