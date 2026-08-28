import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Setup Enterprise Logging
from app.core.logging_config import setup_enterprise_logging
setup_enterprise_logging()

from app.core.logger import get_logger
logger = get_logger("alembic.env")

# Import target metadata and settings
from app.persistence.metadata import metadata
from app.persistence.registry import register_models
from app.config.settings import settings

# Ensure all models are registered before generating migrations
register_models()
target_metadata = metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Overwrite sqlalchemy.url with our settings URL to support environment-aware configurations
db_uri = settings.db.uri.get_secret_value() if settings.db.uri else "sqlite+aiosqlite:///:memory:"
config.set_main_option("sqlalchemy.url", db_uri)
logger.info(f"Alembic connected to environment: {settings.app.environment.value}")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    logger.info("Running migrations offline")
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        logger.info("Migration/Rollback Started (Offline)")
        try:
            context.run_migrations()
            logger.info("Migration/Rollback Finished (Offline)")
        except Exception as e:
            logger.critical(f"Migration/Rollback Failed (Offline): {e}")
            raise


def do_run_migrations(connection: Connection) -> None:
    logger.info("Running migrations online")
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        compare_type=True  # Detect column type changes
    )

    with context.begin_transaction():
        logger.info("Migration/Rollback Started (Online)")
        try:
            context.run_migrations()
            logger.info("Migration/Rollback Finished (Online)")
        except Exception as e:
            logger.critical(f"Migration/Rollback Failed (Online): {e}")
            raise


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
