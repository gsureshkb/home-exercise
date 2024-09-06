#!/bin/bash
# wait-for-it.sh script

host="$1"
shift
cmd="$@"

until nc -z "$host" 5432; do
  echo "Waiting for database..."
  sleep 1
done

exec $cmd
