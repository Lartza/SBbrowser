#!/bin/bash

TIME=$(date +%s)

curl --no-progress-meter -o "database.db" https://sponsor.ajay.app/database.db

pgloader sponsorblock.load
PGPASSWORD=changeme psql -U sponsorblock sponsorblock -c "INSERT INTO sbtmp.config VALUES ('updated', to_timestamp($TIME) AT TIME ZONE 'UTC'); DROP SCHEMA public CASCADE; ALTER SCHEMA sbtmp RENAME TO public;"