-- migrations/0002_create_test_case_examples_table.sql

-- Создаем тип для оценки качества тест-кейса
CREATE TYPE test_case_quality AS ENUM ('good', 'bad');

-- Создаем таблицу с примерами тест-кейсов
CREATE TABLE IF NOT EXISTS test_case_examples (
    example_id SERIAL PRIMARY KEY,
    quality test_case_quality NOT NULL,
    test_case JSONB NOT NULL,
);

-- Комментарии к таблице и полям
COMMENT ON TABLE test_case_examples IS 'Хранит примеры тест-кейсов для обучения ИИ-агентов';
COMMENT ON COLUMN test_case_examples.example_id IS 'Уникальный идентификатор примера';
COMMENT ON COLUMN test_case_examples.quality IS 'Оценка качества тест-кейса (хороший/плохой)';
COMMENT ON COLUMN test_case_examples.test_case IS 'Сам тест-кейс в структурированном формате';

-- Добавляем расширение для генерации UUID (на случай будущего использования)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- INSERT INTO test_case_examples (quality, test_case)
-- SELECT 
--     'good'::test_case_quality AS quality,
--     jsonb_build_object(
--         'test_case', jsonb_build_object(
--             'title', elem->>'title',
--             'preconditions', elem->'preconditions',
--             'steps', elem->'steps',
--             'expected_outcome', elem->>'expected_outcome'
--         )
--     )
-- FROM 
--     temp_raw_json,
--     jsonb_array_elements(content::jsonb) AS elem;
-- DROP TABLE temp_raw_json;