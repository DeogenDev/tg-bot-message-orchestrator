#!/bin/sh
set -eu

uv run alembic upgrade head

if [ "${RUN_MIGRATIONS_ONLY:-0}" = "1" ]; then
  exit 0
fi

exec uv run python -m src.main
