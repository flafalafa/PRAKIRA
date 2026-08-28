"""BMKG Data Transformer for Enterprise Pipeline."""
from typing import List, Dict, Any
from app.collectors.dto.normalized import NormalizedData
from app.pipeline.registry import PipelineRegistry

def transform_bmkg(normalized_data: NormalizedData) -> List[Dict[str, Any]]:
    """
    Transforms BMKG NormalizedData into a list of CanonicalRecord compatible dictionaries.
    Groups parameters sharing the same area and timestamp into a single record.
    Provider-specific BMKG parameter codes are translated to canonical names here so that
    downstream Decision Engines remain provider-agnostic.
    """
    # Translate BMKG-specific codes to provider-neutral canonical names.
    # Keys: raw BMKG parameter names. Values: canonical domain parameter names.
    PARAM_MAP = {
        "t":      "temperature",
        "hu":     "humidity",
        "tp":     "rainfall",
        "ws":     "wind_speed",
        "wd_deg": "wind_direction",
        "tcc":    "cloud_cover",
    }

    records: Dict[str, Dict[str, Any]] = {}
    
    # Extract location metadata
    loc_meta = getattr(normalized_data, "location_data", {}) or {}
    lat = float(loc_meta.get("lat", 0.0))
    lon = float(loc_meta.get("lon", 0.0))
    
    location = {
        "latitude": lat,
        "longitude": lon,
        "spatial_reference": "WGS84"
    }
    
    metadata = {
        "provider_id": "BMKG"
    }
    
    for item in (normalized_data.time_series or []):
        area_id = str(item.get("area_id", ""))
        timestamp = item["timestamp"]
        param = item["parameter"]
        value = item["value"]
        
        group_key = f"{area_id}_{timestamp.isoformat()}"
        
        if group_key not in records:
            # Deterministic Record ID based on provider, area, and timestamp
            record_id = f"BMKG_{area_id}_{int(timestamp.timestamp())}"
            records[group_key] = {
                "record_id": record_id,
                "timestamp": timestamp,
                "location": location,
                "metadata": metadata,
                "measurements": [],
                "enrichment_tags": {"area_id": area_id}
            }
            
        if param in ["wd", "weather_desc"]:
            # Non-float measurements are added to enrichment_tags
            records[group_key]["enrichment_tags"][param] = str(value)
            continue
            
        try:
            float_val = float(value)
        except (ValueError, TypeError):
            continue
            
        # Translate BMKG parameter to canonical name; fall back to the original if unmapped.
        canonical_param = PARAM_MAP.get(param, param)

        # Determine unit based on BMKG parameter conventions
        unit = ""
        if param == "t":
            unit = "C"
        elif param == "hu":
            unit = "%"
        elif param == "ws":
            unit = "km/h"
        elif param == "wd_deg":
            unit = "deg"
        elif param == "tp":
            unit = "mm"
        
        records[group_key]["measurements"].append({
            "parameter": canonical_param,
            "value": float_val,
            "unit": unit,
            "quality_score": 1.0
        })
        
    return list(records.values())

# Auto-register upon import
PipelineRegistry.register_transformer("BMKG", transform_bmkg)
