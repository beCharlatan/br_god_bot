#!/bin/bash
# chmod +x migrations/run.sh
# ./migrations/run.sh

set -a
source .env
set +a

if [[ -z "$DB_HOST" || -z "$DB_PORT" || -z "$DB_NAME" || -z "$DB_USER" || -z "$DB_PASSWORD" ]]; then
    echo "Ошибка: Не все переменные окружения заданы"
    exit 1
fi

PSQL="psql -v ON_ERROR_STOP=1 -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER"

echo "Применяем миграцию..."
$PSQL -f migrations/test_case_examples.sql

if [ $? -eq 0 ]; then
    echo "Миграция успешно применена!"
else
    echo "Ошибка применения миграции. Проверьте логи выше."
    exit 1
fi