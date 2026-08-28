import sys
import types
app_core_config = types.ModuleType('app.core.config')
app_core_config.settings = type('Settings', (), {'BMKG_COLLECTOR': {}})()
sys.modules['app.core.config'] = app_core_config

import asyncio
from app.collectors.providers.bmkg.collector import BMKGCollector
from app.pipeline.pipeline import EnterprisePipeline

async def main():
    collector = BMKGCollector()
    print("Testing BMKG Collector + Pipeline...")
    try:
        # Fetch with adm4 code
        raw_data = await collector.fetch(adm4_code="31.71.06.1001")
        print(f"Raw data length: {len(raw_data.raw_content)}")
        
        parsed = await collector.parse(raw_data)
        print(f"Parsed keys: {parsed.model_dump().keys() if hasattr(parsed, 'model_dump') else type(parsed)}")
        print(f"Lokasi metadata: {parsed.lokasi}")
        
        normalized = await collector.normalize(parsed)
        print(f"Normalized data time_series count: {len(normalized.time_series)}")
        
        # Now run the pipeline
        print("Running EnterprisePipeline...")
        canonical_records = EnterprisePipeline.process(normalized, "BMKG")
        print(f"Canonical records: {len(canonical_records)}")
        if canonical_records:
            print("First record:")
            print(canonical_records[0].model_dump_json(indent=2))
    except Exception as e:
        print(f"Error: {e.__class__.__name__} - {str(e)}")
    finally:
        await collector.disconnect()

if __name__ == "__main__":
    asyncio.run(main())


