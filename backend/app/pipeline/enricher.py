"""Enriches Canonical Records with pipeline metadata."""
from typing import List
from datetime import datetime, timezone
from app.pipeline.canonical import CanonicalRecord
from app.pipeline.context import PipelineContext

class DataEnricher:
    @staticmethod
    def enrich(records: List[CanonicalRecord], context: PipelineContext) -> List[CanonicalRecord]:
        enrichment_tags = {
            "pipeline_version": "1.0",
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "trace_id": context.trace_id,
            "provider_id": context.provider_id
        }
        
        for record in records:
            record.enrichment_tags.update(enrichment_tags)
            
        return records
