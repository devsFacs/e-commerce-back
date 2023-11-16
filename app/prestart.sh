#! /usr/bin/env bash

# format the code
python /app/app/format_code.py

# Let the DB start
python /app/app/backend_pre_start.py

# Run migrations
#alembic upgrade head

# Create initial data in DB
python /app/app/initial_data.py
