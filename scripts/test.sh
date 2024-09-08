set -x

VERSION=${1:-3.11}
COMMAND="docker compose --env-file .env.test"

$COMMAND build backend --build-arg VERSION=$VERSION -q
$COMMAND -f docker-compose.yml -f docker-compose.test.yml up backend --force-recreate --always-recreate-deps --abort-on-container-exit --no-log-prefix
CODE=$?
$COMMAND down -v
exit $CODE
