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

# First run the migrations
# $PSQL -f migrations/test_case_examples.sql

# Create a temporary SQL file for loading data
cat > /tmp/load_data.sql << EOF
BEGIN;
CREATE TABLE IF NOT EXISTS temp_raw_json (content TEXT);
\copy temp_raw_json FROM PROGRAM 'jq --stream -nc -f documents/test_case_examples_good.json';
INSERT INTO test_case_examples (quality, test_case)
SELECT 
    'good'::test_case_quality AS quality,
    jsonb_build_object(
        'test_case', jsonb_build_object(
            'title', elem->>'title',
            'preconditions', elem->'preconditions',
            'steps', elem->'steps',
            'expected_outcome', elem->>'expected_outcome'
        )
    )
FROM 
    temp_raw_json,
    jsonb_array_elements(content::jsonb) AS elem;
COMMIT;
EOF

# Run the data loading script
echo "Загружаем данные..."
$PSQL -f /tmp/load_data.sql

# Clean up
rm /tmp/load_data.sql


if [ $? -eq 0 ]; then
    echo "Миграция успешно применена!"
else
    echo "Ошибка применения миграции. Проверьте логи выше."
    exit 1
fi