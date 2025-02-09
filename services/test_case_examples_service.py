from typing import List, Dict, Any, Optional
from config.database import db
from sqlalchemy import select
from sqlalchemy.sql.expression import desc


class TestCaseExamplesService:
    """Сервис для работы с примерами тест-кейсов"""

    @staticmethod
    def get_good_examples(limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Получение примеров хороших тест-кейсов
        
        Args:
            limit: Ограничение количества возвращаемых записей
            
        Returns:
            List[Dict]: Список тест-кейсов с оценкой 'good'
        """
        with next(db.get_db()) as session:
            query = select([
                "example_id",
                "test_case",
                "created_at",
                "updated_at"
            ]).select_from("test_case_examples").where(
                "quality = 'good'"
            ).order_by(desc("created_at"))

            if limit:
                query = query.limit(limit)

            result = session.execute(query)
            return [dict(row) for row in result]

    @staticmethod
    def get_bad_examples(limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Получение примеров плохих тест-кейсов
        
        Args:
            limit: Ограничение количества возвращаемых записей
            
        Returns:
            List[Dict]: Список тест-кейсов с оценкой 'bad'
        """
        with next(db.get_db()) as session:
            query = select([
                "example_id",
                "test_case",
                "created_at",
                "updated_at"
            ]).select_from("test_case_examples").where(
                "quality = 'bad'"
            ).order_by(desc("created_at"))

            if limit:
                query = query.limit(limit)

            result = session.execute(query)
            return [dict(row) for row in result]