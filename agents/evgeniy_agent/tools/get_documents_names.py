from langchain.tools import tool
from services.document_store import DocumentStore
from typing import List


@tool
def get_documents_names() -> List[str]:
    """
    Получает все бизнес-требования (БТ) из хранилища документов для операций ИИ-агента

    Интерфейс:
        Входные данные: Отсутствуют
        Выходные данные: Список имён файлов БТ

    Ключевые особенности:
        - Прямая интеграция с сервисом DocumentStore
        - Возвращает оригинальные имена файлов для отслеживания
        - Совместим с экосистемой инструментов LangChain

    Использование:
        Когда ИИ-агенту необходимо:
        1. Проверить покрытие требований
        2. Перекрестно-ссылаться на функции с БТ
        3. Генерировать содержимое на основе требований

    Пример использования агента:
        br_list = get_documents_names()
        for br in br_list:
            analyze_requirement(br)

    Возвращает:
        List[str]: Имена файлов БТ в формате 'BR_<feature>_<version>.<ext>'
    """
    # Log agent tool activation
    print(f'[BR Agent] Fetching all business requirements')

    # Access document storage service
    document_embedder = DocumentStore()
    return [doc.original_filename for doc in document_embedder.get_all_documents()]