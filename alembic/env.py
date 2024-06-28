from logging.config import fileConfig
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context
from bot.db.entities import Entity
from bot.db.postgers_settings import settings

load_dotenv(".env")  # Загрузка переменных окружения из .env файла

# Получаем конфигурацию Alembic
config = context.config
# Устанавливаем URL подключения к базе данных
config.set_main_option("sqlalchemy.url", settings.postgres_connection_url.render_as_string(hide_password=False))

# Настройка логгирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Установка метаданных для автогенерации миграций
target_metadata = Entity.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме."""
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
    """Запуск миграций в 'online' режиме."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
