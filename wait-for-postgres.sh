#!/bin/sh

# Script to wait for PostgreSQL to become available

host="$DB_HOST"
port="$DB_PORT"
cmd="$@"

# Function to check if PostgreSQL is ready
wait_for_postgres() {
  while ! nc -z "$host" "$port"; do
    echo "Waiting for PostgreSQL to become available at $host:$port..."
    sleep 1
  done
  echo "PostgreSQL is available at $host:$port"
}

# Execute the function and then run the command
wait_for_postgres && exec "$cmd"
