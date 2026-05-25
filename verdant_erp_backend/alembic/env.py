import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from app.core.database import Base
from app.models import (
    user,
    role,
    token,
    customer,
    service_order,
    service_order_task,
    service_order_item,
    service_order_material,
    service_order_log,
    service_order_assignment,
    role_permission,
    permission
)
from app.core.config import settings

config = context.config

# 👇 Conectar con tu .env
config.set_main_option("sqlalchemy.url", settings.SYNC_DATABASE_URL)
from app.models import *  # 🔥 ESTO FUERZA EL REGISTRO

# IMPORTS CRÍTICOS
from app.models.customer import *
from app.models.crm import *

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
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
