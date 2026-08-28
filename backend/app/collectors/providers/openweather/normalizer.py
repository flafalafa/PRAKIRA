"""Normalizes OpenWeather Parsed Data into Canonical NormalizedData DTO."""
from datetime import datetime, timezone
from app.collectors.providers.openweather.models import OpenWeatherParsedData
from app.collectors.dto.normalized import NormalizedData
from app.core.logger import get_logger

logger = get_logger(__name__)

class OpenWeatherNormalizer:
    @staticmethod
    def normalize(parsed_data: OpenWeatherParsedData) -> NormalizedData:
        logger.debug("Normalization Started for OpenWeather data.")
        
        area_id = f"ow_loc_{parsed_data.lat}_{parsed_data.lon}"
        time_series = []
        
        # Process current weather
        if parsed_data.current:
            dt = datetime.fromtimestamp(parsed_data.current.get("dt", 0), tz=timezone.utc)
            metrics = {
                "temperature": parsed_data.current.get("temp"),
                "humidity": parsed_data.current.get("humidity"),
                "pressure": parsed_data.current.get("pressure"),
                "wind_speed": parsed_data.current.get("wind_speed"),
                "wind_direction": parsed_data.current.get("wind_deg"),
                "cloud_coverage": parsed_data.current.get("clouds"),
                "visibility": parsed_data.current.get("visibility")
            }
            # Rainfall in OpenWeather is often under 'rain' -> '1h'
            if "rain" in parsed_data.current and isinstance(parsed_data.current["rain"], dict):
                metrics["rainfall"] = parsed_data.current["rain"].get("1h", 0.0)
            
            for param, value in metrics.items():
                if value is not None:
                    time_series.append({
                        "area_id": area_id,
                        "timestamp": dt,
                        "parameter": param,
                        "value": value
                    })
                    
        # Process hourly forecast
        for h in (parsed_data.hourly or []):
            dt = datetime.fromtimestamp(h.get("dt", 0), tz=timezone.utc)
            metrics = {
                "temperature": h.get("temp"),
                "humidity": h.get("humidity"),
                "rainfall": h.get("rain", {}).get("1h", 0.0) if isinstance(h.get("rain"), dict) else 0.0
            }
            for param, value in metrics.items():
                if value is not None:
                    time_series.append({
                        "area_id": area_id,
                        "timestamp": dt,
                        "parameter": f"forecast_hourly_{param}",
                        "value": value
                    })
                    
        return NormalizedData(
            provider_id="OpenWeather",
            normalized_time=datetime.now(timezone.utc),
            time_series=time_series,
            location_data={"lat": parsed_data.lat, "lon": parsed_data.lon}
        )
