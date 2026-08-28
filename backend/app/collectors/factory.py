"""Factory for instantiating collectors."""
from app.collectors.registry import CollectorRegistry
from app.collectors.base import BaseCollector
from app.collectors.pipeline import CollectorPipeline

class CollectorFactory:
    """Creates Collector instances and wraps them in Pipelines."""
    
    @staticmethod
    def create_provider(provider_name: str) -> BaseCollector:
        provider_class = CollectorRegistry.get_provider_class(provider_name)
        # Instantiate with its registered config key (using provider_name by default)
        return provider_class(config_key=provider_name)
        
    @staticmethod
    def create_pipeline(provider_name: str) -> CollectorPipeline:
        provider = CollectorFactory.create_provider(provider_name)
        return CollectorPipeline(provider=provider)
