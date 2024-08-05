#!/bin/sh

# Set the PostgreSQL user
export PGUSER="postgres"

# Create the database
psql -c "CREATE DATABASE inventory"

# Create the extension in the database
psql inventory -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"