from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from os import environ

# Импортируйте Base и модели
from api.database import Base
from api.models import DeviceData  # И другие модели

# Метаданные для автогенерации миграций
target_metadata = Base.metadata

# Настройка логгера
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Загрузка URL базы данных из переменной окружения
DATABASE_URL = environ.get("DATABASE_URL", "postgresql://user:password@db:5432/mydb")
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
