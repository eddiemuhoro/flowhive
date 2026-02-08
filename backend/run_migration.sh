#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run the migration
alembic upgrade head

echo "Migration completed!"
