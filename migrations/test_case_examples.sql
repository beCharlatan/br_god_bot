-- migrations/0002_create_test_case_examples_table.sql

-- Создаем тип для оценки качества тест-кейса
CREATE TYPE test_case_quality AS ENUM ('good', 'bad');

-- Создаем таблицу с примерами тест-кейсов
CREATE TABLE IF NOT EXISTS test_case_examples (
    example_id SERIAL PRIMARY KEY,
    quality test_case_quality NOT NULL,
    test_case JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Комментарии к таблице и полям
COMMENT ON TABLE test_case_examples IS 'Хранит примеры тест-кейсов для обучения ИИ-агентов';
COMMENT ON COLUMN test_case_examples.example_id IS 'Уникальный идентификатор примера';
COMMENT ON COLUMN test_case_examples.quality IS 'Оценка качества тест-кейса (хороший/плохой)';
COMMENT ON COLUMN test_case_examples.test_case IS 'Сам тест-кейс в структурированном формате';
COMMENT ON COLUMN test_case_examples.created_at IS 'Дата создания записи';
COMMENT ON COLUMN test_case_examples.updated_at IS 'Дата последнего обновления';

-- Создаем триггер для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_test_case_examples_modtime
BEFORE UPDATE ON test_case_examples
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Добавляем расширение для генерации UUID (на случай будущего использования)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Обновляем путь к файлу и структуру запроса
DO $$
DECLARE
    json_data JSONB := pg_read_file('documents/test_case_examples_good.json')::JSONB;
BEGIN
    INSERT INTO test_case_examples (quality, test_case)
    SELECT 
        'good'::test_case_quality AS quality,
        jsonb_build_object(
            'test_case', jsonb_build_object(
                'id', tc->>'id',
                'title', tc->>'title',
                'scenario', tc->'scenario',
                'validation_rules', tc->'validation_rules',
                'tags', ARRAY['авторизация', 'ролевая модель']::JSONB
            )
        )
    FROM 
        jsonb_array_elements(json_data->'test_cases') tc;
EXCEPTION
    WHEN others THEN
        RAISE NOTICE 'Ошибка при загрузке тест-кейсов: %', SQLERRM;
END $$;