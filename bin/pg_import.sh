#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

FILE_DIR="$(cd "$(dirname "$2")"; pwd)"

if [ "$1" == "-h" -o "$1" == "--help" ]; then
    echo "Import SQL dump into PostgreSQL database."
    echo ""
    echo "Usage: `basename $0` {--production|--beta|--staging|--local[default]} infile"
    echo "       `basename $0` {-h|--help}"
    exit 0
elif [ "$1" == "--production" ]; then
    ENV_FILE=prod.env
    SERVICE=pg-proxy
    OUTFILE=$2
elif [ "$1" == "--beta" ]; then
    ENV_FILE=beta.env
    SERVICE=pg-proxy
    OUTFILE=$2
elif [ "$1" == "--staging" ]; then
    ENV_FILE=staging.env
    SERVICE=pg-proxy
    OUTFILE=$2
elif [ "$1" == "--local" ]; then
    ENV_FILE=.env
    SERVICE=postgres
    OUTFILE=$2
else
    OUTFILE=$1
    ENV_FILE=.env
    SERVICE=postgres
fi

if [ -z "$OUTFILE" ]; then
    echo "Must specify infile."
    exit 1
fi

source $ENV_FILE
export $(cut -d= -f1 $ENV_FILE)

docker-compose up -d $SERVICE
if [ "$SERVICE" == "postgres" ]; then
    docker-compose run -v $FILE_DIR:/app psql dropdb -U postgres -h $SERVICE $POSTGRES_APP_DB
    docker-compose run -v $FILE_DIR:/app psql createdb -U postgres -h $SERVICE $POSTGRES_APP_DB
else
    echo "Not recreating database because not running on local. I hope you are running this on an empty database."
fi
docker-compose run -v $FILE_DIR:/app psql bash -c "psql -U postgres -h $SERVICE $POSTGRES_APP_DB < /app/$(basename $OUTFILE)"

if [ "$SERVICE" == "pg-proxy" ]; then
    docker-compose kill pg-proxy
fi
