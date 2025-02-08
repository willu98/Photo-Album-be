import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Alembic Config object
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your SQLAlchemy Base and its metadata
from database.database import Base
target_metadata = [Base.metadata]

# Construct database URL from environment variables
DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URI')

# Override sqlalchemy.url in alembic config
config.set_main_option("sqlalchemy.url", str("postgresql://postgres:password@localhost/postgres"))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    print("running offline made")
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    print("running online made")
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        print(connection)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
